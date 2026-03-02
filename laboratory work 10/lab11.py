# Лабораторна робота 11

import random

# ====== Введення розмірів ======
l = int(input("Введіть кількість шарів (глибина l): "))
m = int(input("Введіть кількість рядків (m): "))
n = int(input("Введіть кількість стовпців (n): "))

#Створення 3D масиву
# Робимо золото рідким (менша ймовірність)
values = [0, 0, 0, 0, 1, 1, 2, 3, 4, 5, 6, 7]

mass = []

for k in range(l):
    layer = []
    for i in range(m):
        row = []
        for j in range(n):
            row.append(random.choice(values))
        layer.append(row)
    mass.append(layer)

#Пошук вертикального стовпця
max_gold = 0
best_i = 0
best_j = 0

for i in range(m):
    for j in range(n):
        gold_count = 0

        for k in range(l // 2):  # тільки верхня половина
            if mass[k][i][j] == 7:
                gold_count += 1

        if gold_count > max_gold:
            max_gold = gold_count
            best_i = i
            best_j = j

#Виведення результату
print("\nНайбільше золота у верхній половині шарів:")
print("Кількість золота:", max_gold)
print("Вертикальний стовпець: рядок =", best_i, ", стовпець =", best_j)