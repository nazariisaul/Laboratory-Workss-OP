import random

# 1. Введення даних
m = int(input("Введіть кількість рядків: "))
n = int(input("Введіть кількість стовпців: "))

# 2. Генерація матриці
a = []
for i in range(m):
    row = [random.randint(1, 20) for _ in range(n)] # Створюємо рядок
    a.append(row)   # Додаємо рядок у матрицю

# Вивід масиву
print("\nЗгенерована матриця:")
for row in a:
    print(row)

# 3. Аналіз пар рядків
for i in range(m - 1):
    # Об'єднуємо та сортуємо від меншого до більшого
    combined = sorted(a[i] + a[i + 1])

    print(f"Пара рядків {i + 1} та {i + 2}: {combined}")

    # Визначаємо крок d між першим та другим елементом
    d = combined[1] - combined[0]

    is_progression = True
    # Перевіряємо сталість кроку d по всьому списку
    for k in range(len(combined) - 1):
        if combined[k + 1] - combined[k] != d: # Якщо хоча б одна пара чисел має іншу різницю
            is_progression = False  # Це не прогресія
            break

    # 4. Вивід результату
    if is_progression:
        if d == 0:
            print(f"   Це стаціонарна прогресія (всі числа однакові, d = 0)")
        else:
            print(f"   Це арифметична прогресія з кроком d = {d}")
    else:
        print(f"   Не є прогресією (різниця між числами змінюється)")
