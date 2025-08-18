import json
import httpx
from environs import Env
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from src.prompts.prompt_template import generate_prompt, get_json_schema
from src.utils.cost_calculator import format_cost_summary
from config import OPENAI_MODEL


class Translator:
    def __init__(self):
        # Загружаем переменные окружения
        env = Env()
        env.read_env(".env")

        self.api_key = env.str("OPENAI_API_KEY")
        proxy_url = env.str("PROXY_URL")
        proxy_login = env.str("PROXY_LOGIN")
        proxy_password = env.str("PROXY_PASSWORD")

        # Формируем URL прокси с аутентификацией
        proxy_auth_url = (
            f"socks5://{proxy_login}:{proxy_password}@{proxy_url.split('://')[1]}"
        )

        # Настраиваем прокси
        self.http_client = httpx.Client(proxy=proxy_auth_url, timeout=60.0)

        # Инициализируем LLM
        self.llm = ChatOpenAI(
            api_key=self.api_key,
            model=OPENAI_MODEL,
            temperature=0,
            http_client=self.http_client,
        )

        # Настройки
        self.system_prompt = generate_prompt()
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_requests = 0
        self.last_translated_batch = None  # История последнего переведенного батча

    def translate_batch(self, batch):
        """Переводит батч строк используя PromptTemplate с историей"""
        try:
            # Подготавливаем входные данные
            input_data = json.dumps(batch, ensure_ascii=False, indent=2)

            # Подготавливаем историю
            previous_batch_text = ""
            if self.last_translated_batch:
                previous_batch_text = (
                    "Previous translated batch for context:\n"
                    f"{json.dumps(self.last_translated_batch, ensure_ascii=False, indent=2)}\n"
                )

            # Создаем промпт шаблон
            prompt_template = PromptTemplate.from_template(self.system_prompt)

            # Создаем парсер
            output_parser = JsonOutputParser(pydantic_object=get_json_schema())

            # Выполняем цепочку по частям для получения токенов
            prompt_value = prompt_template.invoke(
                {"input": input_data, "previous_batch": previous_batch_text}
            )
            llm_response = self.llm.invoke(prompt_value)
            response = output_parser.invoke(llm_response)

            self.total_requests += 1

            # Сохраняем текущий батч как историю для следующего запроса
            self.last_translated_batch = response

            # Получаем информацию о токенах из промежуточного результата
            if (
                hasattr(llm_response, "response_metadata")
                and llm_response.response_metadata
            ):
                usage = llm_response.response_metadata.get("token_usage", {})
                self.total_input_tokens += usage.get("prompt_tokens", 0)
                self.total_output_tokens += usage.get("completion_tokens", 0)

            return response

        except Exception as e:
            print(f"Ошибка при переводе батча: {e}")
            # Возвращаем исходные строки в случае ошибки
            return [
                {"line_number": item["line_number"], "translated_line": item["line"]}
                for item in batch
            ]

    def get_token_stats(self):
        """Возвращает статистику использования токенов"""
        return {
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "requests": self.total_requests,
        }

    def get_translation_cost(self):
        """Возвращает расчет стоимости перевода"""
        if self.total_input_tokens == 0 and self.total_output_tokens == 0:
            return "Нет данных о токенах для расчета стоимости"

        return format_cost_summary(
            OPENAI_MODEL, self.total_input_tokens, self.total_output_tokens
        )

    def close(self):
        """Закрывает соединения"""
        if hasattr(self, "http_client"):
            self.http_client.close()
