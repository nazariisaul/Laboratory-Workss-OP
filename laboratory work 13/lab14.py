from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Помічник збирача меблів v2.0")
root.geometry("850x650")

# --- Глобальні змінні ---
prices_dict = {"Шафа": 800, "Ліжко": 600, "Кухня": 2500, "Стіл": 400, "Комод": 500}
floor_price_per_one = 150
urgent_ratio = 1.5
tools_price = 200

# Розміри та шрифти
current_width, current_height = 850, 650
font_size, title_font_size, result_font_size = 10, 12, 12


# --- Функції ---

def update_fonts():
    """Оновлення шрифтів для всіх віджетів (Зум)"""
    title_label.config(font=("Arial", title_font_size, "bold"))
    listbox.config(font=("Arial", font_size))
    ent_name.config(font=("Arial", font_size))
    name_label.config(font=("Arial", font_size))

    r1.config(font=("Arial", font_size))
    r2.config(font=("Arial", font_size))
    complexity_label.config(font=("Arial", font_size, "bold"))

    c1.config(font=("Arial", font_size))
    c2.config(font=("Arial", font_size))
    c3.config(font=("Arial", font_size))
    scale_floor.config(font=("Arial", font_size))

    spin_label.config(font=("Arial", font_size))
    spin_count.config(font=("Arial", font_size))

    btn_calc.config(font=("Arial", title_font_size, "bold"))
    btn_about.config(font=("Arial", font_size))
    btn_zoom_in.config(font=("Arial", font_size))
    btn_zoom_out.config(font=("Arial", font_size))
    l5.config(font=("Courier", result_font_size, "bold"))


def zoom_in():
    global current_width, current_height, font_size, title_font_size, result_font_size
    current_width += 50
    current_height += 40
    root.geometry(f"{current_width}x{current_height}")
    font_size += 1;
    title_font_size += 1;
    result_font_size += 1
    update_fonts()


def zoom_out():
    global current_width, current_height, font_size, title_font_size, result_font_size
    if current_width > 500:
        current_width -= 50;
        current_height -= 40
        root.geometry(f"{current_width}x{current_height}")
        font_size -= 1;
        title_font_size -= 1;
        result_font_size -= 1
        update_fonts()


def calculate(event=None):
    # Отримання вибору з Listbox
    selection = listbox.curselection()
    if not selection:
        result_text.set("Оберіть тип меблів у списку!")
        return

    m_name = listbox.get(selection[0])
    base_price = prices_dict[m_name]
    client = ent_name.get() if ent_name.get() else "Клієнт"

    # Початковий текст
    s = f"Замовник: {client}\n"
    s += f"Обрано: {m_name} ({base_price} грн)\n"

    total = base_price

    # Складність
    if var_r1.get() == 2:
        extra = int(base_price * 0.3)
        total += extra
        s += f"Складність: Ексклюзив (+{extra} грн)\n"
    else:
        s += "Складність: Стандарт (+0 грн)\n"

    # Поверхи (Scale)
    if var_c1.get() == 1:
        floors = scale_floor.get()
        f_total = floors * floor_price_per_one
        total += f_total
        s += f"Підйом на {floors} пов. (+{f_total} грн)\n"

    # Матеріали
    if var_c2.get() == 1:
        total += tools_price
        s += f"Витратні матеріали (+{tools_price} грн)\n"

    # Терміновість
    if var_c3.get() == 1:
        u_extra = int(base_price * (urgent_ratio - 1))
        total += u_extra
        s += f"Терміновість (+{u_extra} грн)\n"

    # Кількість (Spinbox)
    count = int(spin_count.get())
    total *= count

    result_text.set(s + f"\nКількість: {count} шт.\n" + "=" * 20 + f"\nРАЗОМ: {int(total)} грн.")


def about(event=None):
    result_text.set("Лабораторна робота №14\nВикористання Frame, Listbox, Entry, Scale, Spinbox\nВиконав: Сауляк Н.")


# --- Інтерфейс (Frame) ---

# f1 - Ліва панель
f1 = Frame(root, bg="saddle brown", padx=10, pady=10)
f1.pack(side=LEFT, fill=Y)

title_label = Label(f1, text="ТИП МЕБЛІВ", fg="white", bg="saddle brown")
title_label.pack(pady=5)

listbox = Listbox(f1, height=8, exportselection=0)
for item in prices_dict.keys():
    listbox.insert(END, item)
listbox.pack(pady=5, fill=X)

name_label = Label(f1, text="Ім'я клієнта:", fg="white", bg="saddle brown")
name_label.pack(pady=(10, 0))
ent_name = Entry(f1)
ent_name.pack(pady=5, fill=X)

# f2 - Складність (Radio)
f2 = Frame(root, bg="peru", padx=10, pady=5)
f2.pack(side=TOP, fill=X)
complexity_label = Label(f2, text="Складність:", bg="peru")
complexity_label.pack(side=LEFT)
var_r1 = IntVar(value=1)
r1 = Radiobutton(f2, text="Стандарт", variable=var_r1, value=1, bg="peru")
r2 = Radiobutton(f2, text="Ексклюзив", variable=var_r1, value=2, bg="peru")
r1.pack(side=LEFT, padx=10);
r2.pack(side=LEFT)

# f3 - Опції та Scale
f3 = Frame(root, bg="tan", padx=10, pady=5)
f3.pack(side=TOP, fill=X)
var_c1, var_c2, var_c3 = IntVar(), IntVar(), IntVar()
c1 = Checkbutton(f3, text="Підйом", variable=var_c1, bg="tan")
c2 = Checkbutton(f3, text="Матеріали", variable=var_c2, bg="tan")
c3 = Checkbutton(f3, text="Терміново", variable=var_c3, bg="tan", fg="red")
c1.grid(row=0, column=0, sticky=W);
c2.grid(row=1, column=0, sticky=W);
c3.grid(row=2, column=0, sticky=W)

scale_floor = Scale(f3, from_=1, to=20, orient=HORIZONTAL, label="Оберіть поверх", bg="tan", length=200)
scale_floor.grid(row=0, column=1, rowspan=3, padx=20)

# f_extra - Spinbox (Новий функціонал)
f_extra = Frame(root, bg="gray90", padx=10, pady=5)
f_extra.pack(side=TOP, fill=X)
spin_label = Label(f_extra, text="Кількість комплектів:", bg="gray90")
spin_label.pack(side=LEFT)
spin_count = Spinbox(f_extra, from_=1, to=50, width=5)
spin_count.pack(side=LEFT, padx=10)

# f5 - Результат
result_text = StringVar(value="Оберіть параметри...")
l5 = Label(root, textvariable=result_text, bg="white", anchor="nw", justify=LEFT, padx=10, pady=10, relief=SUNKEN)
l5.pack(side=TOP, expand=1, fill=BOTH, padx=10, pady=10)

# f4 - Кнопки
f4 = Frame(root, bg="gray80")
f4.pack(side=BOTTOM, fill=X)

btn_calc = Button(f4, text="РОЗРАХУВАТИ", bg="orange", command=calculate)
btn_calc.pack(side=LEFT, expand=1, fill=BOTH)

btn_about = Button(f4, text="?", bg="gray70", width=3, command=about)
btn_about.pack(side=LEFT, fill=Y)

btn_zoom_in = Button(f4, text="+", bg="lightgreen", width=3, command=zoom_in)
btn_zoom_in.pack(side=LEFT, fill=Y)

btn_zoom_out = Button(f4, text="-", bg="tomato", width=3, command=zoom_out)
btn_zoom_out.pack(side=LEFT, fill=Y)

update_fonts()
root.mainloop()