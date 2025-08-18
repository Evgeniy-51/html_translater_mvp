#!/usr/bin/env python3
"""
Тест новой логики формирования батчей
"""

from main import create_batch


def test_batch_creation():
    """Тестирует новую логику формирования батчей"""

    print("=== ТЕСТ ФОРМИРОВАНИЯ БАТЧЕЙ ===")

    # Тестовые строки разной длины
    test_lines = [
        "Короткая строка",  # ~15 символов
        "Средняя строка с дополнительным текстом",  # ~40 символов
        "Очень длинная строка с большим количеством текста, который должен превысить лимит батча и показать, как работает новая логика формирования батчей на основе количества символов",  # ~150 символов
        "Еще одна короткая строка",  # ~25 символов
        "Средняя строка номер два",  # ~25 символов
        "И еще одна средняя строка",  # ~25 символов
    ]

    print(f"Тестовые строки:")
    for i, line in enumerate(test_lines, 1):
        print(f"  {i}: '{line}' ({len(line)} символов)")

    print(f"\nЛимит батча: 1200 символов")
    print("-" * 50)

    # Тестируем формирование батчей
    start_index = 0
    batch_num = 1

    while start_index < len(test_lines):
        batch = create_batch(test_lines, start_index)

        if not batch:
            break

        total_chars = sum(len(item["line"]) for item in batch)

        print(f"\nБатч {batch_num}:")
        print(f"  Строки: {[item['line_number'] for item in batch]}")
        print(f"  Количество строк: {len(batch)}")
        print(f"  Общая длина: {total_chars} символов")

        for item in batch:
            print(
                f"    Строка {item['line_number']}: '{item['line']}' ({len(item['line'])} символов)"
            )

        start_index += len(batch)
        batch_num += 1


if __name__ == "__main__":
    test_batch_creation()
