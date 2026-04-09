from tkinter import *

root = Tk()
root.title("Помічник збирача меблів v1.0")
root.geometry("700x550")

# --- Глобальні змінні ---
mebel_type = 0  # 1-Шафа, 2-Ліжко, 3-Кухня, 4-Стіл, 5-Комод

# Базові ціни за збірку
p1, p2, p3, p4, p5 = 800, 600, 2500, 400, 500

# Додаткові коефіцієнти/ціни
floor_price = 150
urgent_ratio = 1.5
tools_price = 200

# Розміри вікна
current_width = 700
current_height = 550

# Розміри шрифтів
font_size = 10
title_font_size = 12
result_font_size = 12


# --- Функції ---
def select_mebel(m_type):
    global mebel_type
    mebel_type = m_type


def show_info():
    s = ""

    if mebel_type == 0:
        s = "Оберіть тип меблів для розрахунку!"
    else:
        names = {
            1: ("Шафа", p1),
            2: ("Ліжко", p2),
            3: ("Кухня", p3),
            4: ("Стіл", p4),
            5: ("Комод", p5)
        }

        name, base_price = names[mebel_type]

        s = f"Обрано: {name}\n"
        s += f"Базова ціна: {base_price} грн\n"

        if var_r1.get() == 1:
            s += "Складність: Стандарт (+0 грн)\n"
        else:
            extra_complexity = int(base_price * 0.3)
            s += f"Складність: Ексклюзив (+{extra_complexity} грн)\n"

        if var_c1.get() == 1:
            s += f"Поверховий підйом (+{floor_price} грн)\n"

        if var_c2.get() == 1:
            s += f"Свої витратні матеріали (+{tools_price} грн)\n"

        if var_c3.get() == 1:
            urgent_extra = int(base_price * (urgent_ratio - 1))
            s += f"Терміново (сьогодні) (+{urgent_extra} грн)\n"

    result_text.set(s)


def calculate(event):
    show_info()

    if mebel_type == 0:
        return

    prices = {1: p1, 2: p2, 3: p3, 4: p4, 5: p5}
    total = prices[mebel_type]

    if var_r1.get() == 2:
        total *= 1.3

    if var_c1.get() == 1:
        total += floor_price

    if var_c2.get() == 1:
        total += tools_price

    if var_c3.get() == 1:
        total *= urgent_ratio

    current_s = result_text.get()
    result_text.set(current_s + f"\n\nРазом до сплати: {int(total)} грн.")


def about(event):
    result_text.set(
        "Лабораторна робота №13\n"
        "Професія: Збирач меблів\n"
        "Виконав: Сауляк Н."
    )


def update_fonts():
    title_label.config(font=("Arial", title_font_size, "bold"))

    for b in [b1, b2, b3, b4, b5]:
        b.config(font=("Arial", font_size))

    r1.config(font=("Arial", font_size))
    r2.config(font=("Arial", font_size))

    c1.config(font=("Arial", font_size))
    c2.config(font=("Arial", font_size))
    c3.config(font=("Arial", font_size))

    btn_calc.config(font=("Arial", title_font_size, "bold"))
    btn_about.config(font=("Arial", font_size))
    btn_zoom_in.config(font=("Arial", font_size))
    btn_zoom_out.config(font=("Arial", font_size))

    complexity_label.config(font=("Arial", font_size, "bold"))
    l5.config(font=("Courier", result_font_size, "bold"))


def zoom_in():
    global current_width, current_height
    global font_size, title_font_size, result_font_size

    current_width += 50
    current_height += 40
    root.geometry(f"{current_width}x{current_height}")

    font_size += 1
    title_font_size += 1
    result_font_size += 1
    update_fonts()


def zoom_out():
    global current_width, current_height
    global font_size, title_font_size, result_font_size

    if current_width > 400 and current_height > 300:
        current_width -= 50
        current_height -= 40
        root.geometry(f"{current_width}x{current_height}")

        if font_size > 8:
            font_size -= 1
            title_font_size -= 1
            result_font_size -= 1
            update_fonts()


