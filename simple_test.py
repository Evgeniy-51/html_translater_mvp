#!/usr/bin/env python3
"""
Простой тест логики формирования батчей
"""

def create_batch(lines, start_index):
    """Упрощенная версия функции create_batch для тестирования"""
    batch = []
    current_length = 0
    i = start_index
    BATCH_LIMIT = 1200

    while i < len(lines):
        line = lines[i].strip()
        line_length = len(line)
        
        # Добавляем строку в батч
        batch.append({"line_number": i + 1, "line": line})
        current_length += line_length
        
        # Проверяем, не превысили ли лимит
        if current_length > BATCH_LIMIT:
            # Если превысили лимит, убираем последнюю строку и завершаем
            batch.pop()
            break
        
        i += 1

    return batch


def test_batch():
    """Тестирует логику формирования батчей"""
    
    print("=== ТЕСТ ФОРМИРОВАНИЯ БАТЧЕЙ ===")
    
    # Тестовые строки
    test_lines = [
        "Короткая строка",  # 15 символов
        "Средняя строка с текстом",  # 25 символов
        "Очень длинная строка с большим количеством текста",  # 50 символов
        "Еще одна строка",  # 18 символов
    ]
    
    print(f"Тестовые строки:")
    for i, line in enumerate(test_lines, 1):
        print(f"  {i}: '{line}' ({len(line)} символов)")
    
    print(f"\nЛимит: 1200 символов")
    print("-" * 50)
    
    # Тестируем
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
            print(f"    Строка {item['line_number']}: '{item['line']}'")
        
        start_index += len(batch)
        batch_num += 1


if __name__ == "__main__":
    test_batch()
