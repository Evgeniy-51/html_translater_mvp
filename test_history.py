#!/usr/bin/env python3
"""
Тест истории сообщений - перевод двух батчей подряд
"""

from src.core.translator import Translator
from src.prompts.prompt_template import save_prompt_to_file


def test_history():
    """Тестирует перевод с историей сообщений"""

    # Обновляем промпт
    save_prompt_to_file()

    # Создаем два тестовых батча
    batch1 = [
        {
            "line_number": 16,
            "line": '<body style="background-color:#FFFFFF;"><a name="caption1"></a>',
        },
        {
            "line_number": 17,
            "line": '<h2><a name="bookmark0"></a><span class="font1" style="font-weight:bold;"><a name="bookmark1"></a>Learning Objectives</span></h2>',
        },
        {
            "line_number": 18,
            "line": '<ul style="list-style:none;"><li>',
        },
    ]

    batch2 = [
        {
            "line_number": 19,
            "line": '<span class="font0">Understand the basic principles of operation</span>',
        },
        {
            "line_number": 20,
            "line": '<span class="font0">Learn safety procedures and guidelines</span>',
        },
        {
            "line_number": 21,
            "line": '<span class="font0">Master troubleshooting techniques</span>',
        },
    ]

    print("=== ТЕСТ ИСТОРИИ СООБЩЕНИЙ ===")
    print("Батч 1:", batch1)
    print("Батч 2:", batch2)
    print("-" * 50)

    # Создаем переводчик
    translator = Translator()

    try:
        # Переводим первый батч
        print("Переводим БАТЧ 1...")
        result1 = translator.translate_batch(batch1)

        print("\n=== РЕЗУЛЬТАТ БАТЧ 1 ===")
        for item in result1:
            print(f"Строка {item['line_number']}: {item['translated_line']}")

        # Переводим второй батч (с историей)
        print("\nПереводим БАТЧ 2 (с историей)...")
        result2 = translator.translate_batch(batch2)

        print("\n=== РЕЗУЛЬТАТ БАТЧ 2 ===")
        for item in result2:
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
    test_history()