# --- Інтерфейс (Віджети) ---

# l1 - Ліва панель (Вибір меблів)
l1 = Label(root, bg="saddle brown", padx=10, pady=10)
l1.pack(side=LEFT, expand=1, fill=BOTH)

title_label = Label(
    l1,
    text="ТИП МЕБЛІВ",
    fg="white",
    bg="saddle brown",
    font=("Arial", title_font_size, "bold")
)
title_label.pack(pady=10)

b1 = Button(l1, text="Шафа", bg="burlywood", command=lambda: select_mebel(1))
b2 = Button(l1, text="Ліжко", bg="burlywood", command=lambda: select_mebel(2))
b3 = Button(l1, text="Кухня", bg="burlywood", command=lambda: select_mebel(3))
b4 = Button(l1, text="Стіл", bg="burlywood", command=lambda: select_mebel(4))
b5 = Button(l1, text="Комод", bg="burlywood", command=lambda: select_mebel(5))

for b in [b1, b2, b3, b4, b5]:
    b.pack(side=TOP, expand=1, fill=BOTH, pady=2)

# Права частина вікна
l2 = Label(root, bg="peru")
l3 = Label(root, bg="tan")
l4 = Label(root, bg="gray80")

result_text = StringVar()

l5 = Label(
    root,
    textvariable=result_text,
    bg="white",
    font=("Courier", result_font_size, "bold"),
    height=12,
    width=40,
    anchor="nw",
    justify=LEFT,
    padx=10,
    pady=10
)

l2.pack(side=TOP, expand=1, fill=BOTH)
l3.pack(side=TOP, expand=1, fill=BOTH)
l5.pack(side=TOP, expand=1, fill=BOTH)
l4.pack(side=TOP, expand=1, fill=BOTH)

# Віджети для l2
complexity_label = Label(
    l2,
    text="Складність конструкції:",
    bg="peru",
    font=("Arial", font_size, "bold")
)
complexity_label.pack(side=LEFT, padx=5)

var_r1 = IntVar()
var_r1.set(1)

r1 = Radiobutton(l2, text="Стандарт", variable=var_r1, value=1, bg="peru")
r2 = Radiobutton(l2, text="Ексклюзив", variable=var_r1, value=2, bg="peru")

r1.pack(side=LEFT, expand=1)
r2.pack(side=LEFT, expand=1)

# Віджети для l3
var_c1 = IntVar()
var_c2 = IntVar()
var_c3 = IntVar()

c1 = Checkbutton(l3, text="Поверховий підйом", variable=var_c1, bg="tan")
c2 = Checkbutton(l3, text="Свої витратні матеріали", variable=var_c2, bg="tan")
c3 = Checkbutton(l3, text="Терміново (сьогодні)", variable=var_c3, bg="tan", fg="red")

c1.pack(side=LEFT, expand=1)
c2.pack(side=LEFT, expand=1)
c3.pack(side=LEFT, expand=1)

# Віджети для l4
btn_calc = Button(l4, text="РОЗРАХУВАТИ ВАРТІСТЬ", bg="orange")
btn_calc.bind("<Button-1>", calculate)
btn_calc.pack(side=LEFT, expand=1, fill=BOTH)

btn_about = Button(l4, text="?", bg="gray70", width=3)
btn_about.bind("<Button-1>", about)
btn_about.pack(side=LEFT, fill=Y)

btn_zoom_in = Button(l4, text="+", bg="lightgreen", width=3, command=zoom_in)
btn_zoom_in.pack(side=LEFT, fill=Y)

btn_zoom_out = Button(l4, text="-", bg="tomato", width=3, command=zoom_out)
btn_zoom_out.pack(side=LEFT, fill=Y)

# Початкове оновлення шрифтів
update_fonts()

root.mainloop()