# Лабораторна робота 12
# Завдання 2 (з ЛР10)

input_file = "input2.txt"
output_file = "output2.txt"

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

    out = open(output_file, "w")

    out.write("Масив:\n")
    i = 0
    while i < m:
        out.write(str(a[i]) + "\n")
        i += 1

    i = 0
    while i < m:
        row = sorted(a[i])

        if n < 2:
            out.write("Рядок " + str(i + 1) + " - недостатньо елементів\n")
        else:
            d = row[1] - row[0]
            j = 2
            is_progression = True

            while j < n:
                if row[j] - row[j - 1] != d:
                    is_progression = False
                j += 1

            if is_progression:
                out.write("Рядок " + str(i + 1) +
                          " - можна побудувати арифметичну прогресію\n")
            else:
                out.write("Рядок " + str(i + 1) +
                          " - не можна побудувати арифметичну прогресію\n")

        i += 1

    out.close()

except Exception as e:
    out = open(output_file, "w")
    out.write("Помилка: " + str(e))
    out.close()