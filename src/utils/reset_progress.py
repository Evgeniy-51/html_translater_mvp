#!/usr/bin/env python3
"""
Скрипт для сброса прогресса перевода
"""
from src.core.progress_manager import ProgressManager


def reset_progress():
    progress_manager = ProgressManager()
    progress_manager.reset_progress()
    print("Прогресс перевода сброшен!")


if __name__ == "__main__":
    reset_progress()
