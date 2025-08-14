import time
import re


class TranslatorTest:
    """Тестовый переводчик с заглушкой"""

    def __init__(self):
        pass

    def translate_line(self, html_line):
        """
        Тестовый режим - имитирует перевод span элементов
        """
        # Имитируем задержку API
        time.sleep(0.1)

        # Находим все span элементы
        spans = re.findall(r"<span[^>]*>(.*?)</span>", html_line, re.DOTALL)

        if not spans:
            return html_line

        # Создаем переведенную версию
        translated_line = html_line

        for span_text in spans:
            # Имитируем перевод - добавляем префикс к тексту
            translated_text = f"[ПЕРЕВЕДЕНО] {span_text}"

            # Заменяем оригинальный текст на переведенный
            translated_line = translated_line.replace(
                f">{span_text}<", f">{translated_text}<"
            )

        return translated_line

    def get_token_stats(self):
        """
        Заглушка для совместимости с реальным переводчиком
        """
        return {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0, "requests": 0}

    def close(self):
        """Заглушка для совместимости с реальным переводчиком"""
        pass
