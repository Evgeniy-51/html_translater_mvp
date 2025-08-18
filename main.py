import os
import sys
import json

from src.core.translator import Translator
from src.core.translator_test import TranslatorTest
from src.core.progress_manager import ProgressManager
from src.parsers.html_parser import HTMLParser
from src.parsers.span_merger import process_lines
from config import MODE, OPENAI_MODEL, BATCH_LIMIT
from src.prompts.prompt_template import save_prompt_to_file
from src.gui.file_selector import select_file_gui, select_output_file_gui


def get_translator():
    """
    Возвращает переводчик в зависимости от режима
    """
    if MODE == "test":
        print("Запуск в ТЕСТОВОМ режиме")
        return TranslatorTest()
    elif MODE == "work":
        print(f"Запуск в РАБОЧЕМ режиме с моделью: {OPENAI_MODEL}")
        return Translator()
    else:
        raise ValueError(f"Неизвестный режим: {MODE}")


def create_batch(lines, start_index, batch_size=3):
    """
    Создает батч строк для отправки в нейросеть на основе лимита символов

    Args:
        lines: список всех строк
        start_index: индекс начала батча
        batch_size: устаревший параметр (оставлен для совместимости)

    Returns:
        list: батч строк с их номерами
    """
    batch = []
    current_length = 0
    i = start_index

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


def process_html_file(input_file, output_file=None):
    """
    Обрабатывает HTML файл батчами, переводя span элементы
    """
    if not os.path.exists(input_file):
        print(f"Файл {input_file} не найден!")
        return

    # Определяем выходной файл
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_translated.html"

    # Обновляем промпт перед началом работы
    save_prompt_to_file()

    # Инициализируем компоненты
    translator = get_translator()
    progress_manager = ProgressManager()
    parser = HTMLParser()

    try:
        # Читаем все строки файла
        with open(input_file, "r", encoding="utf-8") as f:
            all_lines = f.readlines()

        # Объединяем разорванные span элементы
        print("Объединяем разорванные параграфы...")
        processed_lines = process_lines(all_lines)

        total_lines = len(processed_lines)
        progress_manager.set_total_lines(total_lines, input_file)

        # Получаем последнюю обработанную строку
        start_line = progress_manager.get_last_processed_line()

        print(f"Начинаем обработку файла: {input_file}")
        print(f"Всего строк после объединения: {total_lines}")
        print(f"Начинаем с строки: {start_line + 1}")
        print(f"Лимит батча: {BATCH_LIMIT} символов")

        # Обрабатываем файл батчами
        with open(output_file, "w", encoding="utf-8") as output_f:
            i = start_line

            while i < total_lines:
                # Создаем батч
                batch = create_batch(processed_lines, i, batch_size=3)

                if not batch:
                    break

                # Проверяем, есть ли в батче строки с span элементами
                has_translatable_content = any(
                    parser.has_span_elements(item["line"]) for item in batch
                )

                if has_translatable_content:
                    print(f"Переводим батч строк {i+1}-{i+len(batch)}/{total_lines}")

                    # Отправляем батч на перевод
                    translated_batch = translator.translate_batch(batch)

                    # Сохраняем переведенные строки
                    for item in translated_batch:
                        output_f.write(item["translated_line"] + "\n")
                        progress_manager.update_progress(
                            item["line_number"], translated=True
                        )
                else:
                    # Копируем строки без изменений
                    for item in batch:
                        output_f.write(item["line"] + "\n")
                        progress_manager.update_progress(
                            item["line_number"], translated=False
                        )

                # Переходим к следующему батчу
                i += len(batch)

                # Выводим прогресс каждые 10 строк
                if i % 10 == 0 or i >= total_lines:
                    print(f"Обработано строк: {i}/{total_lines}")

        print(f"Обработка завершена! Результат сохранен в: {output_file}")

        # Выводим статистику токенов для рабочего режима
        if MODE == "work" and hasattr(translator, "get_token_stats"):
            stats = translator.get_token_stats()
            print("\n=== СТАТИСТИКА ТОКЕНОВ ===")
            print(f"Запросов к API: {stats['requests']}")
            print(f"Входных токенов: {stats['input_tokens']:,}")
            print(f"Выходных токенов: {stats['output_tokens']:,}")
            print(f"Всего токенов: {stats['total_tokens']:,}")
            print("==========================")

            # Выводим стоимость перевода
            if hasattr(translator, "get_translation_cost"):
                cost_report = translator.get_translation_cost()
                print(f"\n{cost_report}")

    except KeyboardInterrupt:
        print("\nОбработка прервана пользователем")
        print(
            f"Прогресс сохранен. Можно продолжить с строки {progress_manager.get_last_processed_line() + 1}"
        )

    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        print(
            f"Прогресс сохранен. Можно продолжить с строки {progress_manager.get_last_processed_line() + 1}"
        )

    finally:
        translator.close()


def main():
    """Основная функция"""
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1:
        # Режим командной строки
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None

        if not os.path.exists(input_file):
            print(f"Файл {input_file} не найден!")
            return

        process_html_file(input_file, output_file)
    else:
        # Режим GUI
        print("HTML Lines Translator")
        print(f"Режим: {MODE}")
        if MODE == "work":
            print(f"Модель: {OPENAI_MODEL}")
        print("-" * 50)

        # Выбираем входной файл
        print("Выберите HTML файл для перевода...")
        input_file = select_file_gui()

        if input_file is None:
            print("Выбор файла отменен.")
            return

        print(f"Выбран файл: {input_file}")

        # Выбираем место сохранения
        print("Выберите место для сохранения переведенного файла...")
        output_file = select_output_file_gui(input_file)

        if output_file is None:
            print("Выбор места сохранения отменен.")
            return

        print(f"Файл будет сохранен как: {output_file}")
        print("-" * 50)

        # Обрабатываем файл
        process_html_file(input_file, output_file)


if __name__ == "__main__":
    main()
