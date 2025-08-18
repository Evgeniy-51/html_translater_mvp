#!/usr/bin/env python3
"""
Тест для отладки проблемы объединения
"""

from src.parsers.span_merger import should_merge_spans, merge_spans, clean_html_tags
import re


def debug_merge():
    """Отладка проблемы объединения"""

    # Проблемная ситуация
    line1 = '<p><span class="font1">(Нил Деграсс Тайсон, </span><span class="font1" style="font-style:italic;">HBO\'s Real Time with Bill Maher</span><span class="font1">, 2 апреля 2011 года)</span></p>'
    line2 = '<h2><a name="bookmark10"></a><span class="font3" style="font-weight:bold;"><a name="bookmark11"></a>Цели обучения</span></h2>'

    print("=== ОТЛАДКА ПРОБЛЕМЫ ОБЪЕДИНЕНИЯ ===")
    print(f"Строка 1: {line1}")
    print(f"Строка 2: {line2}")

    # Проверяем span'ы в первой строке
    spans1 = re.findall(r"<span[^>]*>(.*?)</span>", line1, re.DOTALL)
    print(f"\nSpan'ы в строке 1:")
    for i, span in enumerate(spans1):
        print(f"  {i}: '{span}'")

    # Проверяем span'ы во второй строке
    spans2 = re.findall(r"<span[^>]*>(.*?)</span>", line2, re.DOTALL)
    print(f"\nSpan'ы в строке 2:")
    for i, span in enumerate(spans2):
        print(f"  {i}: '{span}'")

    # Проверяем логику
    if spans1 and spans2:
        last_span1 = spans1[-1].strip()
        first_span2 = spans2[0].strip()

        print(f"\nПоследний span строки 1: '{last_span1}'")
        print(f"Первый span строки 2: '{first_span2}'")

        # Очищаем HTML-теги
        clean_last_span1 = clean_html_tags(last_span1)
        clean_first_span2 = clean_html_tags(first_span2)

        print(f"Очищенный последний span: '{clean_last_span1}'")
        print(f"Очищенный первый span: '{clean_first_span2}'")

        # Проверяем условия
        from config import sentence_endings

        current_ends_with_punctuation = any(
            clean_last_span1.endswith(p) for p in sentence_endings
        )
        next_starts_with_capital = clean_first_span2 and clean_first_span2[0].isupper()

        print(f"Заканчивается знаками препинания: {current_ends_with_punctuation}")
        print(f"Начинается с заглавной буквы: {next_starts_with_capital}")
        print(
            f"Должны объединяться: {not current_ends_with_punctuation and not next_starts_with_capital}"
        )

    # Тестируем функцию
    should_merge = should_merge_spans(line1, line2)
    print(f"\nРезультат should_merge_spans: {should_merge}")


if __name__ == "__main__":
    debug_merge()
