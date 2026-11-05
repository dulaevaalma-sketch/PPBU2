import tkinter as tk
from tkinter import ttk, messagebox as mb
import requests

# --- Словарь валют (вынесен в глобальную область для доступа из разных функций) ---
currencies = {
    'EUR': 'Евро',
    'USD': 'Доллар США',
    'JPY': 'Японская йена',
    'GBP': 'Фунт стерлингов',
    'AUD': 'Австралийский доллар',
    'CAD': 'Канадский доллар',
    'CHF': 'Швейцарский франк',
    'CNY': 'Китайский юань',
    'RUB': 'Российский рубль',
    'KZT': 'Казахстанский тенге',
    'UZS': 'Узбекский сум'
}


def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """
    Получает курс валюты из API.
    Возвращает число (float) или выбрасывает исключение.
    """
    try:
        # Запрашиваем данные относительно базовой валюты
        response = requests.get(f'https://open.er-api.com/v6/latest/{from_currency}', timeout=10)
        response.raise_for_status()  # Если сервер вернул ошибку (404, 500), программа остановится здесь

        data = response.json()

        # Проверяем, успешно ли прошел запрос по мнению API
        if data.get('result') != 'success':
            raise Exception(f"Ошибка API: {data.get('error-type', 'Unknown error')}")

        # Проверяем наличие целевой валюты в списке
        if to_currency in data['rates']:
            return data['rates'][to_currency]
        else:
            raise Exception(f"Валюта {to_currency} не найдена в ответе API")

    except requests.exceptions.RequestException as e:
        # Ошибки сети (нет интернета, таймаут)
        raise Exception(f"Ошибка сети: {e}")
    except Exception as e:
        # Любые другие ошибки (парсинг JSON и т.д.)
        raise Exception(f"Ошибка обработки данных: {e}")


def exchange():
    base1 = base_combo_1.get()
    base2 = base_combo_2.get()
    target = target_combo.get()

    if not base1 or not base2 or not target:
        result_label.config(text="Выберите все валюты!")
        return

    try:
        # Получаем курсы. Если внутри get_exchange_rate будет ошибка,
        # она вылетит сюда и попадет в блок except.
        rate1 = get_exchange_rate(base1, target)
        rate2 = get_exchange_rate(base2, target)

        result_text = (
            f"{base1} → {target}: {rate1:.2f}\n"
            f"{base2} → {target}: {rate2:.2f}"
        )
        result_label.config(text=result_text, foreground="black")

    except Exception as er:
        # Ловим все ошибки, которые прилетели из функции получения курса
        result_label.config(text=f"Ошибка: {er}", foreground="red")


# --- Создание окна ---
root = tk.Tk()
root.title("Курсы обмена валют")
root.geometry("350x300")

# Базовая валюта 1
ttk.Label(root, text="Базовая валюта 1").pack(pady=5)
base_combo_1 = ttk.Combobox(root, values=list(currencies.keys()), state="readonly")
base_combo_1.set("EUR")
base_combo_1.pack(pady=2)

# Вторая базовая валюта
ttk.Label(root, text="Базовая валюта 2").pack(pady=5)
base_combo_2 = ttk.Combobox(root, values=list(currencies.keys()), state="readonly")
base_combo_2.set("USD")
base_combo_2.pack(pady=2)

# Целевая валюта
ttk.Label(root, text="Целевая валюта").pack(pady=5)
target_combo = ttk.Combobox(root, values=list(currencies.keys()), state="readonly")
target_combo.set("RUB")
target_combo.pack(pady=2)

# Кнопка
btn = ttk.Button(root, text="Получить курс обмена", command=exchange)
btn.pack(pady=15)

# Результат
result_label = ttk.Label(root, text="Выберите валюты и нажмите кнопку", justify="center", font=("Arial", 11))
result_label.pack(pady=5)

root.mainloop()