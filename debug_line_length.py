#!/usr/bin/env python3
"""
Проверка длины строки 21
"""

from main import process_lines

# Читаем файл
with open("CONTENT/R_J_Haier_The_107_115-.html", "r", encoding="utf-8") as f:
    all_lines = f.readlines()

# Объединяем параграфы
processed_lines = process_lines(all_lines)

# Проверяем строку 21 (индекс 20)
line_21 = processed_lines[20]
print(f"Строка 21 (индекс 20):")
print(f"Длина: {len(line_21)} символов")
print(f"Содержимое: {line_21[:100]}...")
print(f"Полное содержимое: {line_21}")

# Проверяем BATCH_LIMIT
from config import BATCH_LIMIT
print(f"\nBATCH_LIMIT: {BATCH_LIMIT}")

if len(line_21) > BATCH_LIMIT:
    print(f"ПРОБЛЕМА: Строка 21 ({len(line_21)} символов) превышает BATCH_LIMIT ({BATCH_LIMIT})")
else:
    print(f"Строка 21 помещается в лимит")

