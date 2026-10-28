import tkinter as tk
from tkinter import ttk

# Заглушка для получения курсов (в реальном проекте замените на запрос к API)
def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    # Пример статических курсов относительно RUB
    rates = {
        ("EUR", "RUB"): 92.5,
        ("USD", "RUB"): 85.0,
        ("RUB", "RUB"): 1.0,
    }
    return rates.get((from_currency, to_currency), 1.0)

def exchange():
    base1 = base_combo_1.get()
    base2 = base_combo_2.get()
    target = target_combo.get()

    if not base1 or not base2 or not target:
        result_label.config(text="Выберите все валюты!")
        return

    rate1 = get_exchange_rate(base1, target)
    rate2 = get_exchange_rate(base2, target)

    result_text = (
        f"{base1} → {target}: {rate1:.2f}\n"
        f"{base2} → {target}: {rate2:.2f}"
    )
    result_label.config(text=result_text)

# Создание окна
root = tk.Tk()
root.title("Курсы обмена валют")
root.geometry("350x300")

# Базовая валюта 1
ttk.Label(root, text="Базовая валюта").pack(pady=5)
base_combo_1 = ttk.Combobox(root, values=["EUR", "USD", "CNY"], state="readonly")
base_combo_1.set("EUR")
base_combo_1.pack(pady=2)

# Вторая базовая валюта (новый элемент по п. 1)
ttk.Label(root, text="Вторая базовая валюта").pack(pady=5)
base_combo_2 = ttk.Combobox(root, values=["EUR", "USD", "CNY"], state="readonly")
base_combo_2.set("USD")
base_combo_2.pack(pady=2)

# Целевая валюта
ttk.Label(root, text="Целевая валюта").pack(pady=5)
target_combo = ttk.Combobox(root, values=["RUB", "EUR", "USD"], state="readonly")
target_combo.set("RUB")
target_combo.pack(pady=2)

# Кнопка
btn = ttk.Button(root, text="Получить курс обмена", command=exchange)
btn.pack(pady=15)

# Результат
result_label = ttk.Label(root, text="", justify="center", font=("Arial", 11))
result_label.pack(pady=5)

root.mainloop()
