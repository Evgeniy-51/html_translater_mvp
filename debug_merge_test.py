#!/usr/bin/env python3
"""
Отладка объединения параграфов 35-36
"""

from src.parsers.span_merger import should_merge_spans, merge_spans, process_lines

# Тестовые строки 35-36
line_35 = "<p><span class=\"font1\">We had been wondering if low-IQ individuals might have inefficient brains, possibly due to a failure of neural pruning, the normal developmental reduction in excess or extraneous synapses starting about age 5 years. We were interested in scanning people with Down's syndrome who had IQs between 50 and 75, and of course, control groups of people without Down's syndrome who also had IQs in the same low range for no apparent</span></p>"

line_36 = '<p><span class="font1">genetic or brain-damage reason. We also had other controls with IQs in the average range (Haier </span><span class="font1" style="font-style:italic;">et al</span><span class="font1">.,</span><a href="#bookmark17"><span class="font1"> </span><span class="font1" style="text-decoration:underline;color:#5D6CEB;">1995</span></a><span class="font1">).</span></p>'

print("=== АНАЛИЗ СТРОК 35-36 ===")
print(f"Строка 35: {line_35}")
print(f"Строка 36: {line_36}")

print("\n=== ПРОВЕРКА ОБЪЕДИНЕНИЯ ===")
should_merge = should_merge_spans(line_35, line_36)
print(f"Должны ли объединяться: {should_merge}")

if should_merge:
    merged = merge_spans(line_35, line_36)
    print(f"\nОбъединенная строка: {merged}")

    # Проверяем длину
    print(f"Длина объединенной строки: {len(merged)} символов")

    # Проверяем, что весь контент на месте
    if "genetic or brain-damage reason" in merged and "1995" in merged:
        print("✓ Весь контент присутствует в объединенной строке")
    else:
        print("✗ Контент потерян!")
        if "genetic or brain-damage reason" not in merged:
            print("  - Отсутствует: 'genetic or brain-damage reason'")
        if "1995" not in merged:
            print("  - Отсутствует: '1995'")

print("\n=== ТЕСТ С ПОЛНЫМ ФАЙЛОМ ===")
# Читаем файл и проверяем обработку
with open("CONTENT/R_J_Haier-107-115.html", "r", encoding="utf-8") as f:
    all_lines = f.readlines()

processed_lines = process_lines(all_lines)

print(f"Исходных строк: {len(all_lines)}")
print(f"После объединения: {len(processed_lines)}")

# Находим строки 35-36 в обработанном файле
for i, line in enumerate(processed_lines):
    if "We had been wondering if low-IQ individuals" in line:
        print(f"\nНайдена строка {i+1} с началом параграфа:")
        print(
            f"Содержит 'genetic or brain-damage reason': {'genetic or brain-damage reason' in line}"
        )
        print(f"Содержит '1995': {'1995' in line}")
        print(f"Длина строки: {len(line)}")
        break
