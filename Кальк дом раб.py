import tkinter as tk
from tkinter import messagebox

def multiply_three():
    a_str = entry_a.get().strip()
    b_str = entry_b.get().strip()
    c_str = entry_c.get().strip()

    if not a_str or not b_str or not c_str:
        messagebox.showwarning("Внимание", "Пожалуйста, заполните все три поля числами.")
        return

    try:
        a = float(a_str)
        b = float(b_str)
        c = float(c_str)
        result = a * b * c

        if result.is_integer():
            result_text = f"Результат: {int(result)}"
        else:
            result_text = f"Результат: {result:.4f}".rstrip('0').rstrip('.')

        label_result.config(text=result_text)
    except ValueError:
        messagebox.showerror("Ошибка", "Во всех полях должны быть корректные числа (можно с точкой).")

def add_three():
    a_str = entry_a.get().strip()
    b_str = entry_b.get().strip()
    c_str = entry_c.get().strip()

    if not a_str or not b_str or not c_str:
        messagebox.showwarning("Внимание", "Пожалуйста, заполните все три поля числами для сложения.")
        return

    try:
        a = float(a_str)
        b = float(b_str)
        c = float(c_str)
        result = a + b + c

        if result.is_integer():
            result_text = f"Результат: {int(result)}"
        else:
            result_text = f"Результат: {result:.4f}".rstrip('0').rstrip('.')

        label_result.config(text=result_text)
    except ValueError:
        messagebox.showerror("Ошибка", "Во всех полях должны быть корректные числа.")

def clear_fields():
    entry_a.delete(0, tk.END)
    entry_b.delete(0, tk.END)
    entry_c.delete(0, tk.END)
    label_result.config(text="Результат: ")

root = tk.Tk()
root.title("Калькулятор: сложение и умножение трёх чисел")
root.geometry("350x370")
root.resizable(False, False)

# Поля ввода
tk.Label(root, text="Число 1:").pack(pady=5)
entry_a = tk.Entry(root)
entry_a.pack(pady=3)

tk.Label(root, text="Число 2:").pack(pady=5)
entry_b = tk.Entry(root)
entry_b.pack(pady=3)

tk.Label(root, text="Число 3:").pack(pady=5)
entry_c = tk.Entry(root)
entry_c.pack(pady=3)

# Кнопки
btn_add = tk.Button(root, text="Сложить три числа (a + b + c)", command=add_three, bg="#ddffdd", font=("Arial", 10, "bold"))
btn_add.pack(pady=6)

btn_multiply = tk.Button(root, text="Умножить три числа (a * b * c)", command=multiply_three, bg="#ddddff", font=("Arial", 10, "bold"))
btn_multiply.pack(pady=6)

btn_clear = tk.Button(root, text="Очистить поля", command=clear_fields, bg="#ffe6e6", font=("Arial", 10))
btn_clear.pack(pady=6)

# Результат
label_result = tk.Label(root, text="Результат: ", font=("Arial", 12, "bold"), fg="#333333")
label_result.pack(pady=10)

root.mainloop()



