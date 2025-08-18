#!/usr/bin/env python3
"""
Тест оптимизированной логики объединения
"""

from src.parsers.span_merger import should_merge_spans
import time


def test_optimized_merge():
    """Тестирует оптимизированную логику объединения"""

    print("=== ТЕСТ ОПТИМИЗИРОВАННОЙ ЛОГИКИ ===")

    # Тест 1: Обычное предложение (быстрый отказ)
    print("\n1. Тест обычного предложения (быстрый отказ):")
    line1 = '<span class="font0">This is a complete sentence.</span>'
    line2 = '<span class="font0">This is another sentence.</span>'

    start_time = time.time()
    should_merge = should_merge_spans(line1, line2)
    end_time = time.time()

    print(f"Строка 1: {line1}")
    print(f"Строка 2: {line2}")
    print(f"Должны объединяться: {should_merge}")
    print(f"Время выполнения: {(end_time - start_time)*1000:.3f} мс")

    # Тест 2: Разорванный параграф (проходит основную проверку)
    print("\n2. Тест разорванного параграфа:")
    line3 = '<span class="font0">This is an incomplete sentence</span>'
    line4 = '<span class="font0">that continues here.</span>'

    start_time = time.time()
    should_merge2 = should_merge_spans(line3, line4)
    end_time = time.time()

    print(f"Строка 3: {line3}")
    print(f"Строка 4: {line4}")
    print(f"Должны объединяться: {should_merge2}")
    print(f"Время выполнения: {(end_time - start_time)*1000:.3f} мс")

    # Тест 3: Заголовок (проходит основную, но не дополнительную проверку)
    print("\n3. Тест заголовка:")
    line5 = '<span class="font0">This is an incomplete sentence</span>'
    line6 = '<span class="font0">This is a new sentence.</span>'

    start_time = time.time()
    should_merge3 = should_merge_spans(line5, line6)
    end_time = time.time()

    print(f"Строка 5: {line5}")
    print(f"Строка 6: {line6}")
    print(f"Должны объединяться: {should_merge3}")
    print(f"Время выполнения: {(end_time - start_time)*1000:.3f} мс")

    # Тест 4: Проблемная ситуация (проходит основную, но не дополнительную)
    print("\n4. Тест проблемной ситуации:")
    line7 = '<p><span class="font1">(Нил Деграсс Тайсон, </span><span class="font1" style="font-style:italic;">HBO\'s Real Time with Bill Maher</span><span class="font1">, 2 апреля 2011 года)</span></p>'
    line8 = '<h2><a name="bookmark10"></a><span class="font3" style="font-weight:bold;"><a name="bookmark11"></a>Цели обучения</span></h2>'

    start_time = time.time()
    should_merge4 = should_merge_spans(line7, line8)
    end_time = time.time()

    print(f"Строка 7: {line7}")
    print(f"Строка 8: {line8}")
    print(f"Должны объединяться: {should_merge4}")
    print(f"Время выполнения: {(end_time - start_time)*1000:.3f} мс")


if __name__ == "__main__":
    test_optimized_merge()
