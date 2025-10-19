"""
MCP Client для работы с MCP fetch сервером через Docker
Использует официальную библиотеку MCP Python SDK
"""
import logging
import asyncio
from typing import Dict, Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger(__name__)


class MCPClient:
    """Клиент для взаимодействия с MCP fetch сервером через Docker"""
    
    def __init__(self, server_config: Dict[str, Any]):
        """
        Инициализация MCP клиента
        
        Args:
            server_config: Конфигурация MCP сервера из config.json
        """
        self.command = str(server_config.get("command"))
        self.args = server_config.get("args", [])
        
    def fetch_url(self, url: str) -> Optional[str]:
        """
        Получение содержимого веб-страницы в markdown формате
        
        Args:
            url: URL страницы для парсинга
            
        Returns:
            Содержимое страницы в markdown или None при ошибке
        """
        try:
            logger.info(f"Парсинг URL: {url}")
            
            # Запускаем async функцию в sync контексте
            result = asyncio.run(self._fetch_url_async(url))
            return result
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге URL: {e}")
            return None
    
    async def _fetch_url_async(self, url: str) -> Optional[str]:
        """
        Асинхронное получение контента страницы
        
        Args:
            url: URL страницы
            
        Returns:
            Контент страницы или None
        """
        # Параметры для запуска Docker контейнера
        server_params = StdioServerParameters(
            command=self.command,
            args=self.args,
            env=None
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Инициализация сессии
                await session.initialize()
                
                # Вызов инструмента fetch
                result = await session.call_tool("fetch", arguments={"url": url})
                
                # Извлекаем текст из результата
                if result and hasattr(result, 'content'):
                    for item in result.content:
                        if hasattr(item, 'text'):
                            text = item.text
                            logger.info(f"Получен контент: {len(text)} символов")
                            return text
                
                return None
