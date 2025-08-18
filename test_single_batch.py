#!/usr/bin/env python3
"""
Тестовый скрипт для проверки одного батча и подсчета токенов
"""

from src.core.translator import Translator
from src.prompts.prompt_template import save_prompt_to_file


def test_single_batch():
    """Тестирует перевод одного батча и подсчет токенов"""

    # Обновляем промпт
    save_prompt_to_file()

    # Создаем тестовый батч (строки 16-18 из нашего файла)
    test_batch = [
        {
            "line_number": 16,
            "line": '<body style="background-color:#FFFFFF;"><a name="caption1"></a>',
        },
        {
            "line_number": 17,
            "line": '<h2><a name="bookmark0"></a><span class="font1" style="font-weight:bold;"><a name="bookmark1"></a>Learning Objectives</span></h2>',
        },
        {"line_number": 18, "line": '<ul style="list-style:none;"><li>'},
    ]

    print("=== ТЕСТ ОДНОГО БАТЧА ===")
    print(f"Тестовый батч: {test_batch}")
    print("-" * 50)

    # Создаем переводчик
    translator = Translator()

    try:
        # Переводим батч
        print("Отправляем батч на перевод...")
        result = translator.translate_batch(test_batch)

        print("\n=== РЕЗУЛЬТАТ ===")
        for item in result:
            print(f"Строка {item['line_number']}: {item['translated_line']}")

        # Получаем статистику токенов
        stats = translator.get_token_stats()
        print(f"\n=== СТАТИСТИКА ТОКЕНОВ ===")
        print(f"Запросов к API: {stats['requests']}")
        print(f"Входных токенов: {stats['input_tokens']:,}")
        print(f"Выходных токенов: {stats['output_tokens']:,}")
        print(f"Всего токенов: {stats['total_tokens']:,}")

        # Получаем стоимость
        cost = translator.get_translation_cost()
        print(f"\n=== СТОИМОСТЬ ===")
        print(cost)

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        translator.close()


if __name__ == "__main__":
    test_single_batch()

