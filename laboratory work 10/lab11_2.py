import random

# Введення розмірів
l = int(input("Введіть кількість шарів (глибина l): "))
m = int(input("Введіть кількість рядків (m): "))
n = int(input("Введіть кількість стовпців (n): "))

# Створення 3D масиву
values = [0, 0, 0, 0, 1, 1, 2, 3, 4, 5, 6, 7]
mass = []

for k in range(l):
    layer = []
    for i in range(m):
        row = [random.choice(values) for _ in range(n)]
        layer.append(row)
    mass.append(layer)

# Виведення масиву для перевірки
print("\nСТРУКТУРА ШАРІВ")
for k in range(l):
    print(f"Шар {k}:")
    for row in mass[k]:
        print(row)
    print("-" * 15)

# Пошук найкращого стовпця
mid = l // 2

max_gold_top = -1
best_top = (0, 0)

max_gold_bot = -1
best_bot = (0, 0)

for i in range(m):
    for j in range(n):
        # 1. Рахуємо золото (сімки) у верхній половині
        gold_top = 0
        for k in range(0, mid):
            if mass[k][i][j] == 7:
                gold_top += 1

        if gold_top > max_gold_top:
            max_gold_top = gold_top
            best_top = (i, j)

        # 2. Рахуємо золото (сімки) у нижній половині
        gold_bot = 0
        for k in range(mid, l):
            if mass[k][i][j] == 7:
                gold_bot += 1

        if gold_bot > max_gold_bot:
            max_gold_bot = gold_bot
            best_bot = (i, j)

# Виведення результату з розширеною умовою
print("\nАНАЛІЗ РЕЗУЛЬТАТІВ")

if max_gold_bot > max_gold_top:
    print(f"ПЕРЕМОЖЕЦЬ: Нижня половина шарів.")
    print(f"Там знайдено більше золота: {max_gold_bot} шт.")
    r_idx, c_idx = best_bot
elif max_gold_top > max_gold_bot:
    print(f"ПЕРЕМОЖЕЦЬ: Верхня половина шарів.")
    print(f"Там знайдено більше золота: {max_gold_top} шт.")
    r_idx, c_idx = best_top
else:
    # Випадок, коли max_gold_top == max_gold_bot
    print(f"РЕЗУЛЬТАТ: Нічия! В обох половинах однакова макс. кількість ({max_gold_top} шт).")
    print("За правилом пріоритету виводимо стовпець з верхньої половини.")
    r_idx, c_idx = best_top

print(f"Координати найкращого стовпця: рядок {r_idx}, стовпець {c_idx}")

# Вивід всього стовпця для візуалізації
print(f"\nСтовпець (ряд {r_idx}, стовп {c_idx}) у розрізі:")
for k in range(l):
    part = "ВЕРХ" if k < mid else "НИЗ "
    mark = "<-- золото!" if mass[k][r_idx][c_idx] == 7 else ""
    print(f"Шар {k} ({part}): {mass[k][r_idx][c_idx]} {mark}")