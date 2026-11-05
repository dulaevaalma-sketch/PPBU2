def save_to_history(operation, result):
    # Записывает операцию в файл history.txt
    with open('history.txt', 'a', encoding='utf-8') as file:
        file.write(f'✏️ Результат: {operation} = {result}\n')


def view_history():
    # Читает историю из файла и выводит её пользователю
    try:
        with open('history.txt', 'r', encoding='utf-8') as file:
            history = file.read()
            if not history.strip():
                return "📜 История пуста"
            return history
    except FileNotFoundError:
        return "❌ Файл истории не найден"
    except Exception as e:
        return f"🚫 Ошибка при чтении файла: {e}"


def calculate(num1, num2, operation):
    # Выполняет арифметическую операцию
    match operation:
        case '+':
            return num1 + num2
        case '-':
            return num1 - num2
        case '*':
            return num1 * num2
        case '/':
            if num2 == 0:
                return "Ошибка! Деление на ноль."
            return round(num1 / num2, 2)

    return "Ошибка! Неверная операция."


# Основной цикл программы
while True:
    print("\nВыберите операцию:")
    print("1. Сложение")
    print("2. Вычитание")
    print("3. Умножение")
    print("4. Деление")
    print("5. Просмотр истории вычислений")
    print("6. Выход")

    choice = input("Введите номер операции (1/2/3/4/5/6): ").strip()

    # Обработка выхода или просмотра истории
    if choice == '6':
        print("До свидания!")
        break
    elif choice == '5':
        print(view_history())
        continue

    # Проверка корректности выбора
    operations = {'1': '+', '2': '-', '3': '*', '4': '/'}
    if choice not in operations:
        print("Неверный выбор.")
        continue

    # Получаем числа от пользователя
    try:
        num1 = float(input("Введите первое число: "))
        num2 = float(input("Введите второе число: "))
    except ValueError:
        print("Ошибка! Нужно ввести число.")
        continue

    # Определяем выбранную операцию
    op = operations[choice]
    result = calculate(num1, num2, op)

    # Выводим результат и сохраняем его в историю
    if isinstance(result, str) and result.startswith("Ошибка"):
        print(result)
    else:
        expression = f"{num1} {op} {num2}"
        print(f"✍️ Результат: {expression} = {result}")
        save_to_history(expression, result)