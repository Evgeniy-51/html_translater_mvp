#!/usr/bin/env python3
"""
Проверка длинных строк
"""

from main import process_lines
from config import BATCH_LIMIT

# Читаем файл
with open("CONTENT/R_J_Haier_The_107_115-.html", "r", encoding="utf-8") as f:
    all_lines = f.readlines()

# Объединяем параграфы
processed_lines = process_lines(all_lines)

print(f"Всего строк после объединения: {len(processed_lines)}")
print(f"BATCH_LIMIT: {BATCH_LIMIT}")

long_lines = []
for i, line in enumerate(processed_lines):
    line_length = len(line.strip())
    if line_length > BATCH_LIMIT:
        long_lines.append((i + 1, line_length, line[:50] + "..."))

print(f"\nНайдено длинных строк (> {BATCH_LIMIT}): {len(long_lines)}")

for line_num, length, preview in long_lines:
    print(f"Строка {line_num}: {length} символов - {preview}")

if long_lines:
    print(f"\nРекомендация: увеличить BATCH_LIMIT до {max(length for _, length, _ in long_lines)}")
else:
    print("Все строки помещаются в текущий лимит")

