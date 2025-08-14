import os
import sys
from translator import Translator
from translator_test import TranslatorTest
from progress_manager import ProgressManager
from html_parser import HTMLParser
from span_merger import SpanMerger
from config import MODE


def get_translator():
    """
    Возвращает переводчик в зависимости от режима
    """
    if MODE == "test":
        print("Запуск в ТЕСТОВОМ режиме")
        return TranslatorTest()
    elif MODE == "work":
        print("Запуск в РАБОЧЕМ режиме")
        return Translator()
    else:
        raise ValueError(f"Неизвестный режим: {MODE}")


def process_html_file(input_file, output_file=None):
    """
    Обрабатывает HTML файл построчно, переводя span элементы
    """
    if not os.path.exists(input_file):
        print(f"Файл {input_file} не найден!")
        return

    # Определяем выходной файл
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_translated.html"

    # Инициализируем компоненты
    translator = get_translator()
    progress_manager = ProgressManager()
    parser = HTMLParser()
    merger = SpanMerger()

    try:
        # Читаем все строки файла
        with open(input_file, "r", encoding="utf-8") as f:
            all_lines = f.readlines()

        # Объединяем разорванные span элементы
        print("Объединяем разорванные параграфы...")
        processed_lines = merger.process_lines(all_lines)

        total_lines = len(processed_lines)
        progress_manager.set_total_lines(total_lines, input_file)

        # Получаем последнюю обработанную строку
        start_line = progress_manager.get_last_processed_line()

        print(f"Начинаем обработку файла: {input_file}")
        print(f"Всего строк после объединения: {total_lines}")
        print(f"Начинаем с строки: {start_line + 1}")

        # Обрабатываем файл построчно
        with open(output_file, "w", encoding="utf-8") as output_f:

            for line_number, line in enumerate(processed_lines, 1):
                # Пропускаем уже обработанные строки
                if line_number <= start_line:
                    output_f.write(line)
                    continue

                # Проверяем, есть ли span элементы
                if parser.has_span_elements(line):
                    print(f"Переводим строку {line_number}/{total_lines}")

                    # Переводим строку
                    translated_line = translator.translate_line(line)

                    # Сохраняем переведенную строку
                    output_f.write(translated_line + "\n")

                    # Обновляем прогресс
                    progress_manager.update_progress(line_number, translated=True)
                else:
                    # Копируем строку без изменений
                    output_f.write(line)
                    progress_manager.update_progress(line_number, translated=False)

                # Выводим прогресс каждые 10 строк
                if line_number % 10 == 0:
                    print(f"Обработано строк: {line_number}/{total_lines}")

        print(f"Обработка завершена! Результат сохранен в: {output_file}")

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
    if len(sys.argv) < 2:
        print("Использование: python main.py <input_file> [output_file]")
        print("Пример: python main.py CONTENT/R_J_Haier_107-112.html")
        print(f"Текущий режим: {MODE}")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    process_html_file(input_file, output_file)


if __name__ == "__main__":
    main()
