#!/usr/bin/env python3
"""
Скрипт проверки что всё необходимое установлено и работает.
Запуск: python check_setup.py
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Проверка версии Python."""
    print("✓ Проверка версии Python...")
    version = sys.version_info
    if version >= (3, 12):
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor} (требуется 3.12+)")
        return False


def check_imports():
    """Проверка основных импортов."""
    print("✓ Проверка импортов...")
    try:
        import telebot
        print("  ✅ pyTelegramBotAPI установлен")
    except ImportError:
        print("  ❌ pyTelegramBotAPI не установлен")
        return False

    try:
        import openai
        print("  ✅ openai установлен")
    except ImportError:
        print("  ❌ openai не установлен")
        return False

    try:
        import mcp
        print("  ✅ mcp установлен")
    except ImportError:
        print("  ❌ mcp не установлен")
        return False

    try:
        import bot
        print("  ✅ bot.py импортируется")
    except Exception as e:
        print(f"  ❌ bot.py имеет ошибки: {e}")
        return False

    try:
        import mcp_client
        print("  ✅ mcp_client.py импортируется")
    except Exception as e:
        print(f"  ❌ mcp_client.py имеет ошибки: {e}")
        return False

    return True


def check_config():
    """Проверка конфигурации."""
    print("✓ Проверка конфигурации...")
    config_file = Path("config.json")
    
    if not config_file.exists():
        print(f"  ❌ config.json не найден")
        print("     Скопируйте config.json.example -> config.json")
        return False
    
    try:
        import json
        with open(config_file) as f:
            config = json.load(f)
        
        # Проверка основных полей
        if "telegram" not in config or "token" not in config["telegram"]:
            print("  ❌ telegram.token не установлен в config.json")
            return False
        
        token = config["telegram"]["token"]
        if token.startswith("YOUR_"):
            print("  ❌ telegram.token содержит placeholder")
            return False
        
        print("  ✅ config.json валиден")
        return True
    except Exception as e:
        print(f"  ❌ Ошибка при проверке config.json: {e}")
        return False


def check_docker():
    """Проверка Docker."""
    print("✓ Проверка Docker...")
    try:
        result = subprocess.run(["docker", "ps"], capture_output=True, timeout=5)
        if result.returncode == 0:
            print("  ✅ Docker работает")
            
            # Проверка MCP образа
            result = subprocess.run(
                ["docker", "images", "--format", "{{.Repository}}"],
                capture_output=True,
                timeout=5,
                text=True
            )
            if "mcp/fetch" in result.stdout:
                print("  ✅ mcp/fetch образ загружен")
                return True
            else:
                print("  ⚠️  mcp/fetch образ не загружен")
                print("     Запустите: docker pull mcp/fetch")
                return False
        else:
            print("  ❌ Docker не работает")
            return False
    except FileNotFoundError:
        print("  ❌ Docker не установлен")
        return False
    except subprocess.TimeoutExpired:
        print("  ⚠️  Docker не отвечает")
        return False
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        return False


def check_files():
    """Проверка необходимых файлов."""
    print("✓ Проверка файлов проекта...")
    required_files = [
        "main.py",
        "bot.py",
        "mcp_client.py",
        "pyproject.toml",
        ".python-version",
    ]
    
    for file in required_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} отсутствует")
            return False
    
    return True


def main():
    """Главная функция."""
    print("\n" + "=" * 50)
    print("🔍 Проверка конфигурации MCP-CB")
    print("=" * 50 + "\n")
    
    checks = [
        ("Python версия", check_python_version),
        ("Файлы проекта", check_files),
        ("Импорты", check_imports),
        ("Конфигурация", check_config),
        ("Docker", check_docker),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
            print()
        except Exception as e:
            print(f"  ❌ Ошибка: {e}\n")
            results.append((name, False))
    
    # Итоговый отчет
    print("=" * 50)
    print("📋 ИТОГОВЫЙ ОТЧЕТ:")
    print("=" * 50)
    
    all_ok = True
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
        if not result:
            all_ok = False
    
    print("=" * 50)
    
    if all_ok:
        print("\n✨ Все проверки пройдены успешно!")
        print("Вы готовы запустить бота:")
        print("  python main.py")
        return 0
    else:
        print("\n⚠️  Некоторые проверки не пройдены.")
        print("Смотрите ошибки выше и выполните рекомендации.")
        print("\n📖 Помощь: https://github.com/maxistm/mcp_use_test#readme")
        return 1


if __name__ == "__main__":
    sys.exit(main())