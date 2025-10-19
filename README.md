# MCP-CB - Telegram Bot with ChatGPT and Web Page Parser

Telegram бот с интеграцией ChatGPT/DeepSeek и MCP fetch сервера для парсинга и анализа веб-страниц.

## 📚 Документация

- **[Полная документация](docs/)** - все инструкции и руководства
- **[Настройка и установка](docs/SETUP.md)** - пошаговое руководство
- **[Примеры использования](docs/EXAMPLES.md)** - как пользоваться ботом
- **[Устранение проблем](docs/TROUBLESHOOTING.md)** - решение типичных ошибок

## Возможности

- 🤖 Интеллектуальные ответы через ChatGPT/DeepSeek API
- 🌐 Автоматическое определение URL в сообщениях
- 📄 Парсинг веб-страниц в Markdown формат через MCP fetch сервер
- 📊 Краткое резюме контента страницы от AI
- 📝 Логирование всех операций

## Требования

- Python 3.12+
- Docker (для MCP fetch сервера)
- Telegram Bot Token
- OpenAI-compatible API Key (DeepSeek, OpenAI, и т.д.)

> 💡 **Подробная инструкция:** см. [docs/SETUP.md](docs/SETUP.md)

## Быстрый старт

### 1. Установка зависимостей

```bash
# Клонируйте репозиторий
git clone <repo-url>
cd MCP_CB

# Создайте виртуальное окружение
python3.12 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate  # Windows

# Установите зависимости
pip install pytelegrambotapi openai mcp
```

### 2. Настройка Docker

```bash
# Скачайте MCP fetch образ
docker pull mcp/fetch

# Проверьте что Docker работает
docker ps
```

### 3. Конфигурация

Создайте `config.json`:

```json
{
  "telegram": {
    "token": "YOUR_TELEGRAM_BOT_TOKEN"
  },
  "openai": {
    "api_key": "YOUR_API_KEY",
    "model": "deepseek-chat",
    "base_url": "https://api.deepseek.com"
  },
  "mcpServers": {
    "fetch": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp/fetch"]
    }
  }
}
```

### 4. Запуск

```bash
python main.py
```

## Использование

Просто отправьте боту URL любой веб-страницы:

```
https://example.com
```

Бот:
1. Определит URL в сообщении
2. Запарсит страницу через MCP fetch сервер
3. Передаст контент ChatGPT для анализа
4. Вернет краткое описание страницы

Также можно задавать обычные вопросы без URL.

## Тестирование

```bash
# Тест MCP fetch функционала
python tests/test_fetch.py

# Тест импортов
python tests/test_imports.py
```

Подробнее о тестах: [tests/README.md](tests/README.md)

## Архитектура

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Telegram   │────▶│     Bot      │────▶│  ChatGPT/   │
│    User     │◀────│   (bot.py)   │◀────│  DeepSeek   │
└─────────────┘     └──────┬───────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ MCP Client   │
                    │(mcp_client.py│
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Docker MCP   │
                    │ Fetch Server │
                    └──────────────┘
```

## Структура проекта

```
MCP_CB/
├── main.py              # Точка входа
├── bot.py               # Логика Telegram бота
├── mcp_client.py        # MCP клиент для fetch сервера
├── config.json          # Конфигурация (не в git)
├── docs/                # 📚 Документация
│   ├── README.md        # Обзор документации
│   ├── SETUP.md         # Инструкция по установке
│   ├── EXAMPLES.md      # Примеры использования
│   └── TROUBLESHOOTING.md  # Устранение проблем
├── tests/               # 🧪 Тестовые скрипты
│   ├── test_fetch.py    # Тест MCP fetch
│   ├── test_imports.py  # Тест импортов
│   └── README.md        # Документация по тестам
└── .github/
    └── copilot-instructions.md  # Инструкции для AI
```

## Дополнительно

- **[Документация](docs/)** - полные руководства и инструкции
- **[Тесты](tests/)** - тестирование функционала
- **[AI инструкции](.github/copilot-instructions.md)** - для разработчиков

## Лицензия

MIT
