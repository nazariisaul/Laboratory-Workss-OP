def phone_info(a1, a2, a3, a4, a5, b1, b2, b3, b4, b5):
    # Формуємо номер
    number = f"{a1}{a2}{a3}{a4}{a5}{b1}{b2}{b3}{b4}{b5}"

    # Визначення оператора
    operator = ""
    if number.startswith("050") or number.startswith("095") or number.startswith("099"):
        operator = "Vodafone"

    if number.startswith("067") or number.startswith("068") or number.startswith("096") or number.startswith("097") or number.startswith("098"):
        operator = "Kyivstar"

    if number.startswith("063") or number.startswith("073") or number.startswith("093"):
        operator = "Lifecell"

    # Перевірка елітності
    elite = False
    if "000" in number or "111" in number or "222" in number or \
       "333" in number or "444" in number or "555" in number or \
       "666" in number or "777" in number or "888" in number or \
       "999" in number:
        elite = True

    # Результат
    return number, operator, elite


# приклади виклику
print(phone_info(0,5,0,1,2, 3,4,5,6,7))
print(phone_info(0,6,7,1,2, 3,3,3,4,4))
print(phone_info(0,9,9,1,1, 1,1,1,1,1))
