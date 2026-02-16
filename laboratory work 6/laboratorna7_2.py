def count_repeated(x1, x2, x3, x4, x5):
    count = 0

    # Перевіряємо, чи x1 повторюється
    if x1 == x2 or x1 == x3 or x1 == x4 or x1 == x5:
        count += 1

    # Для x2
    if x2 == x3 or x2 == x4 or x2 == x5:
        count += 1

    # Для x3
    if x3 == x4 or x3 == x5:
        count += 1

    # Для x4
    if x4 == x5:
        count += 1

    return count


# приклади виклику
print(count_repeated(1, 2, 3, 2, 5))
print(count_repeated(7, 7, 7, 7, 7))
print(count_repeated(1, 2, 3, 4, 5))
