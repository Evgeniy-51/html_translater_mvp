import re


class SpanMerger:
    @staticmethod
    def should_merge_spans(current_line, next_line):
        """
        Проверяет, нужно ли объединить span элементы из текущей и следующей строки
        """
        if not current_line or not next_line:
            return False

        # Извлекаем текст из span элементов
        current_spans = re.findall(r"<span[^>]*>(.*?)</span>", current_line, re.DOTALL)
        next_spans = re.findall(r"<span[^>]*>(.*?)</span>", next_line, re.DOTALL)

        if not current_spans or not next_spans:
            return False

        # Берем последний span из текущей строки и первый из следующей
        current_text = current_spans[-1].strip()
        next_text = next_spans[0].strip()

        # Проверяем условия объединения
        # 1. Текущий span не заканчивается на знаки завершения
        # 2. Следующий span не начинается с заглавной буквы
        sentence_endings = [".", "!", "?", "...", ":", ";"]
        current_ends_with_sentence = any(
            current_text.endswith(ending) for ending in sentence_endings
        )
        next_starts_with_capital = next_text and next_text[0].isupper()

        return not current_ends_with_sentence and not next_starts_with_capital

    @staticmethod
    def merge_spans(current_line, next_line):
        """
        Объединяет span элементы из двух строк
        """
        # Находим все span элементы
        current_spans = re.findall(r"(<span[^>]*>.*?</span>)", current_line, re.DOTALL)
        next_spans = re.findall(r"(<span[^>]*>.*?</span>)", next_line, re.DOTALL)

        if not current_spans or not next_spans:
            return current_line, next_line

        # Объединяем последний span из текущей строки с первым из следующей
        last_current_span = current_spans[-1]
        first_next_span = next_spans[0]

        # Извлекаем содержимое span элементов
        last_content = re.search(
            r"<span[^>]*>(.*?)</span>", last_current_span, re.DOTALL
        )
        first_content = re.search(
            r"<span[^>]*>(.*?)</span>", first_next_span, re.DOTALL
        )

        if not last_content or not first_content:
            return current_line, next_line

        # Объединяем содержимое
        merged_content = (
            last_content.group(1).strip() + " " + first_content.group(1).strip()
        )

        # Создаем новый объединенный span с атрибутами первого
        span_attrs = re.search(r"<span([^>]*)>", first_next_span)
        if span_attrs:
            new_span = f"<span{span_attrs.group(1)}>{merged_content}</span>"
        else:
            new_span = f"<span>{merged_content}</span>"

        # Заменяем последний span в текущей строке
        merged_current = re.sub(
            r"<span[^>]*>.*?</span>(?=[^<]*$)", new_span, current_line, flags=re.DOTALL
        )

        # Удаляем первый span из следующей строки
        merged_next = re.sub(
            r"<span[^>]*>.*?</span>", "", next_line, count=1, flags=re.DOTALL
        )

        return merged_current, merged_next

    @staticmethod
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

            # Проверяем, есть ли следующая строка и нужно ли объединение
            if i + 1 < len(lines) and SpanMerger.should_merge_spans(
                current_line, lines[i + 1]
            ):
                # Объединяем текущую и следующую строку
                merged_current, merged_next = SpanMerger.merge_spans(
                    current_line, lines[i + 1]
                )

                # Добавляем объединенную строку
                if merged_current.strip():
                    processed_lines.append(merged_current)

                # Если в следующей строке остался контент, добавляем его
                if merged_next.strip():
                    processed_lines.append(merged_next)

                # Пропускаем следующую строку (она уже обработана)
                i += 2
            else:
                # Добавляем строку без изменений
                processed_lines.append(current_line)
                i += 1

        return processed_lines
