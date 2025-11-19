"""
Калькулятор стоимости перевода
"""

from src.utils.model_prices import get_model_price, format_price


class CostCalculator:
    """Калькулятор стоимости перевода"""
    
    def __init__(self, model_name):
        self.model_name = model_name
        self.prices = get_model_price(model_name)
        
        if not self.prices:
            raise ValueError(f"Неизвестная модель: {model_name}")
    
    def calculate_cost(self, input_tokens, output_tokens, cached_tokens=0):
        """
        Рассчитывает стоимость перевода
        
        Args:
            input_tokens: количество входных токенов
            output_tokens: количество выходных токенов
            cached_tokens: количество кэшированных токенов (опционально)
        
        Returns:
            dict: словарь с расчетами стоимости
        """
        # Конвертируем токены в миллионы для расчета
        input_millions = input_tokens / 1_000_000
        output_millions = output_tokens / 1_000_000
        cached_millions = cached_tokens / 1_000_000
        
        # Рассчитываем стоимость
        input_cost = input_millions * self.prices["input"]
        output_cost = output_millions * self.prices["output"]
        cached_cost = cached_millions * self.prices["cached"]
        
        total_cost = input_cost + output_cost + cached_cost
        
        return {
            "model": self.model_name,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cached_tokens": cached_tokens,
            "input_cost": input_cost,
            "output_cost": output_cost,
            "cached_cost": cached_cost,
            "total_cost": total_cost,
            "prices": self.prices
        }
    
    def format_cost_report(self, cost_data):
        """
        Форматирует отчет о стоимости для вывода
        
        Args:
            cost_data: результат calculate_cost()
        
        Returns:
            str: отформатированный отчет
        """
        report = []
        report.append("=== СТОИМОСТЬ ПЕРЕВОДА ===")
        report.append(f"Модель: {cost_data['model']}")
        
        # Входные токены
        input_price = format_price(cost_data['prices']['input'])
        input_cost = format_price(cost_data['input_cost'])
        report.append(
            f"Входные токены: {input_cost} "
            f"({cost_data['input_tokens']:,} × {input_price}/1M)"
        )
        
        # Выходные токены
        output_price = format_price(cost_data['prices']['output'])
        output_cost = format_price(cost_data['output_cost'])
        report.append(
            f"Выходные токены: {output_cost} "
            f"({cost_data['output_tokens']:,} × {output_price}/1M)"
        )
        
        # Кэшированные токены (если есть)
        if cost_data['cached_tokens'] > 0:
            cached_price = format_price(cost_data['prices']['cached'])
            cached_cost = format_price(cost_data['cached_cost'])
            report.append(
                f"Кэшированные токены: {cached_cost} "
                f"({cost_data['cached_tokens']:,} × {cached_price}/1M)"
            )
        
        # Общая стоимость
        total_cost = format_price(cost_data['total_cost'])
        report.append(f"Общая стоимость: {total_cost}")
        report.append("==========================")
        
        return "\n".join(report)
    
    def estimate_cost(self, estimated_tokens):
        """
        Оценивает стоимость для планируемого количества токенов
        
        Args:
            estimated_tokens: предполагаемое количество токенов
        
        Returns:
            dict: оценка стоимости
        """
        # Предполагаем соотношение входных/выходных токенов 3:1
        input_tokens = int(estimated_tokens * 0.75)
        output_tokens = int(estimated_tokens * 0.25)
        
        return self.calculate_cost(input_tokens, output_tokens)


def calculate_translation_cost(model_name, input_tokens, output_tokens, cached_tokens=0):
    """
    Удобная функция для быстрого расчета стоимости
    
    Args:
        model_name: название модели
        input_tokens: входные токены
        output_tokens: выходные токены
        cached_tokens: кэшированные токены
    
    Returns:
        dict: данные о стоимости
    """
    calculator = CostCalculator(model_name)
    return calculator.calculate_cost(input_tokens, output_tokens, cached_tokens)


def format_cost_summary(model_name, input_tokens, output_tokens, cached_tokens=0):
    """
    Удобная функция для получения отформатированного отчета
    
    Args:
        model_name: название модели
        input_tokens: входные токены
        output_tokens: выходные токены
        cached_tokens: кэшированные токены
    
    Returns:
        str: отформатированный отчет
    """
    calculator = CostCalculator(model_name)
    cost_data = calculator.calculate_cost(input_tokens, output_tokens, cached_tokens)
    return calculator.format_cost_report(cost_data)
