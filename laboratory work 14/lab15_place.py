from tkinter import *
from tkinter import messagebox

# --- Глобальні змінні ---
prices_dict = {"Шафа": 800, "Ліжко": 600, "Кухня": 2500, "Стіл": 400, "Комод": 500}
floor_price_per_one = 150
urgent_ratio = 1.5
tools_price = 200

# Початкові налаштування
current_width, current_height = 850, 650
font_size, title_font_size, result_font_size = 10, 12, 12

# --- Функції ---

def update_fonts():
    """Оновлення шрифтів для всіх віджетів (Зум)"""
    title_label.config(font=("Arial", title_font_size, "bold"))
    listbox.config(font=("Arial", font_size))
    ent_name.config(font=("Arial", font_size))
    name_label.config(font=("Arial", font_size))
    complexity_label.config(font=("Arial", font_size, "bold"))
    r1.config(font=("Arial", font_size))
    r2.config(font=("Arial", font_size))
    c1.config(font=("Arial", font_size))
    c2.config(font=("Arial", font_size))
    c3.config(font=("Arial", font_size))
    scale_floor.config(font=("Arial", font_size))
    spin_label.config(font=("Arial", font_size))
    spin_count.config(font=("Arial", font_size))
    btn_calc.config(font=("Arial", title_font_size, "bold"))
    l5.config(font=("Courier", result_font_size, "bold"))

def zoom_in():
    global current_width, current_height, font_size, title_font_size, result_font_size
    current_width += 50; current_height += 40
    root.geometry(f"{current_width}x{current_height}")
    font_size += 1; title_font_size += 1; result_font_size += 1
    update_fonts()

def zoom_out():
    global current_width, current_height, font_size, title_font_size, result_font_size
    if current_width > 500:
        current_width -= 50; current_height -= 40
        root.geometry(f"{current_width}x{current_height}")
        font_size -= 1; title_font_size -= 1; result_font_size -= 1
        update_fonts()

def calculate(event=None):
    selection = listbox.curselection()
    if not selection:
        result_text.set("Оберіть тип меблів у списку!")
        return

    m_name = listbox.get(selection[0])
    base_price = prices_dict[m_name]
    client = ent_name.get() if ent_name.get() else "Клієнт"

    s = f"Замовник: {client}\nОбрано: {m_name} ({base_price} грн)\n"
    total = base_price

    if var_r1.get() == 2:
        extra = int(base_price * 0.3)
        total += extra
        s += f"Складність: Ексклюзив (+{extra} грн)\n"
    else:
        s += "Складність: Стандарт (+0 грн)\n"

    if var_c1.get() == 1:
        floors = scale_floor.get()
        f_total = floors * floor_price_per_one
        total += f_total
        s += f"Підйом на {floors} пов. (+{f_total} грн)\n"

    if var_c2.get() == 1:
        total += tools_price
        s += f"Витратні матеріали (+{tools_price} грн)\n"

    if var_c3.get() == 1:
        u_extra = int(base_price * (urgent_ratio - 1))
        total += u_extra
        s += f"Терміновість (+{u_extra} грн)\n"

    count = int(spin_count.get())
    total *= count
    result_text.set(s + f"\nКількість: {count} шт.\n" + "=" * 25 + f"\nРАЗОМ: {int(total)} грн.")

def about(event=None):
    result_text.set("ЛР №15\nПозиціонування: PLACE\nВиконав: Сауляк Н.")

# --- Інтерфейс ---

root = Tk()
root.title("Помічник меблевика v2.0 (Метод PLACE)")
root.geometry(f"{current_width}x{current_height}")

# 1. Ліва панель (Frame f1)
f1 = Frame(root, bg="saddle brown")
f1.place(x=0, y=0, width=220, relheight=0.92)

title_label = Label(f1, text="ТИП МЕБЛІВ", fg="white", bg="saddle brown")
title_label.place(relx=0.5, y=20, anchor=CENTER)

listbox = Listbox(f1, exportselection=0)
for item in prices_dict.keys():
    listbox.insert(END, item)
listbox.place(x=20, y=50, width=180, height=180)

name_label = Label(f1, text="Ім'я клієнта:", fg="white", bg="saddle brown")
name_label.place(x=20, y=250)
ent_name = Entry(f1)
ent_name.place(x=20, y=275, width=180)

# 2. Верхня панель - Складність (Frame f2)
f2 = Frame(root, bg="peru")
f2.place(x=220, y=0, relwidth=1.0, height=60)

complexity_label = Label(f2, text="Складність:", bg="peru")
complexity_label.place(x=20, y=20)

var_r1 = IntVar(value=1)
r1 = Radiobutton(f2, text="Стандарт", variable=var_r1, value=1, bg="peru")
r2 = Radiobutton(f2, text="Ексклюзив", variable=var_r1, value=2, bg="peru")
r1.place(x=120, y=20)
r2.place(x=230, y=20)

# 3. Центральна панель - Опції (Frame f3)
f3 = Frame(root, bg="tan")
f3.place(x=220, y=60, relwidth=1.0, height=130)

var_c1, var_c2, var_c3 = IntVar(), IntVar(), IntVar()
c1 = Checkbutton(f3, text="Підйом", variable=var_c1, bg="tan")
c2 = Checkbutton(f3, text="Матеріали", variable=var_c2, bg="tan")
c3 = Checkbutton(f3, text="Терміново", variable=var_c3, bg="tan", fg="red")
c1.place(x=20, y=10)
c2.place(x=20, y=40)
c3.place(x=20, y=70)

scale_floor = Scale(f3, from_=1, to=20, orient=HORIZONTAL, label="Поверх", bg="tan")
scale_floor.place(x=150, y=15, width=200)

# 4. Додаткова панель - Кількість (Frame f_extra)
f_extra = Frame(root, bg="gray90")
f_extra.place(x=220, y=190, relwidth=1.0, height=50)

spin_label = Label(f_extra, text="Кількість комплектів:", bg="gray90")
spin_label.place(x=20, y=15)
spin_count = Spinbox(f_extra, from_=1, to=50, width=5)
spin_count.place(x=180, y=15)

# 5. Результат (Label l5)
result_text = StringVar(value="Оберіть параметри та натисніть Розрахувати")
l5 = Label(root, textvariable=result_text, bg="white", anchor="nw", justify=LEFT, padx=15, pady=15, relief=SUNKEN)
l5.place(x=240, y=260, relwidth=0.68, relheight=0.55)

# 6. Нижня панель кнопок (Frame f4)
f4 = Frame(root, bg="gray80")
f4.place(x=0, rely=0.92, relwidth=1.0, relheight=0.08)

btn_calc = Button(f4, text="РОЗРАХУВАТИ", bg="orange", command=calculate)
btn_calc.place(x=0, y=0, relwidth=0.6, relheight=1.0)

btn_about = Button(f4, text="?", command=about)
btn_about.place(relx=0.6, y=0, relwidth=0.1, relheight=1.0)

btn_zoom_in = Button(f4, text="+", bg="lightgreen", command=zoom_in)
btn_zoom_in.place(relx=0.7, y=0, relwidth=0.15, relheight=1.0)

btn_zoom_out = Button(f4, text="-", bg="tomato", command=zoom_out)
btn_zoom_out.place(relx=0.85, y=0, relwidth=0.15, relheight=1.0)

update_fonts()
root.mainloop()