#----Товар----
class Product(object):
    name = "Raffaelo"                       # Назва продукту
    category = "Солодощі"                   # Категорія продукту
    price = 170                             # Ціна продукту
    brand = "Ferrero"                       # Бренд продукту
    weight = 150                            # Вага продукту
    expiry_date = "01.10.2025"              # Дата виробництва
    quantity = 500                          # Кількість продуктів
    barcode = "4740001"                     # Штрих-код
    supplier = "Raffaelo Ltd"               # Назва постачальника продукту
    discount = 2                            # Знижка на продукт
    country = "Італія"                      # Країна виробник продукту

    #----Екземпляри класу
p1 = Product()                              # Перший екземпляр класу Product
p2 = Product()                              # Другий екземпляр класу Product
p3 = Product()                              # Третій екземпляр класу Product

    #----Опис першого екземпляру класу Product
p1.name = "Молоко"
p1.category = "Молочні продукти"
p1.price = 38.5
p1.brand = "Яготинське"
p1.weight = 1.0
p1.expiry_date = "8.10.2025"
p1.quantity = 80
p1.barcode = "4820001"
p1.supplier = "Ферма Україна"
p1.discount = 5
p1.country = "Україна"

    #----Опис другого екземпляру класу Product
p2.name = "Сир"
p2.category = "Молочні продукти"
p2.price = 125
p2.brand = "Галичина"
p2.weight = 0.3
p2.expiry_date = "20.09.2025"
p2.quantity = 50
p2.barcode = "483001"
p2.supplier = "Молокозавод Львів"
p2.discount = 10
p2.country = "Україна"

    #----Опис третього екземпляру класу Product
p3.name = "Шоколад"
p3.category = "Солодощі"
p3.price = 268
p3.brand = "Milka"
p3.weight = 300
p3.expiry_date = "31.08.2025"
p3.quantity = 120
p3.barcode = "4510001"
p3.supplier = "Milka Ltd"
p3.discount = 0
p3.country = "Австрія"

    #----Виведення трьох екземплярів класу Product
print("Екземпляр p1 класу Product:")
print("Назва:", p1.name)
print("Категорія:", p1.category)
print("Ціна:", p1.price)
print("Бренд:", p1.brand)
print("Вага:", p1.weight)
print("Термін придатності:", p1.expiry_date)
print("Кількість:", p1.quantity)
print("Штрих-код:", p1.barcode)
print("Постачальник:", p1.supplier)
print("Знижка:", p1.discount, "%")
print("Країна виробник:", p1.country)

print()

print("Екземпляр p2 класу Product:")
print("Назва:", p2.name)
print("Категорія:", p2.category)
print("Ціна:", p2.price)
print("Бренд:", p2.brand)
print("Вага:", p2.weight)
print("Термін придатності:", p2.expiry_date)
print("Кількість:", p2.quantity)
print("Штрих-код:", p2.barcode)
print("Постачальник:", p2.supplier)
print("Знижка:", p2.discount, "%")
print("Країна виробник:", p2.country)

print()

print("Екземпляр p3 класу Product:")
print("Назва:", p3.name)
print("Категорія:", p3.category)
print("Ціна:", p3.price)
print("Бренд:", p3.brand)
print("Вага:", p3.weight)
print("Термін придатності:", p3.expiry_date)
print("Кількість:", p3.quantity)
print("Штрих-код:", p3.barcode)
print("Постачальник:", p3.supplier)
print("Знижка:", p3.discount, "%")
print("Країна виробник:", p3.country)

#----Покупець----
class Customer(object):
    name = "Петро"                          # Ім'я покупця
    age = 45                                # Вік покупця
    email = "petro45@ukr.net"               # Електрона адреса покупця
    phone = "+380976462583"                 # Номер телефону покупця
    card_number = "4849454683832365"        # Номер карточки покупця
    bonus_points = 125                      # Бонусні бали покупця
    address = "Вінниця вул. Шевченнка 12"   # Адреса проживання покупця
    gender = "Ч"                            # Стать покупця
    last_visited = "08.10.2025"             # Дата останього віддвідування
    total_purchases = 320                   # Загальна кількість покупок

    # ----Екземпляри класу
c1 = Customer()                         # Перший екземпляр класу Customer
c2 = Customer()                         # Другий екземпляр класу Customer
c3 = Customer()                         # Третій екземпляр класу Customer
    # ----Опис першого екземпляру класу Customer
