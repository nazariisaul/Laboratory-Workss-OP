def distance_to_line(x, y, a, b, c):

    # крок 1: обчислюємо вираз
    value = a*x + b*y + c

    # крок 2: модуль
    if value < 0:
        value = -value

    # крок 3: обчислюємо a^2 + b^2
    square_sum = a*a + b*b

    # крок 4: корінь квадратний
    root = square_sum ** 0.5

    # крок 5: ділимо
    distance = value / root

    # крок 6: повертаємо результат
    return distance

# з перевіркою:

# приклади виклику:
print(distance_to_line(3, 4, 2, -1, -1))
print(distance_to_line(0, 2, 1, 2, -3))
print(distance_to_line(x=1, y=5, a=3, b=4, c=-10))

def distance_to_line(x, y, a, b, c):
    # --- Внутрішні перевірки та нотифікації ---

    # 1. Перевірка на некоректність прямої (a=0 та b=0)
    if a == 0 and b == 0:
        print("\nПОМИЛКА: Коефіцієнти a та b не можуть бути одночасно нульовими (це не рівняння прямої).")
        return None

    # 2. Перевірка, чи пряма проходить через початок координат (0, 0)
    # Пряма проходить через (0, 0), якщо a*0 + b*0 + c = 0, тобто c = 0.
    if c == 0:
        print(f"\nПРИМІТКА: Пряма",a,"x + ", b,"y = 0 проходить через початок координат (0, 0).")

    # 3. Перевірка, чи пряма є віссю OX (y = 0)
    if a == 0 and b != 0 and c == 0:
        print(f"\nПРИМІТКА: Пряма є віссю OX (y = 0).")

    # 4. Перевірка, чи пряма є віссю OY (x = 0)
    elif b == 0 and a != 0 and c == 0:
        print(f"\nПРИМІТКА: Пряма є віссю OY (x = 0).")

    # --- Обчислення відстані (без імпорту) ---

    # Крок 1: Обчислюємо чисельник (вираз ax + by + c)
    value = a * x + b * y + c

    # Крок 2: Модуль чисельника (використовуємо вбудовану функцію abs)
    numerator = abs(value)

    # Крок 3: Обчислюємо a^2 + b^2
    square_sum = a * a + b * b

    # Крок 4: Корінь квадратний (знаменник)
    # Використовуємо ** 0.5 для добування кореня
    denominator = square_sum ** 0.5

    # Крок 5: Ділимо
    distance = numerator / denominator

    # Крок 6: Повертаємо результат
    return distance

print("1 варіант")
print(distance_to_line(0, 2, 0, 4, 0))
print()
print()
print("2 варіант")
print(distance_to_line(0, 2, 5, 0, 0))
print()
print()
print("3 варіант")
print(distance_to_line(0, 2, 5, 5, 0))
print()
print()
print("4 варіант")
print(distance_to_line(0, 2, 5, 5, 4))
