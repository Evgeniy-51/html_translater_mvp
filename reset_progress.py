#!/usr/bin/env python3
"""
Скрипт для сброса прогресса перевода
"""

from progress_manager import ProgressManager

def reset_progress():
    """Сбрасывает прогресс перевода"""
    progress_manager = ProgressManager()
    progress_manager.reset_progress()
    print("Прогресс перевода сброшен!")

if __name__ == "__main__":
    reset_progress()