c1.name = "Оксана"
c1.age =  32
c1.email = "oksana32@gmail.com"
c1.phone = "+380976433763"
c1.card_number = "4849443683552365"
c1.bonus_points = 340
c1.address = "Вінниця вул. Данила Галицького 5"
c1.gender = "Ж"
c1.last_visited = "09.10.2025"
c1.total_purchases = 451
    # ----Опис другого екземпляру класу Customer
c2.name = "Маріна"
c2.age =  19
c2.email = "marynam19@gmail.com"
c2.phone = "+380675433763"
c2.card_number = "4849576683552365"
c2.bonus_points = 0
c2.address = "Вінниця вул. Соборна 25"
c2.gender = "Ж"
c2.last_visited = "01.10.2025"
c2.total_purchases = 15
    # ----Опис третього екземпляру класу Customer
c3.name = "Микола"
c3.age =  20
c3.email = "mycolau2005@gmail.com"
c3.phone = "+380920433705"
c3.card_number = "4849420053552365"
c3.bonus_points = 10
c3.address = "Вінниця вул. Данила Галицького 5"
c3.gender = "Ж"
c3.last_visited = "20.09.2025"
c3.total_purchases = 57
    # ----Виведення трьох екземплярів класу Customer
print()
print()

print("Екземпляр c1 класу Customer:")
print("Покупець:",c1.name)
print("Вік:", c1.age)
print("E-mail:", c1.email)
print("Телефон:", c1.phone)
print("Картка:", c1.card_number)
print("Бонуси:", c1.bonus_points,)
print("Адреса:", c1.address)
print("Стать:", c1.gender)
print("Останій візит", c1.last_visited)
print("Загальні покупки", c1.total_purchases)

print()

print("Екземпляр c2 класу Customer:")
print("Покупець:",c2.name)
print("Вік:", c2.age)
print("E-mail:", c2.email)
print("Телефон:", c2.phone)
print("Картка:", c2.card_number)
print("Бонуси:", c2.bonus_points,)
print("Адреса:", c2.address)
print("Стать:", c2.gender)
print("Останій візит", c2.last_visited)
print("Загальні покупки", c2.total_purchases)

print()

print("Екземпляр c3 класу Customer:")
print("Покупець:",c3.name)
print("Вік:", c3.age)
print("E-mail:", c3.email)
print("Телефон:", c3.phone)
print("Картка:", c3.card_number)
print("Бонуси:", c3.bonus_points,)
print("Адреса:", c3.address)
print("Стать:", c3.gender)
print("Останій візит", c3.last_visited)
print("Загальні покупки", c1.total_purchases)

#----Працівник----
class Employee(object):
    name = "Анастасія"                     # Ім'я працівника
    position = "Касир"                     # Посада працівника
    salary = 15500                         # Зарплата пацівника
    experience = 5                         # Досвід працівника
    phone ="+38096238386"                  # Номер телефону працівника
    email ="anastasia.a@ukr.net"           # Електорона адреса працівника
    shift ="08:00-18:00"                   # Змінна в яку працює працвник
    id_number ="E025"                      # Номер ID
    hire_date ="02.09.2020"                # Дата прийому на роботу
    supervisor ="Олександр Сергійович"                # Керівник
    department ="Молочний відділ"          # Відділ в якому працює
    # ----Екземпляри класу
e1 = Employee()      # Перший екземпляр класу Employee
e2 = Employee()      # Другий екземпляр класу Employee
e3 = Employee()      # Третій екземпляр класу Employee
    # ----Опис першого екземпляру класу Employee
e1.name = "Олексій"
e1.position = "Охоронець"
e1.salary = 22300
e1.experience = 12
e1.phone = "+38065238386"
e1.email = "olexey.qw@gmail.com"
e1.shift = "20:00-08:00"
e1.id_number = "C106"
e1.hire_date = "30.04.2017"
e1.supervisor = "Андрій Миколайович"
e1.department = "Охорона"
    # ----Опис другого екземпляру класу Employee
e1.name = "Іванна"
e1.position = "Менеджер"
e1.salary = 25000
e1.experience = 8
e1.phone = "+38062837478"
e1.email = "ivanna.adm@ukr.net"
e1.shift = "09:00-17:00"
e1.id_number = "A006"
e1.hire_date = "22.02.2022"
e1.supervisor = "Микола Іванович"
e1.department = "Адміністрація"
    # ----Опис третього екземпляру класу Employee
