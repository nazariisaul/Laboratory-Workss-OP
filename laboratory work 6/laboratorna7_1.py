def check_square_corner(A, B):
    # Перевірка 1: центр квадрата
    if A == 0 and B == 0:
        return "Це центр квадрата, а не кут."

    # Перевірка 2: точка лежить на осі
    if A == 0 or B == 0:
        return "Точка лежить на осі координат і не є кутом квадрата."

    # Перевірка 3: умова кута квадрата |A| = |B|
    if abs(A) == abs(B):
        return "Так, ця точка є кутом квадрата з центром у (0, 0)."

    # Інший випадок
    return "Ні, ця точка не є кутом квадрата."


# приклади виклику
print(check_square_corner(3, 3))
print(check_square_corner(0, 5))
print(check_square_corner(2, -3))
