import re


class HTMLParser:
    @staticmethod
    def has_span_elements(html_line):
        """
        Проверяет, содержит ли HTML строка span элементы
        """
        # Простая проверка на наличие <span в строке
        return "<span" in html_line

    @staticmethod
    def count_span_elements(html_line):
        """
        Подсчитывает количество span элементов в строке
        """
        # Находим все открывающие теги span
        span_tags = re.findall(r"<span[^>]*>", html_line)
        return len(span_tags)

    @staticmethod
    def extract_span_text(html_line):
        """
        Извлекает текст из span элементов (для отладки)
        """
        # Находим все span элементы и их содержимое
        spans = re.findall(r"<span[^>]*>(.*?)</span>", html_line, re.DOTALL)
        return spans
