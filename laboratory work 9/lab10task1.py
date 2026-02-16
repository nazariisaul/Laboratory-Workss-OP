# Лабораторна робота 10 Завдання 1

import random

# Введення розмірів масиву
m = int(input("Введіть кількість рядків: "))
n = int(input("Введіть кількість стовпців: "))

# Створення двовимірного масиву
a = []
i = 0
while i < m:
    row = []
    j = 0
    while j < n:
        row.append(random.randint(-1000, 1000))
        j += 1
    a.append(row)
    i += 1

# Вивід масиву
print("\nМасив:")
i = 0
while i < m:
    print(a[i])
    i += 1

# Пошук рядків з нулем
rows_with_zero = 0
i = 0
while i < m:
    j = 0
    found = False
    while j < n:
        if a[i][j] == 0:
            found = True
        j += 1
    if found:
        rows_with_zero += 1
    i += 1

# Пошук стовпців з нулем
cols_with_zero = 0
j = 0
while j < n:
    i = 0
    found = False
    while i < m:
        if a[i][j] == 0:
            found = True
        i += 1
    if found:
        cols_with_zero += 1
    j += 1

print("\nКількість рядків з нулем:", rows_with_zero)
print("Кількість стовпців з нулем:", cols_with_zero)
