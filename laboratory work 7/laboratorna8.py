import random

class Product:
    # ЦІЛІ ЧИСЛА (int)
    price = 0
    weight = 0
    quantity = 0
    discount_percent = 0
    barcode = 0

    # ДРОБОВІ ЧИСЛА (float)
    rating = 0.0
    cost_price = 0.0
    markup = 0.0
    vat = 0.0
    final_price = 0.0

# ФУНКЦІЯ ВИВЕДЕННЯ
def print_product(p):
    print("Ціна:", p.price, "грн")
    print("Вага:", p.weight, "г")
    print("Кількість:", p.quantity)
    print("Знижка:", p.discount_percent, "%")
    print("Штрихкод:", p.barcode)
    print("Рейтинг:", p.rating)
    print("Собівартість:", p.cost_price)
    print("Націнка:", p.markup, "%")
    print("ПДВ:", p.vat, "%")
    print("Фінальна ціна:", p.final_price)
    print("-" * 30)

# ЕКЗЕМПЛЯРИ
p1 = Product()
p2 = Product()
p3 = Product()
p4 = Product()
p5 = Product()

# ЗАПОВНЕННЯ

# p1
p1.price = random.randint(50, 500)
p1.weight = random.randint(100, 1000)
p1.quantity = random.randint(0, 500)
p1.discount_percent = random.randint(0, 25)
p1.barcode = random.randint(1000000, 9999999)

p1.rating = random.randint(10, 50) / 10
p1.cost_price = random.randint(300, p1.price * 10) / 10
p1.markup = random.randint(10, 50)
p1.vat = 20.0
p1.final_price = p1.price * (1 - p1.discount_percent / 100)

# p2
p2.price = random.randint(50, 500)
p2.weight = random.randint(100, 1000)
p2.quantity = random.randint(0, 500)
p2.discount_percent = random.randint(0, 25)
p2.barcode = random.randint(1000000, 9999999)

p2.rating = random.randint(10, 50) / 10
p2.cost_price = random.randint(300, p2.price * 10) / 10
p2.markup = random.randint(10, 50)
p2.vat = 20.0
p2.final_price = p2.price * (1 - p2.discount_percent / 100)

# p3
p3.price = random.randint(50, 500)
p3.weight = random.randint(100, 1000)
p3.quantity = random.randint(0, 500)
p3.discount_percent = random.randint(0, 25)
p3.barcode = random.randint(1000000, 9999999)

p3.rating = random.randint(10, 50) / 10
p3.cost_price = random.randint(300, p3.price * 10) / 10
p3.markup = random.randint(10, 50)
p3.vat = 20.0
p3.final_price = p3.price * (1 - p3.discount_percent / 100)

# p4
p4.price = random.randint(50, 500)
p4.weight = random.randint(100, 1000)
p4.quantity = random.randint(0, 500)
p4.discount_percent = random.randint(0, 25)
p4.barcode = random.randint(1000000, 9999999)

p4.rating = random.randint(10, 50) / 10
p4.cost_price = random.randint(300, p4.price * 10) / 10
p4.markup = random.randint(10, 50)
p4.vat = 20.0
p4.final_price = p4.price * (1 - p4.discount_percent / 100)

# p5
p5.price = random.randint(50, 500)
p5.weight = random.randint(100, 1000)
p5.quantity = random.randint(0, 500)
p5.discount_percent = random.randint(0, 25)
p5.barcode = random.randint(1000000, 9999999)

p5.rating = random.randint(10, 50) / 10
p5.cost_price = random.randint(300, p5.price * 10) / 10
p5.markup = random.randint(10, 50)
p5.vat = 20.0
p5.final_price = p5.price * (1 - p5.discount_percent / 100)


# ВИВІД
print_product(p1)
print_product(p2)
print_product(p3)
print_product(p4)
print_product(p5)
