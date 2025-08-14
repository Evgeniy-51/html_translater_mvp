import json
import os
from datetime import datetime


class ProgressManager:
    def __init__(self, progress_file="CONTENT/progress.json"):
        self.progress_file = progress_file
        self.progress = self.load_progress()

    def load_progress(self):
        """Загружает прогресс из файла"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки прогресса: {e}")

        # Возвращаем начальное состояние
        return {
            "last_processed_line": 0,
            "last_translated_line": 0,
            "total_lines": 0,
            "start_time": datetime.now().isoformat(),
            "file_name": "",
        }

    def save_progress(self):
        """Сохраняет прогресс в файл"""
        try:
            os.makedirs(os.path.dirname(self.progress_file), exist_ok=True)
            with open(self.progress_file, "w", encoding="utf-8") as f:
                json.dump(self.progress, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения прогресса: {e}")

    def update_progress(self, line_number, translated=False):
        """Обновляет прогресс"""
        self.progress["last_processed_line"] = line_number
        if translated:
            self.progress["last_translated_line"] = line_number
        self.save_progress()

    def set_total_lines(self, total_lines, file_name):
        """Устанавливает общее количество строк"""
        self.progress["total_lines"] = total_lines
        self.progress["file_name"] = file_name
        self.save_progress()

    def get_last_processed_line(self):
        """Возвращает номер последней обработанной строки"""
        return self.progress["last_processed_line"]

    def get_last_translated_line(self):
        """Возвращает номер последней переведенной строки"""
        return self.progress["last_translated_line"]

    def reset_progress(self):
        """Сбрасывает прогресс"""
        self.progress = {
            "last_processed_line": 0,
            "last_translated_line": 0,
            "total_lines": 0,
            "start_time": datetime.now().isoformat(),
            "file_name": "",
        }
        self.save_progress()