e1.name = "Сергій"
e1.position = "Тех. підтримка"
e1.salary = 40000
e1.experience = 6
e1.phone = "+380963738123"
e1.email = "sergiy.teh@shop.ua"
e1.shift = "08:00-18:00"
e1.id_number = "T051"
e1.hire_date = "25.05.2024"
e1.supervisor = "Галина Михайлівна"
e1.department = "Сервісна служба"
    # ----Виведення трьох екземплярів класу Employee
print()
print()

print("Екземпляр e1 класу Employee:")
print("Працівник:", e1.name)
print("Посада:", e1.position)
print("Зарплата:", e1.salary, "грн.")
print("Досвід:", e1.experience, "років")
print("Телефон:", e1.phone)
print("E-mail:", e1.email)
print("Змінна:", e1.shift)
print("ID:", e1.id_number)
print("Дата прийому:", e1.hire_date)
print("Керівник:", e1.supervisor)
print("Відділ:", e1.department)

print()

print("Екземпляр e2 класу Employee:")
print("Працівник:", e2.name)
print("Посада:", e2.position)
print("Зарплата:", e2.salary, "грн.")
print("Досвід:", e2.experience, "років")
print("Телефон:", e2.phone)
print("E-mail:", e2.email)
print("Змінна:", e2.shift)
print("ID:", e2.id_number)
print("Дата прийому:", e2.hire_date)
print("Керівник:", e2.supervisor)
print("Відділ:", e2.department)

print()

print("Екземпляр e3 класу Employee:")
print("Працівник:", e3.name)
print("Посада:", e3.position)
print("Зарплата:", e3.salary, "грн.")
print("Досвід:", e3.experience, "років")
print("Телефон:", e3.phone)
print("E-mail:", e3.email)
print("Змінна:", e3.shift)
print("ID:", e3.id_number)
print("Дата прийому:", e3.hire_date)
print("Керівник:", e3.supervisor)
print("Відділ:", e3.department)

#----Касовий чек----

class Receipt(object):
    receipt_id = "R001"           # Номер чеку
    cashier = "Андрій"            # Касир
    items = ["Хліб", "Молоко"]    # Товари
    total = 60                    # Сума
    date = "05.10.2025"           # Дата
    time = "12:24"                # Час
    customer_name = "Ігор"        # Покупець
    payment_type = "Картка"       # Оплата
    vat = 20                      # ПДВ %
    discount = 5                  # Знижка
    final_sum = 57                # Фінальна сума

    # ----Екземпляри класу
r1 = Receipt()  # Перший екземпляр класу Receipt
r2 = Receipt()  # Другий екземпляр класу Receipt
r3 = Receipt()  # Третій екземпляр класу Receipt

    # ----Опис першого екземпляру класу Receipt
r1.receipt_id = "R002"
r1.cashier = "Ганна"
r1.items = ["Яблука", "Сік"]
r1.total = 80
r1.date = "09.10.2025"
r1.time = "20:54"
r1.customer_name = "Катерина"
r1.payment_type = "Готівка"
r1.vat = 20
r1.discount = 0
r1.final_sum = 80
    # ----Опис другого екземпляру класу Receipt
r2.receipt_id = "R005"
r2.cashier = "Петро"
r2.items = ["Кава","Сир"]
r2.total = 140
r2.date = "02.10.2025"
r2.time = "09:39"
r2.customer_name = "Мирослав"
r2.payment_type = "Картка"
r2.vat = 20
r2.discount = 10
r2.final_sum = 126
    # ----Опис третього екземпляру класу Receipt
r3.receipt_id = "R010"
r3.cashier = "Денис"
r3.items = ["Вино","Цукерки"]
r3.total = 160
r3.total = 190
r3.date = "10.10.2025"
r3.time = "19:04"
r3.customer_name = "Дмитро"
r3.payment_type = "Картка"
r3.vat = 20
r3.discount = 0
r3.final_sum = 190
    # ----Виведення трьох екземплярів класу Receipt
print()
print()
print("Екземпляр r1 класу Receipt:")
print("Чек №", r1.receipt_id)
print("Касир", r1.cashier)
print("Товари:", r1.items)
print("Сума:", r1.total, "грн.")
print("Дата:", r1.date)
print("Час:", r1.time)
print("Покупець:", r1.customer_name)
print("Оплата:", r1.payment_type)
print("ПДВ", r1.vat, "%")
print("Знижка:", r1.discount, "%")
print("До оплати:", r1.final_sum)

print()

