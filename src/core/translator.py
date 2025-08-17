from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from environs import Env
import httpx
import json
from src.prompts.prompt_template import generate_prompt, get_json_schema
from src.utils.cost_calculator import format_cost_summary
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
        """Переводит одну строку (для обратной совместимости)"""
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

    def translate_batch(self, batch):
        """
        Переводит батч строк с использованием output_format

        Args:
            batch: список словарей с ключами 'index' и 'line'

        Returns:
            list: список словарей с ключами 'index' и 'translated_line'
        """
        try:
            # Подготавливаем входные данные
            input_data = json.dumps(batch, ensure_ascii=False, indent=2)

            # Создаем парсер для JSON с правильной схемой
            output_parser = JsonOutputParser(pydantic_object=get_json_schema())

            # Создаем промпт с output_format
            prompt = PromptTemplate(
                template=self.system_prompt, input_variables=["input"]
            )

            # Создаем цепочку с output_format
            chain = prompt | self.llm | output_parser

            # Отправляем запрос
            response = chain.invoke({"input": input_data})

            # Обновляем статистику токенов (если доступна)
            # Примечание: с output_parser статистика может быть недоступна
            self.total_requests += 1

            return response

        except Exception as e:
            print(f"Ошибка при переводе батча: {e}")
            # Возвращаем исходные строки в случае ошибки
            return [
                {"index": item["index"], "translated_line": item["line"]}
                for item in batch
            ]

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

    def get_translation_cost(self):
        """
        Возвращает отформатированный отчет о стоимости перевода
        """
        if self.total_input_tokens == 0 and self.total_output_tokens == 0:
            return "Нет данных о токенах для расчета стоимости"

        return format_cost_summary(
            OPENAI_MODEL, self.total_input_tokens, self.total_output_tokens
        )

    def close(self):
        """Закрывает HTTP клиент"""
        if hasattr(self, "http_client"):
            self.http_client.close()
