# MCP-CB - Telegram Bot with ChatGPT and Web Page Parser

Telegram бот с интеграцией ChatGPT/DeepSeek и MCP fetch сервера для парсинга и анализа веб-страниц.

## 📚 Документация

Проект использует современный подход с `pyproject.toml` для управления зависимостями и конфигурацией.

### Основные файлы конфигурации:
- **`pyproject.toml`** - описание проекта, зависимости и настройки
- **`config.json`** - конфигурация бота (токены, API ключи)
- **`.python-version`** - версия Python (3.12)
- **`uv.lock`** - lock-файл для точного воспроизведения зависимостей

## Возможности

- 🤖 Интеллектуальные ответы через ChatGPT/DeepSeek API
- 🌐 Автоматическое определение URL в сообщениях
- 📄 Парсинг веб-страниц в Markdown формат через MCP fetch сервер
- 📊 Краткое резюме контента страницы от AI
- 📝 Логирование всех операций

## Требования

- Python 3.12+ (указано в `.python-version`)
- Docker (для MCP fetch сервера)
- Telegram Bot Token
- OpenAI-compatible API Key (DeepSeek, OpenAI, и т.д.)

> 💡 **Зависимости:** автоматически устанавливаются из `pyproject.toml`

## ⚡ Быстрый старт

### За 4 шага:

```bash
# 1. Клонирование
git clone <repo-url>
cd mcp_use_test

# 2. Окружение
python3.12 -m venv .venv
source .venv/bin/activate  # Linux/Mac или .venv\Scripts\activate (Windows)

# 3. Установка зависимостей из pyproject.toml
pip install -e .

# 4. Конфигурация
cp config.json.example config.json
# Отредактируйте config.json со своими токенами

# 5. Запуск
python main.py
```

📖 **Полные инструкции выше** с получением токенов и решением проблем

### Требования перед запуском:

```bash
# Скачайте MCP fetch образ Docker
docker pull mcp/fetch

# Проверьте что Docker работает
docker ps
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
# Убедитесь, что зависимости установлены
pip install -e .

# Тест импортов и базовой функциональности
python -c "import bot, mcp_client, main; print('Все модули импортированы успешно')"

# Проверка MCP fetch функционала (требует Docker)
python -c "import asyncio; from mcp_client import MCPClient; print('MCP клиент готов к работе')"
```

### Альтернативная установка с uv

Если у вас установлен [uv](https://github.com/astral-sh/uv):

```bash
# Установка зависимостей с uv (быстрее pip)
uv sync

# Запуск с uv
uv run python main.py
```

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
mcp_use_test/
├── main.py              # Точка входа
├── bot.py               # Логика Telegram бота
├── mcp_client.py        # MCP клиент для fetch сервера
├── pyproject.toml       # Конфигурация проекта и зависимости
├── uv.lock              # Lock-файл для uv package manager
├── config.json          # Конфигурация (не в git)
├── config.json.example  # Пример конфигурации
├── .python-version      # Версия Python (3.12)
├── .venv/               # Виртуальное окружение (не в git)
├── bot.log              # Логи работы бота
└── .github/
    └── copilot-instructions.md  # Инструкции для AI
```

## Дополнительно

### Управление зависимостями

Проект использует `pyproject.toml` для современного управления зависимостями:

```toml
[project]
name = "mcp-cb"
version = "0.1.0"
description = "Telegram chatbot with ChatGPT and MCP server integration"
requires-python = ">=3.12"
dependencies = [
    "pyTelegramBotAPI>=4.14.0",
    "openai>=1.12.0", 
    "requests>=2.31.0",
    "mcp",
]
```

### Добавление новых зависимостей

```bash
# Добавить новую зависимость
echo 'new-package>=1.0.0' >> pyproject.toml

# Переустановить с новыми зависимостями  
pip install -e .

# Или с uv
uv add new-package
```

### Часто задаваемые вопросы (FAQ)

**Q: Как получить Telegram Bot Token?**
- Поговорите с [@BotFather](https://t.me/botfather) в Telegram
- Используйте команду `/newbot` и следуйте инструкциям

**Q: Как получить API ключ DeepSeek?**
- Перейдите на [DeepSeek API платформу](https://platform.deepseek.com)
- Создайте аккаунт и сгенерируйте API ключ

**Q: Docker требуется?**
- Да, для работы MCP fetch сервера
- Установите Docker Desktop для вашей ОС

**Q: Можно использовать OpenAI вместо DeepSeek?**
- Да! Просто измените `base_url` и `model` в `config.json`

**Q: Ошибка "config.json не найден"**
- Запустите: `cp config.json.example config.json`
- Отредактируйте с вашими данными

**Q: Ошибка "Cannot connect to Docker daemon"**
- Docker не запущен. Запустите Docker Desktop или демон
- Linux: `sudo systemctl start docker`

## Разработка

### Настройка окружения разработчика

```bash
# Установка с dev зависимостями
pip install -e .

# С инструментами для разработки
pip install black flake8 isort pytest

# Или с uv
uv sync
```

### Форматирование и проверка кода

```bash
# Форматирование
black .
isort .

# Проверка стиля
flake8 .

# Запуск тестов
pytest
```

### Проверка конфигурации

```bash
python check_setup.py
```

### Кодовые конвенции

- ✅ Type hints обязательны
- ✅ Docstrings для функций и методов
- ✅ Логирование вместо print
- ✅ Python 3.12+ idioms
- ✅ Async/await для MCP операций

## Вклад в проект

### Процесс PR

1. Fork репозиторий
2. Создайте feature branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "feat: описание"`
4. Push и создайте Pull Request

### Типы коммитов

```
feat:   новая функция
fix:    исправление ошибки
docs:   документация
refactor: переделка кода
test:   тесты
chore:  служебные файлы
```

## Лицензия

MIT
