#!/usr/bin/env python3
"""
Тест нового формата вывода
"""


def simulate_output():
    """Симулирует новый формат вывода"""

    print("=== ТЕСТ НОВОГО ФОРМАТА ВЫВОДА ===")

    # Симуляция обработки файла
    total_lines = 43
    batch_counter = 1

    # Примеры батчей
    batches = [
        (1, 4),  # батч 1: строки 1-4
        (5, 3),  # батч 2: строки 5-7
        (8, 2),  # батч 3: строки 8-9
        (10, 5),  # батч 4: строки 10-14
        (15, 3),  # батч 5: строки 15-17
    ]

    for start_line, batch_size in batches:
        end_line = start_line + batch_size - 1
        print(
            f"send {batch_counter} batch {batch_size} lines ({start_line}-{end_line}/{total_lines})"
        )
        batch_counter += 1

    print(f"\nОбработано строк: {total_lines}/{total_lines}")
    print("Обработка завершена!")


if __name__ == "__main__":
    simulate_output()
