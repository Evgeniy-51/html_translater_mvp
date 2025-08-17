from config import INPUT_LANGUAGE, TARGET_LANGUAGE


def get_language_name(language_code):
    """Возвращает название языка на английском"""
    language_names = {
        "english": "English",
        "russian": "Russian",
        "chinese": "Chinese",
        "spanish": "Spanish",
        "french": "French",
        "italian": "Italian",
        "japanese": "Japanese",
        "korean": "Korean",
        "german": "German",
    }
    return language_names.get(language_code.lower(), language_code.title())


def generate_prompt():
    """Генерирует промпт для перевода"""
    input_lang = get_language_name(INPUT_LANGUAGE)
    target_lang = get_language_name(TARGET_LANGUAGE)

    prompt = f"""You are a professional translator specializing in HTML content translation from {input_lang} to {target_lang}.

Your task is to translate HTML lines while preserving all HTML structure, tags, attributes, and formatting.

## Input Format
You will receive a JSON array of HTML lines, each with an index and content.

## Translation Rules
1. **Translate only text content** within `<span>` elements from {input_lang} to {target_lang}
2. **Preserve all HTML structure** - tags, attributes, classes, IDs, etc.
3. **Maintain line order** and formatting exactly as in the input
4. **Keep non-translatable lines unchanged** - if a line has no span elements or no translatable content, return it as-is
5. **Use context from surrounding lines** for better translation accuracy
6. **Preserve special characters** and HTML entities

## Output Format
Return a JSON array with the same structure, containing translated lines. Each object should have:
- "index": the original line index (integer)
- "translated_line": the translated HTML line (string)

## Important Notes
- Only translate text within `<span>` elements
- Keep all other HTML elements unchanged
- If text cannot be translated, leave it as-is
- Maintain the exact same HTML structure and attributes
- Use the context from multiple lines for better translation quality

Translate the following batch of HTML lines from {input_lang} to {target_lang}:

{{input}}"""

    return prompt


def get_json_schema():
    """Возвращает схему JSON для output_format"""
    return {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "index": {"type": "integer"},
                "translated_line": {"type": "string"},
            },
            "required": ["index", "translated_line"],
        },
    }


def save_prompt_to_file():
    """Сохраняет промпт в файл"""
    prompt = generate_prompt()
    with open("prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)
    print(f"Промпт обновлен для перевода с {INPUT_LANGUAGE} на {TARGET_LANGUAGE}")


if __name__ == "__main__":
    save_prompt_to_file()
