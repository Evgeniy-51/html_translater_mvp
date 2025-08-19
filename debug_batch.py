#!/usr/bin/env python3
"""
Отладочный скрипт для проверки логики формирования батчей
"""

from main import create_batch, process_lines
from src.parsers.html_parser import HTMLParser


def debug_batch_creation():
    """Отладка формирования батчей"""
    
    # Читаем файл
    with open("CONTENT/R_J_Haier_The_107_115-.html", "r", encoding="utf-8") as f:
        all_lines = f.readlines()
    
    print(f"Исходный файл: {len(all_lines)} строк")
    
    # Объединяем параграфы
    processed_lines = process_lines(all_lines)
    print(f"После объединения: {len(processed_lines)} строк")
    
    # Проверяем формирование батчей
    parser = HTMLParser()
    i = 0
    batch_num = 1
    
    while i < len(processed_lines):
        print(f"\n--- Батч {batch_num} ---")
        print(f"Начинаем с индекса: {i}")
        
        # Создаем батч
        batch = create_batch(processed_lines, i)
        
        if not batch:
            print(f"Батч пустой! Индекс: {i}")
            break
        
        print(f"Батч содержит {len(batch)} строк")
        
        # Проверяем, есть ли переводимый контент
        has_translatable_content = any(
            parser.has_span_elements(item["line"]) for item in batch
        )
        
        print(f"Есть переводимый контент: {has_translatable_content}")
        
        # Показываем первые строки батча
        for j, item in enumerate(batch[:3]):
            line_preview = item["line"][:50] + "..." if len(item["line"]) > 50 else item["line"]
            print(f"  Строка {item['line_number']}: {line_preview}")
        
        if len(batch) > 3:
            print(f"  ... и еще {len(batch) - 3} строк")
        
        # Переходим к следующему батчу
        i += len(batch)
        batch_num += 1
        
        if batch_num > 10:  # Ограничиваем количество батчей для отладки
            print("Ограничение: показано только 10 батчей")
            break
    
    print(f"\nОбработано батчей: {batch_num - 1}")
    print(f"Обработано строк: {i}")
    print(f"Осталось строк: {len(processed_lines) - i}")


if __name__ == "__main__":
    debug_batch_creation()

