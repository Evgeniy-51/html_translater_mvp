from config import INPUT_LANGUAGE, TARGET_LANGUAGE


def get_language_name(language_code):
    """Возвращает английское название языка"""
    language_names = {
        "english": "English",
        "russian": "Russian",
        "german": "German",
        "french": "French",
        "spanish": "Spanish",
        "italian": "Italian",
        "portuguese": "Portuguese",
        "chinese": "Chinese",
        "japanese": "Japanese",
        "korean": "Korean",
    }
    return language_names.get(language_code.lower(), language_code.title())


def generate_prompt():
    """Генерирует промпт для перевода с учетом языков"""
    input_lang = get_language_name(INPUT_LANGUAGE)
    target_lang = get_language_name(TARGET_LANGUAGE)

    prompt = f"""You are a translator. Translate HTML content from {input_lang} to {target_lang}.

Rules:
- Translate only text within span elements
- Keep all HTML structure unchanged
- Return JSON array with line_number and translated_line fields
- Use previous translation context for consistency

IMPORTANT: Your response must be a JSON array where each object has:
- "line_number": the original line number (integer)
- "translated_line": the translated HTML line (string)

{{previous_batch}}

{{input}}"""

    return prompt


def get_json_schema():
    """Возвращает схему для JsonOutputParser"""
    from pydantic import BaseModel, Field, RootModel
    from typing import List

    class TranslatedLine(BaseModel):
        line_number: int = Field(description="Original line number")
        translated_line: str = Field(description="Translated HTML line")

    class TranslationBatch(RootModel[List[TranslatedLine]]):
        pass

    return TranslationBatch


def save_prompt_to_file():
    """Сохраняет промпт в файл для отладки"""
    prompt = generate_prompt()
    with open("prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)
    print(f"Промпт обновлен для перевода с {INPUT_LANGUAGE} на {TARGET_LANGUAGE}")


if __name__ == "__main__":
    save_prompt_to_file()
