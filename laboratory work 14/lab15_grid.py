from tkinter import *
from tkinter import messagebox

# (Глобальні змінні та функції залишаються без змін)
prices_dict = {"Шафа": 800, "Ліжко": 600, "Кухня": 2500, "Стіл": 400, "Комод": 500}
floor_price_per_one, urgent_ratio, tools_price = 150, 1.5, 200
current_width, current_height = 850, 650
font_size, title_font_size, result_font_size = 10, 12, 12

def calculate(event=None):
    selection = listbox.curselection()
    if not selection:
        result_text.set("Оберіть тип меблів у списку!")
        return
    m_name = listbox.get(selection[0]); base_price = prices_dict[m_name]
    client = ent_name.get() if ent_name.get() else "Клієнт"
    total = base_price
    s = f"Замовник: {client}\nОбрано: {m_name} ({base_price} грн)\n"
    if var_r1.get() == 2:
        extra = int(base_price * 0.3); total += extra
        s += f"Складність: Ексклюзив (+{extra} грн)\n"
    if var_c1.get() == 1:
        floors = scale_floor.get(); f_total = floors * floor_price_per_one
        total += f_total; s += f"Підйом на {floors} пов. (+{f_total} грн)\n"
    if var_c2.get() == 1: total += tools_price; s += f"Матеріали (+{tools_price} грн)\n"
    if var_c3.get() == 1:
        u_extra = int(base_price * (urgent_ratio - 1)); total += u_extra
        s += f"Терміновість (+{u_extra} грн)\n"
    count = int(spin_count.get()); total *= count
    result_text.set(s + f"\nКількість: {count} шт.\n" + "=" * 20 + f"\nРАЗОМ: {int(total)} грн.")

def update_fonts():
    title_label.config(font=("Arial", title_font_size, "bold"))
    listbox.config(font=("Arial", font_size))
    ent_name.config(font=("Arial", font_size))
    name_label.config(font=("Arial", font_size))
    r1.config(font=("Arial", font_size)); r2.config(font=("Arial", font_size))
    complexity_label.config(font=("Arial", font_size, "bold"))
    c1.config(font=("Arial", font_size)); c2.config(font=("Arial", font_size)); c3.config(font=("Arial", font_size))
    scale_floor.config(font=("Arial", font_size))
    spin_label.config(font=("Arial", font_size)); spin_count.config(font=("Arial", font_size))
    btn_calc.config(font=("Arial", title_font_size, "bold"))
    l5.config(font=("Courier", result_font_size, "bold"))

def zoom_in():
    global current_width, current_height, font_size, title_font_size, result_font_size
    current_width += 50; current_height += 40; root.geometry(f"{current_width}x{current_height}")
    font_size += 1; title_font_size += 1; result_font_size += 1; update_fonts()

def zoom_out():
    global current_width, current_height, font_size, title_font_size, result_font_size
    if current_width > 500:
        current_width -= 50; current_height -= 40; root.geometry(f"{current_width}x{current_height}")
        font_size -= 1; title_font_size -= 1; result_font_size -= 1; update_fonts()

def about(event=None):
    result_text.set("ЛР №15: Grid & Place\nВиконав: Сауляк Н.")

root = Tk()
root.title("Помічник меблевика v2.0 (GRID)")
root.geometry("850x650")

# --- РОЗМІЩЕННЯ GRID ---
# Конфігурація колонок
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.rowconfigure(4, weight=1) # Для текстового поля

# Ліва панель (Тип меблів)
f1 = Frame(root, bg="saddle brown", padx=10, pady=10)
f1.grid(row=0, column=0, rowspan=5, sticky="nsew")

title_label = Label(f1, text="ТИП МЕБЛІВ", fg="white", bg="saddle brown")
title_label.grid(row=0, column=0, pady=5)

listbox = Listbox(f1, height=10, exportselection=0)
for item in prices_dict.keys(): listbox.insert(END, item)
listbox.grid(row=1, column=0, sticky="ew")

name_label = Label(f1, text="Ім'я клієнта:", fg="white", bg="saddle brown")
name_label.grid(row=2, column=0, pady=(15, 0))
ent_name = Entry(f1)
ent_name.grid(row=3, column=0, pady=5, sticky="ew")

# Складність (Radio)
f2 = Frame(root, bg="peru", padx=10, pady=5)
f2.grid(row=0, column=1, sticky="ew")
complexity_label = Label(f2, text="Складність:", bg="peru")
complexity_label.grid(row=0, column=0)
var_r1 = IntVar(value=1)
r1 = Radiobutton(f2, text="Стандарт", variable=var_r1, value=1, bg="peru")
r2 = Radiobutton(f2, text="Ексклюзив", variable=var_r1, value=2, bg="peru")
r1.grid(row=0, column=1, padx=10); r2.grid(row=0, column=2)

# Опції (Check + Scale)
f3 = Frame(root, bg="tan", padx=10, pady=5)
f3.grid(row=1, column=1, sticky="ew")
var_c1, var_c2, var_c3 = IntVar(), IntVar(), IntVar()
c1 = Checkbutton(f3, text="Підйом", variable=var_c1, bg="tan")
c2 = Checkbutton(f3, text="Матеріали", variable=var_c2, bg="tan")
c3 = Checkbutton(f3, text="Терміново", variable=var_c3, bg="tan", fg="red")
c1.grid(row=0, column=0, sticky="w"); c2.grid(row=1, column=0, sticky="w"); c3.grid(row=2, column=0, sticky="w")
scale_floor = Scale(f3, from_=1, to=20, orient=HORIZONTAL, label="Поверх", bg="tan", length=200)
scale_floor.grid(row=0, column=1, rowspan=3, padx=30)

# Spinbox
f_extra = Frame(root, bg="gray90", padx=10, pady=5)
f_extra.grid(row=2, column=1, sticky="ew")
spin_label = Label(f_extra, text="Кількість комплектів:", bg="gray90")
spin_label.grid(row=0, column=0)
spin_count = Spinbox(f_extra, from_=1, to=50, width=5)
spin_count.grid(row=0, column=1, padx=10)

# Результат
result_text = StringVar(value="Оберіть параметри...")
l5 = Label(root, textvariable=result_text, bg="white", anchor="nw", justify=LEFT, padx=10, pady=10, relief=SUNKEN)
l5.grid(row=3, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)

# Кнопки (Нижня панель)
f4 = Frame(root, bg="gray80")
f4.grid(row=5, column=0, columnspan=2, sticky="ew")
btn_calc = Button(f4, text="РОЗРАХУВАТИ", bg="orange", command=calculate)
btn_calc.pack(side=LEFT, expand=1, fill=X)
btn_about = Button(f4, text="?", width=3, command=about).pack(side=LEFT)
btn_zoom_in = Button(f4, text="+", bg="lightgreen", width=3, command=zoom_in).pack(side=LEFT)
btn_zoom_out = Button(f4, text="-", bg="tomato", width=3, command=zoom_out).pack(side=LEFT)

update_fonts()
root.mainloop()