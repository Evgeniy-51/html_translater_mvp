import re
from config import sentence_endings


def clean_html_tags(text):
    """
    Удаляет HTML-теги из текста, оставляя только текст
    """
    # Удаляем все HTML-теги
    clean_text = re.sub(r"<[^>]+>", "", text)
    return clean_text.strip()


def should_merge_spans(current_line, next_line):
    """
    Определяет, нужно ли объединить span элементы из текущей и следующей строки
    """
    # Ищем span элементы в текущей строке
    current_spans = re.findall(r"<span[^>]*>(.*?)</span>", current_line, re.DOTALL)
    if not current_spans:
        return False

    # Ищем span элементы в следующей строке
    next_spans = re.findall(r"<span[^>]*>(.*?)</span>", next_line, re.DOTALL)
    if not next_spans:
        return False

    # Получаем текст последнего span из текущей строки
    current_text = current_spans[-1].strip()

    # ОСНОВНАЯ ПРОВЕРКА: Текущий span не заканчивается знаками sentence_endings
    clean_current_text = clean_html_tags(current_text)
    current_ends_with_punctuation = any(
        clean_current_text.endswith(p) for p in sentence_endings
    )

    # Если текущий span заканчивается знаками препинания - НЕ объединяем
    if current_ends_with_punctuation:
        return False

    # ДОПОЛНИТЕЛЬНАЯ ПРОВЕРКА: Следующий span не начинается с заглавной буквы
    next_text = next_spans[0].strip()
    clean_next_text = clean_html_tags(next_text)
    next_starts_with_capital = clean_next_text and clean_next_text[0].isupper()

    # Если следующий span начинается с заглавной буквы - НЕ объединяем
    return not next_starts_with_capital


def merge_spans(current_line, next_line):
    """
    Объединяет span элементы из текущей и следующей строки
    """
    # Ищем span элементы в текущей строке
    current_spans = re.findall(r"<span[^>]*>(.*?)</span>", current_line, re.DOTALL)
    next_spans = re.findall(r"<span[^>]*>(.*?)</span>", next_line, re.DOTALL)

    if not current_spans or not next_spans:
        return current_line, next_line

    # Объединяем текст последнего span из текущей строки с первым span из следующей
    merged_text = current_spans[-1].strip() + " " + next_spans[0].strip()

    # Заменяем текст в текущей строке
    current_line = re.sub(
        r"(<span[^>]*>)(.*?)(</span>)",
        lambda m: (
            m.group(1) + merged_text + m.group(3)
            if m.group(2).strip() == current_spans[-1].strip()
            else m.group(0)
        ),
        current_line,
        flags=re.DOTALL,
    )

    # Удаляем первый span из следующей строки
    next_line = re.sub(
        r"(<span[^>]*>)(.*?)(</span>)",
        lambda m: ("" if m.group(2).strip() == next_spans[0].strip() else m.group(0)),
        next_line,
        flags=re.DOTALL,
    )

    return current_line, next_line


def clean_li_markers(html_line):
    """
    Удаляет лишние маркеры списков, которые появляются при восстановлении HTML из PDF
    """
    # Закомментировано: пусть li остаются как есть
    # return html_line.replace("• &nbsp;", "&nbsp;")
    return html_line


def process_lines(lines):
    """
    Обрабатывает список строк, объединяя разорванные span элементы
    """
    if not lines:
        return lines

    processed_lines = []
    i = 0

    while i < len(lines):
        current_line = lines[i]

        # Проверяем, есть ли следующая строка
        if i + 1 < len(lines):
            next_line = lines[i + 1]

            # Если нужно объединить span элементы
            if should_merge_spans(current_line, next_line):
                # Объединяем строки
                merged_current, merged_next = merge_spans(current_line, next_line)

                # Добавляем объединенную текущую строку
                if merged_current.strip():
                    processed_lines.append(clean_li_markers(merged_current))

                # Пропускаем следующую строку (она была объединена)
                i += 2
                continue

        # Если объединение не требуется, добавляем текущую строку как есть
        processed_lines.append(clean_li_markers(current_line))
        i += 1

    return processed_lines
