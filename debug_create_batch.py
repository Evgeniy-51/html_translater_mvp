#!/usr/bin/env python3
"""
Детальная отладка функции create_batch
"""

from main import create_batch, process_lines
from config import BATCH_LIMIT

# Читаем файл
with open("CONTENT/R_J_Haier_The_107_115-.html", "r", encoding="utf-8") as f:
    all_lines = f.readlines()

# Объединяем параграфы
processed_lines = process_lines(all_lines)

print(f"Всего строк после объединения: {len(processed_lines)}")
print(f"BATCH_LIMIT: {BATCH_LIMIT}")

# Тестируем create_batch для индекса 21
i = 21
print(f"\nТестируем create_batch для индекса {i}:")
print(f"Строка {i}: {processed_lines[i][:50]}...")

batch = create_batch(processed_lines, i)
print(f"Результат create_batch: {batch}")

if not batch:
    print("Батч пустой! Проверяем логику...")
    
    # Проверим, что происходит в create_batch
    batch = []
    current_length = 0
    j = i
    
    print(f"\nПошаговая отладка:")
    while j < len(processed_lines):
        line = processed_lines[j].strip()
        line_length = len(line)
        
        print(f"  Индекс {j}: длина строки {line_length}")
        print(f"    Строка: {line[:30]}...")
        
        # Проверяем, не превысим ли лимит
        if current_length + line_length > BATCH_LIMIT:
            print(f"    ПРЕВЫШЕНИЕ ЛИМИТА: {current_length} + {line_length} = {current_length + line_length} > {BATCH_LIMIT}")
            break
        
        # Добавляем строку в батч
        batch.append({"line_number": j + 1, "line": line})
        current_length += line_length
        print(f"    Добавлена в батч. Текущая длина: {current_length}")
        
        j += 1
        
        if j > i + 5:  # Ограничиваем для отладки
            print("    Ограничение отладки")
            break
    
    print(f"Итоговый батч: {len(batch)} строк")

