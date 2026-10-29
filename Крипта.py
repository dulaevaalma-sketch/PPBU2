import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading
import json
import os
from datetime import datetime

CACHE_FILE = "crypto_cache.json"
AUTO_REFRESH_SECONDS = 60  # интервал автообновления в секундах


class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Курсы криптовалют (Аттестационный проект)")
        self.root.geometry("600x400")

        self.coin_ids = ["bitcoin", "ethereum", "solana", "binancecoin", "dogecoin"]
        self.is_loading = False

        self.setup_ui()

        # Сначала пробуем загрузить кэш, потом делаем первый запрос
        self.load_cache()
        self.fetch_data()

        # Запускаем автообновление
        self.schedule_auto_refresh()

    def setup_ui(self):
        header_frame = tk.Frame(self.root)
        header_frame.pack(pady=10)

        tk.Label(header_frame, text="Криптовалюты", font=("Arial", 16, "bold")).pack()

        cols = ("Монета", "Цена (USD)", "Изменение 24ч")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings", height=10)

        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10)

        # Теги для цвета строк
        self.tree.tag_configure("green", foreground="green")
        self.tree.tag_configure("red", foreground="red")

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.update_btn = tk.Button(btn_frame, text="Обновить курсы", command=self.start_fetch_thread, bg="#dddddd")
        self.update_btn.pack()

        self.status_label = tk.Label(self.root, text="Ожидание данных...", fg="gray")
        self.status_label.pack(side="bottom", pady=5)

    def schedule_auto_refresh(self):
        """Планирует следующее автообновление"""
        self.root.after(AUTO_REFRESH_SECONDS * 1000, self.auto_refresh)

    def auto_refresh(self):
        """Автообновление: если не идёт загрузка — запускаем запрос"""
        if not self.is_loading:
            self.start_fetch_thread()
        # Снова планируем следующий цикл
        self.schedule_auto_refresh()

    def load_cache(self):
        """Загружает данные из кэша, если файл есть"""
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    cached = json.load(f)

                # Проверяем, что данные свежие (не старше 24 часов)
                cache_time = datetime.fromisoformat(cached.get("timestamp"))
                if (datetime.now() - cache_time).total_seconds() < 24 * 3600:
                    self.update_table(cached["data"])
                    self.status_label.config(text="Данные кэшированы (без интернета)", fg="orange")
            except Exception:
                # Если кэш битый — просто игнорируем
                pass

    def save_cache(self, data):
        """Сохраняет данные в кэш с меткой времени"""
        payload = {
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        try:
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        except Exception:
            pass  # Не прерываем работу, если не удалось сохранить кэш

    def fetch_data(self):
        """Запрос к API CoinGecko"""
        try:
            ids_str = ",".join(self.coin_ids)
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_str}&vs_currencies=usd&include_24hr_change=true"

            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Сохраняем кэш
            self.save_cache(data)

            self.root.after(0, lambda: self.update_table(data))
            self.root.after(0, lambda: self._finish_loading(success=True))

        except requests.exceptions.RequestException as e:
            # При ошибке сети показываем кэш (если есть)
            self.load_cache()
            self.root.after(0, lambda: self._handle_error(f"Ошибка сети: {e}", str(e)))
        except Exception as e:
            self.root.after(0, lambda: self._handle_error(f"Ошибка обработки: {e}", str(e)))

    def _finish_loading(self, success: bool):
        self.is_loading = False
        self.update_btn.config(state="normal", text="Обновить курсы")
        if success:
            self.status_label.config(text="Данные обновлены успешно", fg="green")

    def _handle_error(self, status_text: str, error_details: str):
        self.is_loading = False
        self.update_btn.config(state="normal", text="Обновить курсы")
        self.status_label.config(text=status_text, fg="red")
        # Для первого запроса показываем окно ошибки, для автообновлений — нет
        # Можно добавить флаг, чтобы не спамить окнами
        messagebox.showerror("Ошибка",
                             f"Не удалось получить данные.\nПроверьте подключение к интернету.\nДетали: {error_details}")

    def update_table(self, data):
        self.tree.delete(*self.tree.get_children())

        names = {
            "bitcoin": "Bitcoin (BTC)",
            "ethereum": "Ethereum (ETH)",
            "solana": "Solana (SOL)",
            "binancecoin": "Binance Coin (BNB)",
            "dogecoin": "Dogecoin (DOGE)"
        }

        for coin_id in self.coin_ids:
            coin_data = data.get(coin_id)
            if not coin_data:
                continue

            price = coin_data.get("usd")
            change = coin_data.get("usd_24h_change")

            if price is None or change is None:
                continue

            color_tag = "green" if change > 0 else "red"
            change_text = f"+{change:.2f}%" if change > 0 else f"{change:.2f}%"

            name = names.get(coin_id, coin_id.capitalize())

            item_id = self.tree.insert("", "end", values=(name, f"${price:,.2f}", change_text))
            self.tree.item(item_id, tags=(color_tag,))

    def start_fetch_thread(self):
        if self.is_loading:
            return
        self.is_loading = True
        self.update_btn.config(state="disabled", text="Загрузка...")
        thread = threading.Thread(target=self.fetch_data, daemon=True)
        thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()




