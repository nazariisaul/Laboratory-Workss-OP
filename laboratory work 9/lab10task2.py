# Лабораторна робота 10 Завдання 2

import random

# Введення розмірів
m = int(input("Введіть кількість рядків: "))
n = int(input("Введіть кількість стовпців: "))

# Створення масиву
a = []
i = 0
while i < m:
    row = []
    j = 0
    while j < n:
        row.append(random.randint(-10, 10))
        j += 1
    a.append(row)
    i += 1

# Вивід масиву
print("\nМасив:")
i = 0
while i < m:
    print(a[i])
    i += 1

# Перевірка кожного рядка
i = 0
while i < m:
    row = sorted(a[i])  # сортуємо рядок

    if n < 2:
        print("Рядок", i + 1, "- недостатньо елементів")
    else:
        d = row[1] - row[0]
        j = 2
        is_progression = True

        while j < n:
            if row[j] - row[j - 1] != d:
                is_progression = False
            j += 1

        if is_progression:
            print("Рядок", i + 1, "- можна побудувати арифметичну прогресію")
        else:
            print("Рядок", i + 1, "- не можна побудувати арифметичну прогресію")

    i += 1
