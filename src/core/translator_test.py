import time
import re
import json


class TranslatorTest:
    """Тестовый переводчик для разработки без использования API"""

    def __init__(self):
        print("Инициализирован тестовый переводчик")

    def translate_line(self, html_line):
        """
        Тестовый перевод одной строки
        """
        time.sleep(0.1)  # Имитируем задержку API
        
        # Ищем span элементы
        spans = re.findall(r"<span[^>]*>(.*?)</span>", html_line, re.DOTALL)
        
        if not spans:
            return html_line
        
        # Переводим текст в span элементах
        translated_line = html_line
        for span_text in spans:
            translated_text = f"[ПЕРЕВЕДЕНО] {span_text}"
            translated_line = translated_line.replace(
                f">{span_text}<", f">{translated_text}<"
            )
        
        return translated_line

    def translate_batch(self, batch):
        """
        Тестовый перевод батча строк
        
        Args:
            batch: список словарей с ключами 'index' и 'line'
        
        Returns:
            list: список словарей с ключами 'index' и 'translated_line'
        """
        time.sleep(0.2)  # Имитируем задержку API для батча
        
        translated_batch = []
        
        for item in batch:
            index = item["index"]
            line = item["line"]
            
            # Ищем span элементы
            spans = re.findall(r"<span[^>]*>(.*?)</span>", line, re.DOTALL)
            
            if not spans:
                # Если нет span элементов, возвращаем строку без изменений
                translated_batch.append({
                    "index": index,
                    "translated_line": line
                })
            else:
                # Переводим текст в span элементах
                translated_line = line
                for span_text in spans:
                    translated_text = f"[ПЕРЕВЕДЕНО] {span_text}"
                    translated_line = translated_line.replace(
                        f">{span_text}<", f">{translated_text}<"
                    )
                
                translated_batch.append({
                    "index": index,
                    "translated_line": translated_line
                })
        
        return translated_batch

    def get_token_stats(self):
        """Возвращает нулевую статистику для тестового режима"""
        return {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "requests": 0,
        }

    def get_translation_cost(self):
        """Возвращает сообщение о том, что в тестовом режиме нет стоимости"""
        return "Тестовый режим - стоимость не рассчитывается"

    def close(self):
        """Закрывает тестовый переводчик"""
        pass
