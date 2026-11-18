import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
from datetime import datetime

CONFIG_FILE = 'config.json'
TICKERS_URL = "https://api.coinpaprika.com/v1/tickers"
DEFAULT_COINS = ['btc', 'eth', 'sol', 'usdt']

APP_TITLE = "Приложение для отображения курсов криптовалют"
PROJECT_LABEL = "Аттестационный проект «CryptoTracker»"


class CryptoTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("800x500")

        self.coins = self.load_coins()

        # --- Верхняя строка: подпись проекта слева (чёрным) ---
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill='x', padx=10, pady=(8, 0))

        project_label = ttk.Label(
            top_frame,
            text=PROJECT_LABEL,
            font=('Arial', 10, 'bold'),
            foreground='black',
            anchor='w',
        )
        project_label.pack(side='left')

        # --- Заголовок приложения по центру ---
        title_label = ttk.Label(
            self.root,
            text=APP_TITLE,
            font=('Arial', 16, 'bold'),
            anchor='center',
        )
        title_label.pack(fill='x', padx=10, pady=(12, 15))

        # --- Таблица ---
        columns = ("name", "ticker", "price", "change", "market_cap")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')

        self.tree.heading("name", text="Название")
        self.tree.heading("ticker", text="Тикер")
        self.tree.heading("price", text="Цена (USD)")
        self.tree.heading("change", text="24h %")
        self.tree.heading("market_cap", text="Капитализация")

        self.tree.column("name", width=230, anchor='w')
        self.tree.column("ticker", width=80, anchor='center')
        self.tree.column("price", width=110, anchor='e')
        self.tree.column("change", width=90, anchor='e')
        self.tree.column("market_cap", width=120, anchor='e')

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.tree.pack(expand=True, fill='both', padx=10, pady=(0, 10))

        # --- Статус-бар ---
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill='x', side='bottom', padx=10, pady=5)
        self.status_label = ttk.Label(status_frame, text="Готово", anchor='w')
        self.status_label.pack(side='left', expand=True, fill='x')
        ttk.Button(status_frame, text="🔄 Обновить", command=self.update_prices).pack(side='right')

        self.update_prices()

    # --- Сохранение списка монет ---
    def load_coins(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, list) and all(isinstance(c, str) for c in data):
                    return [c.lower() for c in data]
            except (json.JSONDecodeError, OSError):
                pass
        return DEFAULT_COINS.copy()

    def save_coins(self):
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.coins, f, ensure_ascii=False, indent=2)
        except OSError as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить настройки:\n{e}")

    # --- Данные ---
    def fetch_tickers(self):
        resp = requests.get(TICKERS_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        by_symbol = {}
        for item in data:
            symbol = (item.get('symbol') or '').lower()
            if symbol:
                by_symbol.setdefault(symbol, item)
        return by_symbol

    @staticmethod
    def _is_number(value):
        try:
            float(value)
            return True
        except (TypeError, ValueError):
            return False

    @staticmethod
    def format_price(price):
        if not CryptoTrackerApp._is_number(price):
            return "N/A"
        return f"${price:,.2f}"

    @staticmethod
    def format_change(change):
        if not CryptoTrackerApp._is_number(change):
            return "N/A"
        return f"{change:+.2f}%"

    @staticmethod
    def format_market_cap(cap):
        if not CryptoTrackerApp._is_number(cap):
            return "N/A"
        if cap >= 1_000_000_000:
            return f"${cap / 1_000_000_000:.2f}B"
        if cap >= 1_000_000:
            return f"${cap / 1_000_000:.2f}M"
        return f"${cap:,.0f}"

    def update_prices(self):
        self.status_label.config(text="Обновление...")
        self.root.update_idletasks()

        if not self.coins:
            for row in self.tree.get_children():
                self.tree.delete(row)
            self.status_label.config(text="Список пуст.")
            return

        try:
            by_symbol = self.fetch_tickers()
        except requests.RequestException as e:
            messagebox.showerror("Ошибка API", f"Ошибка сети:\n{e}")
            self.status_label.config(text="Нет связи")
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        missing = []

        for coin in self.coins:
            item = by_symbol.get(coin)
            if item is None:
                missing.append(coin.upper())
                continue

            usd = item.get('quotes', {}).get('USD', {})
            self.tree.insert('', 'end', values=(
                item.get('name', 'N/A'),
                (item.get('symbol') or coin).upper(),
                self.format_price(usd.get('price')),
                self.format_change(usd.get('percent_change_24h')),
                self.format_market_cap(usd.get('market_cap')),
            ))

        status = f"Обновлено: {datetime.now().strftime('%H:%M:%S')}"
        if missing:
            status += f" | Не найдены: {', '.join(missing)}"
        self.status_label.config(text=status)


def main():
    root = tk.Tk()
    app = CryptoTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
