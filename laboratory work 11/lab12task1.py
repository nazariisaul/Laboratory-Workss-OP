# Лабораторна робота 12
# Завдання 1 (з ЛР10)

input_file = "input1.txt"
output_file = "output1.txt"

try:
    f = open(input_file, "r")
    data = f.read().split()
    f.close()

    if len(data) < 2:
        raise ValueError("Недостатньо даних для розмірів масиву")

    m = int(data[0])
    n = int(data[1])

    if m <= 0 or n <= 0:
        raise ValueError("Розміри масиву повинні бути більшими за нуль")

    numbers = data[2:]

    if len(numbers) != m * n:
        raise ValueError("Кількість елементів не відповідає розмірам масиву")

    a = []
    index = 0
    i = 0
    while i < m:
        row = []
        j = 0
        while j < n:
            num = int(numbers[index])
            if num < -1000 or num > 1000:
                raise ValueError("Елементи повинні бути в діапазоні [-1000; 1000]")
            row.append(num)
            index += 1
            j += 1
        a.append(row)
        i += 1

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

    out = open(output_file, "w")

    out.write("Масив:\n")
    i = 0
    while i < m:
        out.write(str(a[i]) + "\n")
        i += 1

    out.write("\nКількість рядків з нулем: " + str(rows_with_zero) + "\n")
    out.write("Кількість стовпців з нулем: " + str(cols_with_zero) + "\n")

    out.close()

except Exception as e:
    out = open(output_file, "w")
    out.write("Помилка: " + str(e))
    out.close()