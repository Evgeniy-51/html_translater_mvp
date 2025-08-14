from langchain_openai import ChatOpenAI
from environs import Env
import httpx
import os
from prompt_template import generate_prompt
from config import OPENAI_MODEL


class Translator:
    def __init__(self):
        # Загружаем переменные окружения
        env = Env()
        env.read_env(".env copy")  # Используем копию .env файла

        # Получаем данные из .env
        self.api_key = env("OPENAI_API_KEY")
        proxy_url = env("PROXY_URL")
        proxy_login = env("PROXY_LOGIN")
        proxy_password = env("PROXY_PASSWORD")

        # Формируем URL прокси с аутентификацией
        proxy_auth_url = (
            f"socks5://{proxy_login}:{proxy_password}@{proxy_url.split('://')[1]}"
        )

        # Настраиваем HTTP-клиент с прокси
        self.http_client = httpx.Client(proxy=proxy_auth_url)

        # Инициализируем ChatGPT с моделью из конфигурации
        self.llm = ChatOpenAI(
            api_key=self.api_key,
            model=OPENAI_MODEL,
            temperature=0,
            http_client=self.http_client,
        )

        # Генерируем динамический промпт
        self.prompt_template = generate_prompt()

    def translate_line(self, html_line):
        """
        Переводит HTML строку, переводя только текст в span элементах
        """
        try:
            # Формируем полный промпт с HTML строкой
            full_prompt = f"{self.prompt_template}\n\nInput: {html_line}\nOutput:"

            # Отправляем запрос к ChatGPT
            response = self.llm.invoke(full_prompt)

            return response.content.strip()

        except Exception as e:
            print(f"Ошибка при переводе строки: {e}")
            # В случае ошибки возвращаем оригинальную строку
            return html_line

    def close(self):
        """Закрывает HTTP клиент"""
        if hasattr(self, "http_client"):
            self.http_client.close()
