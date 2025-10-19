"""
Telegram бот с интеграцией ChatGPT и MCP fetch сервера
Бот определяет URL в сообщениях и предоставляет краткую информацию о странице
"""
import logging
import json
import re
from typing import Dict, Any
import telebot
from openai import OpenAI
from mcp_client import MCPClient

logger = logging.getLogger(__name__)


class ChatBot:
    """Основной класс Telegram бота"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Инициализация бота
        
        Args:
            config: Конфигурация из config.json
        """
        self.config = config
        
        # Инициализация Telegram бота
        self.bot = telebot.TeleBot(config["telegram"]["token"])
        
        # Инициализация OpenAI клиента
        self.openai_client = OpenAI(
            api_key=config["openai"]["api_key"],
            base_url=config["openai"]["base_url"]
        )
        self.model = config["openai"]["model"]
        
        # Инициализация MCP клиента для fetch
        self.mcp_client = MCPClient(config["mcpServers"]["fetch"])
        
        # Регистрация обработчиков
        self._register_handlers()
        
    def _register_handlers(self):
        """Регистрация обработчиков сообщений"""
        
        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            welcome_text = (
                "Привет! Я бот с интеграцией ChatGPT и парсингом веб-страниц.\n\n"
                "Я могу:\n"
                "- Отвечать на вопросы с помощью ChatGPT\n"
                "- Парсить и анализировать веб-страницы (просто отправь URL)\n\n"
                "Отправь мне URL или задай вопрос!"
            )
            self.bot.reply_to(message, welcome_text)
        
        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            try:
                response = self._process_message(message.text)
                self.bot.reply_to(message, response)
            except Exception as e:
                logger.error(f"Ошибка при обработке сообщения: {e}")
                self.bot.reply_to(message, "Извините, произошла ошибка при обработке вашего запроса.")
    
    def _extract_url(self, text: str) -> str:
        """
        Извлекает URL из текста
        
        Args:
            text: Текст сообщения
            
        Returns:
            URL если найден, иначе None
        """
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+' 
        match = re.search(url_pattern, text)
        return match.group(0) if match else None
    
    def _process_message(self, user_message: str) -> str:
        """
        Обработка сообщения пользователя
        
        Args:
            user_message: Текст сообщения от пользователя
            
        Returns:
            Ответ бота
        """
        # Подготовка контекста для ChatGPT
        messages = [
            {
                "role": "system",
                "content": "Ты полезный ассистент, который может анализировать веб-страницы и отвечать на вопросы."
            }
        ]
        
        # Проверяем наличие URL в сообщении
        url = self._extract_url(user_message)
        
        if url:
            logger.info(f"Найден URL в сообщении: {url}")
            
            # Получаем контент страницы через MCP fetch
            page_content = self.mcp_client.fetch_url(url)
            
            if page_content:
                # Ограничиваем контент для ChatGPT
                max_content_length = 8000
                if len(page_content) > max_content_length:
                    page_content = page_content[:max_content_length] + "\n\n[...контент обрезан...]"
                
                # Добавляем контент страницы в контекст
                messages.append({
                    "role": "system",
                    "content": f"Контент веб-страницы {url}:\n\n{page_content}"
                })
                logger.info("Контент страницы добавлен в контекст")
                
                # Изменяем сообщение пользователя для более релевантного ответа
                
            else:
                logger.warning("Не удалось получить контент страницы")
                return f"К сожалению, не удалось загрузить содержимое страницы {url}. Попробуйте другой URL."
        
        # Добавляем сообщение пользователя
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Получаем ответ от ChatGPT
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            answer = response.choices[0].message.content
            logger.info("Получен ответ от ChatGPT")
            return answer
            
        except Exception as e:
            logger.error(f"Ошибка при обращении к OpenAI API: {e}")
            return "Извините, не могу обработать ваш запрос в данный момент."
    
    def run(self):
        """Запуск бота в режиме polling"""
        logger.info("Бот запущен...")
        self.bot.infinity_polling()
