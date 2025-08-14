# HTML Lines Translator

Приложение для перевода HTML файлов с английского на русский язык с использованием ChatGPT.

## Особенности

- Построчная обработка HTML файлов
- Перевод только текста в span элементах
- Сохранение структуры HTML
- Восстановление после обрыва соединения
- Работа через прокси

## Установка

1. Установите зависимости:
```bash
uv pip install -r requirements.txt
```

2. Настройте переменные окружения в файле `.env copy`:
```
OPENAI_API_KEY=your_api_key
PROXY_URL=socks5://proxy_host:port
PROXY_LOGIN=proxy_username
PROXY_PASSWORD=proxy_password
```

## Использование

```bash
python main.py CONTENT/R_J_Haier_107-112.html
```

### Параметры

- `input_file` - путь к входному HTML файлу
- `output_file` - путь к выходному файлу (опционально)

### Примеры

```bash
# Базовое использование
python main.py CONTENT/R_J_Haier_107-112.html

# С указанием выходного файла
python main.py CONTENT/R_J_Haier_107-112.html CONTENT/result.html
```

## Структура проекта

- `main.py` - основной модуль
- `translator.py` - работа с ChatGPT
- `progress_manager.py` - управление прогрессом
- `html_parser.py` - парсинг HTML
- `prompt.txt` - промпт для ChatGPT
- `CONTENT/` - папка с файлами
- `CONTENT/progress.json` - файл прогресса

## Восстановление после обрыва

При обрыве соединения приложение автоматически сохраняет прогресс. При повторном запуске обработка продолжится с последней успешно переведенной строки.

## Логика работы

1. Читает HTML файл построчно
2. Ищет строки с span элементами
3. Отправляет строку в ChatGPT для перевода
4. Сохраняет результат в выходной файл
5. Обновляет прогресс после каждой строки
