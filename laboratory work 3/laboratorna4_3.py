# Введення цифр числа A
a1 = int(input("Введіть a1: "))
a2 = int(input("Введіть a2: "))
a3 = int(input("Введіть a3: "))
a4 = int(input("Введіть a4: "))
a5 = int(input("Введіть a5: "))

# Введення цифр числа B
b1 = int(input("Введіть b1: "))
b2 = int(input("Введіть b2: "))
b3 = int(input("Введіть b3: "))
b4 = int(input("Введіть b4: "))
b5 = int(input("Введіть b5: "))

# Об'єднуємо всі цифри у єдиний номер
number = f"{a1}{a2}{a3}{a4}{a5}{b1}{b2}{b3}{b4}{b5}"

print("\nЗібраний номер телефону:", number)

# Перевірка оператора
operator = ""
if number.startswith("050") or number.startswith("095") or number.startswith("099"):
    operator = "Vodafone"
if number.startswith("067") or number.startswith("068") or number.startswith("096") or number.startswith("097") or number.startswith("098"):
    operator = "Kyivstar"
if number.startswith("063") or number.startswith("073") or number.startswith("093"):
    operator = "Lifecell"

if operator != "":
    print("Оператор мобільного зв’язку:", operator)
else:
    print("Номер не належить жодному відомому оператору України.")

# Перевірка елітності
elite = False

if "000" in number:
    elite = True
if "111" in number:
    elite = True
if "222" in number:
    elite = True
if "333" in number:
    elite = True
if "444" in number:
    elite = True
if "555" in number:
    elite = True
if "666" in number:
    elite = True
if "777" in number:
    elite = True
if "888" in number:
    elite = True
if "999" in number:
    elite = True

if elite:
    print("Номер є ЕЛІТНИМ")
else:
    print("Номер звичайний.")
