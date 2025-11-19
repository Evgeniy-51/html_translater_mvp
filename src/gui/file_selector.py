import tkinter as tk
from tkinter import filedialog, messagebox
import os


class FileSelector:
    """Класс для выбора HTML файла через графический интерфейс"""

    def __init__(self):
        self.root = None

    def _create_root(self):
        """Создает корневое окно Tkinter"""
        if self.root is None:
            self.root = tk.Tk()
            self.root.withdraw()  # Скрываем основное окно
            # Устанавливаем окно поверх всех остальных
            self.root.attributes("-topmost", True)

    def _destroy_root(self):
        """Уничтожает корневое окно"""
        if self.root:
            try:
                self.root.destroy()
            except:
                pass
            self.root = None

    def select_html_file(self):
        """
        Открывает диалог выбора HTML файла
        Возвращает путь к выбранному файлу или None если отменено
        """
        try:
            self._create_root()

            # Настраиваем диалог выбора файла
            file_path = filedialog.askopenfilename(
                title="Выберите HTML файл для перевода",
                filetypes=[
                    ("HTML files", "*.html"),
                    ("HTML files", "*.htm"),
                    ("All files", "*.*"),
                ],
                initialdir=os.getcwd(),  # Начинаем с текущей директории
            )

            # Проверяем, был ли выбран файл
            if file_path:
                # Проверяем существование файла
                if not os.path.exists(file_path):
                    messagebox.showerror("Ошибка", f"Файл не найден:\n{file_path}")
                    self._destroy_root()
                    return None

                # Проверяем расширение файла
                if not file_path.lower().endswith((".html", ".htm")):
                    result = messagebox.askyesno(
                        "Предупреждение",
                        f"Выбранный файл не имеет расширения .html или .htm:\n{file_path}\n\nПродолжить?",
                    )
                    if not result:
                        self._destroy_root()
                        return None

                self._destroy_root()
                return file_path
            else:
                # Пользователь отменил выбор
                self._destroy_root()
                return None

        except Exception as e:
            self._destroy_root()
            messagebox.showerror("Ошибка", f"Ошибка при выборе файла:\n{str(e)}")
            return None

    def select_output_file(self, input_file_path):
        """
        Открывает диалог для выбора места сохранения переведенного файла
        """
        try:
            self._create_root()

            # Генерируем предложенное имя файла
            base_name = os.path.splitext(input_file_path)[0]
            suggested_name = f"{base_name}_translated.html"

            # Настраиваем диалог сохранения файла
            file_path = filedialog.asksaveasfilename(
                title="Сохранить переведенный файл как",
                defaultextension=".html",
                filetypes=[("HTML files", "*.html"), ("All files", "*.*")],
                initialdir=os.path.dirname(input_file_path),
                initialfile=os.path.basename(suggested_name),
            )

            self._destroy_root()
            return file_path if file_path else None

        except Exception as e:
            self._destroy_root()
            messagebox.showerror(
                "Ошибка", f"Ошибка при выборе места сохранения:\n{str(e)}"
            )
            return None


def select_file_gui():
    """
    Простая функция для выбора файла через GUI
    """
    selector = FileSelector()
    return selector.select_html_file()


def select_output_file_gui(input_file_path):
    """
    Простая функция для выбора места сохранения
    """
    selector = FileSelector()
    return selector.select_output_file(input_file_path)
