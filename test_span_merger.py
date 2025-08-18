#!/usr/bin/env python3
"""
Тест логики объединения параграфов
"""

from src.parsers.span_merger import should_merge_spans, merge_spans, process_lines


def test_span_merger():
    """Тестирует логику объединения параграфов"""

    print("=== ТЕСТ ОБЪЕДИНЕНИЯ ПАРАГРАФОВ ===")

    # Тест 1: Обычный параграф (не должен объединяться)
    print("\n1. Тест обычного параграфа:")
    line1 = '<span class="font0">This is a complete sentence.</span>'
    line2 = '<span class="font0">This is another sentence.</span>'

    should_merge = should_merge_spans(line1, line2)
    print(f"Строка 1: {line1}")
    print(f"Строка 2: {line2}")
    print(f"Должны объединяться: {should_merge}")

    # Тест 2: Разорванный параграф (должен объединяться)
    print("\n2. Тест разорванного параграфа:")
    line3 = '<span class="font0">This is an incomplete sentence</span>'
    line4 = '<span class="font0">that continues here.</span>'

    should_merge2 = should_merge_spans(line3, line4)
    print(f"Строка 3: {line3}")
    print(f"Строка 4: {line4}")
    print(f"Должны объединяться: {should_merge2}")

    if should_merge2:
        merged3, merged4 = merge_spans(line3, line4)
        print(f"Объединенная строка 3: {merged3}")
        print(f"Объединенная строка 4: {merged4}")

    # Тест 3: Заголовок (НЕ должен объединяться)
    print("\n3. Тест заголовка:")
    line5 = '<span class="font0">This is an incomplete sentence</span>'
    line6 = '<span class="font0">This is a new sentence.</span>'

    should_merge3 = should_merge_spans(line5, line6)
    print(f"Строка 5: {line5}")
    print(f"Строка 6: {line6}")
    print(f"Должны объединяться: {should_merge3}")

    # Тест 4: Реальный пример из файла
    print("\n4. Тест реального примера:")
    real_line1 = '<span class="font0">• &nbsp;Understand the basic principles of operation</span>'
    real_line2 = (
        '<span class="font0">and maintenance procedures for the equipment.</span>'
    )

    should_merge4 = should_merge_spans(real_line1, real_line2)
    print(f"Реальная строка 1: {real_line1}")
    print(f"Реальная строка 2: {real_line2}")
    print(f"Должны объединяться: {should_merge4}")

    if should_merge4:
        merged_real1, merged_real2 = merge_spans(real_line1, real_line2)
        print(f"Объединенная реальная строка 1: {merged_real1}")
        print(f"Объединенная реальная строка 2: {merged_real2}")

    # Тест 5: Проблемная ситуация из файла
    print("\n5. Тест проблемной ситуации:")
    problem_line1 = '<h2><a name="bookmark10"></a><span class="font3" style="font-weight:bold;"><a name="bookmark11"></a>Learning Objectives</span></h2>'
    problem_line2 = '<p><a name="bookmark12"></a><span class="font2">How is intelligence defined for most scientific research?</span></p>'

    should_merge5 = should_merge_spans(problem_line1, problem_line2)
    print(f"Проблемная строка 1: {problem_line1}")
    print(f"Проблемная строка 2: {problem_line2}")
    print(f"Должны объединяться: {should_merge5}")

    # Тест 6: Обработка списка строк
    print("\n6. Тест обработки списка строк:")
    test_lines = [
        '<span class="font0">This is a complete sentence.</span>',
        '<span class="font0">This is an incomplete sentence</span>',
        '<span class="font0">that continues here.</span>',
        '<span class="font0">Another complete sentence.</span>',
        '<span class="font0">• &nbsp;List item one</span>',
        '<span class="font0">continues here.</span>',
        '<span class="font0">This is an incomplete sentence</span>',
        '<span class="font0">This is a new sentence.</span>',
    ]

    print("Исходные строки:")
    for i, line in enumerate(test_lines, 1):
        print(f"  {i}: {line}")

    processed = process_lines(test_lines)

    print("\nОбработанные строки:")
    for i, line in enumerate(processed, 1):
        print(f"  {i}: {line}")


if __name__ == "__main__":
    test_span_merger()
