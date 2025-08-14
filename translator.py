from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from environs import Env
import httpx
import os

from prompt_template import generate_prompt
from config import OPENAI_MODEL


class Translator:
    def __init__(self):
        # Загружаем переменные окружения
        env = Env()
        env.read_env(".env")

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

        # Генерируем системный промпт
        self.system_prompt = generate_prompt()

        # Счетчики токенов
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_requests = 0

    def translate_line(self, html_line):
        """
        Переводит HTML строку, переводя только текст в span элементах
        """
        try:
            # Создаем сообщения с системным промптом и пользовательским вводом
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=f"Input: {html_line}\nOutput:"),
            ]

            # Отправляем запрос к ChatGPT
            response = self.llm.invoke(messages)

            # Подсчитываем токены
            if hasattr(response, "response_metadata") and response.response_metadata:
                usage = response.response_metadata.get("token_usage", {})
                self.total_input_tokens += usage.get("prompt_tokens", 0)
                self.total_output_tokens += usage.get("completion_tokens", 0)
                self.total_requests += 1

            return response.content.strip()

        except Exception as e:
            print(f"Ошибка при переводе строки: {e}")
            # В случае ошибки возвращаем оригинальную строку
            return html_line

    def get_token_stats(self):
        """
        Возвращает статистику использования токенов
        """
        return {
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "requests": self.total_requests,
        }

    def close(self):
        """Закрывает HTTP клиент"""
        if hasattr(self, "http_client"):
            self.http_client.close()
