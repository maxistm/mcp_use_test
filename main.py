"""
Точка входа в приложение - Telegram бот с ChatGPT и MCP интеграцией
"""
import json
import logging
import sys
from pathlib import Path
from bot import ChatBot


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


def load_config(config_path: str = "config.json") -> dict:
    """
    Загрузка конфигурации из JSON файла
    
    Args:
        config_path: Путь к файлу конфигурации
        
    Returns:
        Словарь с конфигурацией
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        logger.info(f"Конфигурация загружена из {config_path}")
        return config
    except FileNotFoundError:
        logger.error(f"Файл конфигурации {config_path} не найден!")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка парсинга JSON в {config_path}: {e}")
        sys.exit(1)


def validate_config(config: dict) -> bool:
    """
    Валидация конфигурации
    
    Args:
        config: Словарь конфигурации
        
    Returns:
        True если конфигурация валидна
    """
    required_keys = [
        ("telegram", "token"),
        ("openai", "api_key"),
        ("openai", "model"),
        ("mcpServers", "fetch")
    ]
    
    for keys in required_keys:
        current = config
        for key in keys:
            if key not in current:
                logger.error(f"Отсутствует обязательный параметр конфигурации: {'.'.join(keys)}")
                return False
            current = current[key]
    
    # Проверка на placeholder значения
    if config["telegram"]["token"] == "YOUR_TELEGRAM_BOT_TOKEN":
        logger.error("Необходимо указать реальный Telegram Bot Token в config.json")
        return False
    
    if config["openai"]["api_key"] == "YOUR_OPENAI_API_KEY":
        logger.error("Необходимо указать реальный OpenAI API Key в config.json")
        return False
    
    return True


def main():
    """Основная функция запуска бота"""
    logger.info("=" * 50)
    logger.info("Запуск Telegram бота MCP-CB")
    logger.info("=" * 50)
    
    # Загрузка конфигурации
    config = load_config()
    
    # Валидация конфигурации
    if not validate_config(config):
        logger.error("Конфигурация невалидна. Исправьте config.json и запустите снова.")
        sys.exit(1)
    
    # Создание и запуск бота
    try:
        bot = ChatBot(config)
        bot.run()
    except KeyboardInterrupt:
        logger.info("\nБот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