print("Екземпляр r2 класу Receipt:")
print("Чек №", r2.receipt_id)
print("Касир", r2.cashier)
print("Товари:", r2.items)
print("Сума:", r2.total, "грн.")
print("Дата:", r2.date)
print("Час:", r2.time)
print("Покупець:", r2.customer_name)
print("Оплата:", r2.payment_type)
print("ПДВ", r2.vat, "%")
print("Знижка:", r2.discount, "%")
print("До оплати:", r2.final_sum)

print()

print("Екземпляр r3 класу Receipt:")
print("Чек №", r3.receipt_id)
print("Касир", r3.cashier)
print("Товари:", r3.items)
print("Сума:", r3.total, "грн.")
print("Дата:", r3.date)
print("Час:", r3.time)
print("Покупець:", r3.customer_name)
print("Оплата:", r3.payment_type)
print("ПДВ", r3.vat, "%")
print("Знижка:", r3.discount, "%")
print("До оплати:", r3.final_sum)


#----Відділ----
class Department(object):
    name = "М'ясний"                    # Назва відділу
    floor = 2                           # Поверх на якому знаходиться
    manager = "Михайло"                 # Менеджер відділу
    num_employees = 8                   # Кількість працівників
    num_products = 320                  # Кількість товарів
    area = 130                          # Площа відділу
    phone = "+380675354363"             # Номер телефону
    open_time = "08:00"                 # Час відкриття
    close_time = "22:00"                # Закриття відділу
    specialization = "М'ясні продукти"  # Спеціалізація відділу
    avg_daily_customers = 420           # Середня кількість покупців на день

 # ----Екземпляри класу
d1 = Department()  # Перший екземпляр класу Department
d2 = Department()  # Другий екземпляр класу Department
d3 = Department()  # Третій екземпляр класу Department

    # ----Опис першого екземпляру класу Department
d1.name = "Молочний"
d1.floor = 1
d1.manager = "Анна"
d1.num_employees = 6
d1.num_products = 250
d1.area = 120
d1.phone = "+380675334363"
d1.open_time = "09:00"
d1.close_time = "21:00"
d1.specialization = "Молочні продукти"
d1.avg_daily_customers = 500
    # ----Опис другого екземпляру класу Department
d2.name = ""
d2.floor = 1
d2.manager = "Ірина"
d2.num_employees = 5
d2.num_products = 100
d2.area = 100
d2.phone = "+380675354398"
d2.open_time = "8:00"
d2.close_time = "22:00"
d2.specialization = "Овочі та фрукти"
d2.avg_daily_customers = 450
    # ----Опис третього екземпляру класу Department
d3.name = ""
d3.floor = 2
d3.manager = "Олег"
d3.num_employees = 7
d3.num_products = 400
d3.area = 150
d3.phone = "+3806753523463"
d3.open_time = "8:00"
d3.close_time = "21:00"
d3.specialization = "Сухі продукти"
d3.avg_daily_customers = 600
    # ----Виведення трьох екземплярів класу Department

print()
print()

print("Екземпляр d1 класу Department:")
print("Відділ:", d1.name)
print("Поверх:",d1.floor)
print("Менеджер:",d1.manager)
print("Працівників:",d1.num_employees)
print("Товарів:",d1.num_products)
print("Площа",d1.area, "м²")
print("Телефон:",d1.phone)
print("Відчиняється:",d1.open_time)
print("Зачиняється:",d1.close_time)
print("Спеціалізація:",d1.specialization)
print("Середньоденна кількість покупців:",d1.avg_daily_customers)

print()
print("Екземпляр d2 класу Department:")
print("Відділ:", d2.name)
print("Поверх:",d2.floor)
print("Менеджер:",d2.manager)
print("Працівників:",d2.num_employees)
print("Товарів:",d2.num_products)
print("Площа",d2.area, "м²")
print("Телефон:",d2.phone)
print("Відчиняється:",d2.open_time)
print("Зачиняється:",d2.close_time)
print("Спеціалізація:",d2.specialization)
print("Середньоденна кількість покупців:",d2.avg_daily_customers)

print()

print("Екземпляр d3 класу Department:")
print("Відділ:", d3.name)
print("Поверх:",d3.floor)
print("Менеджер:",d3.manager)
print("Працівників:",d3.num_employees)
print("Товарів:",d3.num_products)
print("Площа",d3.area, "м²")
print("Телефон:",d3.phone)
print("Відчиняється:",d3.open_time)
print("Зачиняється:",d3.close_time)
print("Спеціалізація:",d3.specialization)
print("Середньоденна кількість покупців:",d3.avg_daily_customers)