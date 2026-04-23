from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# --- Ініціалізація головного вікна ---
root = Tk()
root.title("Помічник збирача меблів v2.0")
root.geometry("850x720")

# Словник з базовими цінами на вироби в доларах
prices_usd = {
    "Стіл": 125,
    "Комод": 140,
    "Ліжко": 150,
    "Шафа-купе (2-дв)": 310,
    "Кухня (пог. метр)": 550,
    "Офісне крісло": 90,
}

floor_usd_per_one = 3.0    # Вартість підйому на один поверх ($)
tools_usd = 5.0            # Витрати на розхідні матеріали ($)
urgent_ratio = 1.3         # Коефіцієнт за терміновість (+30%)
# Вартість доставки по містах
cities_delivery = {"Київ": 0, "Бровари": 8, "Бориспіль": 8, "Ірпінь": 8, "Область": 15}

# Початкові налаштування розмірів вікна та шрифтів
current_width, current_height = 850, 720
font_size, title_font_size, result_font_size = 10, 12, 12

# --- Функції (Логіка програми) ---

def update_fonts():
    """Оновлює шрифти для всіх віджетів (використовується при масштабуванні)"""
    f_style = ("Arial", font_size)
    b_style = ("Arial", title_font_size, "bold")
    title_label.config(font=b_style)
    listbox.config(font=f_style)
    ent_name.config(font=f_style)
    ent_rate.config(font=f_style)
    name_label.config(font=f_style)
    rate_label.config(font=f_style)
    r1.config(font=f_style)
    r2.config(font=f_style)
    complexity_label.config(font=("Arial", font_size, "bold"))
    c1.config(font=f_style)
    c2.config(font=f_style)
    c3.config(font=f_style)
    scale_floor.config(font=f_style)
    spin_label.config(font=f_style)
    spin_count.config(font=f_style)
    btn_calc.config(font=b_style)
    btn_clear.config(font=b_style)
    btn_about.config(font=f_style)
    btn_zoom_in.config(font=f_style)
    btn_zoom_out.config(font=f_style)
    l5.config(font=("Courier", result_font_size, "bold"))

def zoom_in():
    """Збільшує вікно та розмір тексту"""
    global current_width, current_height, font_size, title_font_size, result_font_size
    current_width += 50; current_height += 40
    root.geometry(f"{current_width}x{current_height}")
    font_size += 1; title_font_size += 1; result_font_size += 1
    update_fonts()

def zoom_out():
    """Зменшує вікно та розмір тексту (до певної межі)"""
    global current_width, current_height, font_size, title_font_size, result_font_size
    if current_width > 600:
        current_width -= 50; current_height -= 40
        root.geometry(f"{current_width}x{current_height}")
        font_size -= 1; title_font_size -= 1; result_font_size -= 1
        update_fonts()

def clear_all():
    """Скидає всі введені дані до початкового стану"""
    ent_name.delete(0, END)
    listbox.selection_clear(0, END)
    var_r1.set(1)
    var_c1.set(0)
    var_c2.set(0)
    var_c3.set(0)
    scale_floor.set(1)
    spin_count.delete(0, END)
    spin_count.insert(0, "1")
    combo_city.current(0)
    var_pay.set("Готівка")
    result_text.set("Поля очищено. Сформуйте нове замовлення...")

def about():
    """Показує вікно з інформацією про програму"""
    messagebox.showinfo("Про автора", "Виконав: Сауляк Н.\nВерсія 2.5: Додано функцію очищення.")

def calculate():
    """Основна функція розрахунку вартості замовлення"""
    try:
        # Отримуємо курс валют
        current_rate = float(ent_rate.get().replace(',', '.'))
    except ValueError:
        messagebox.showerror("Помилка", "Введіть коректний курс (напр. 43.4)")
        return

    # Перевірка, чи обрано виріб у списку
    selection = listbox.curselection()
    if not selection:
        result_text.set("Оберіть виріб у списку!")
        return

    m_name = listbox.get(selection[0]) # Назва обраного виробу
    base_usd = prices_usd[m_name]       # Його базова ціна
    client = ent_name.get() if ent_name.get() else "Клієнт"

    total_usd = base_usd
    s = f"Замовник: {client}\nОб'єкт: {m_name} (${base_usd})\n"

    # Доплата за складність (Ексклюзив)
    if var_r1.get() == 2:
        extra = base_usd * 0.4
        total_usd += extra
        s += f"Складність: Ексклюзив (+${extra:.1f})\n"

    # Доплата за доставку по містах
    city = combo_city.get()
    d_usd = cities_delivery.get(city, 0)
    total_usd += d_usd
    if d_usd > 0: s += f"Доставка ({city}): +${d_usd}\n"

    # Розрахунок підйому на поверх
    if var_c1.get() == 1:
        floors = scale_floor.get()
        f_total = floors * floor_usd_per_one
        total_usd += f_total
        s += f"Підйом на {floors} пов.: +${f_total:.1f}\n"

    # Доплата за розхідні матеріали
    if var_c2.get() == 1:
        total_usd += tools_usd
        s += f"Матеріали: +${tools_usd}\n"

    # Націнка за терміновість (на всю суму)
    if var_c3.get() == 1:
        u_extra = total_usd * (urgent_ratio - 1)
        total_usd += u_extra
        s += f"Терміновість: +30% (+${u_extra:.1f})\n"

    # Врахування кількості одиниць
    count = int(spin_count.get())
    total_usd *= count
    total_uah = total_usd * current_rate # Переведення в гривні

    # Формування підсумкового тексту
    final_res = s + f"Кількість: {count} шт. | Оплата: {var_pay.get()}\n"
    final_res += f"Курс: {current_rate} грн/$\n" + "="*25 + f"\nРАЗОМ: {int(total_uah)} грн."
    result_text.set(final_res)

# --- Графічний інтерфейс (UI) ---

# Ліва панель (Каталог та основні дані)
f1 = Frame(root, bg="saddle brown", padx=10, pady=10)
f1.pack(side=LEFT, fill=Y)

title_label = Label(f1, text="КАТАЛОГ", fg="white", bg="saddle brown")
title_label.pack(pady=5)

listbox = Listbox(f1, height=8, exportselection=0)
for item in prices_usd.keys():
    listbox.insert(END, item)
listbox.pack(pady=5, fill=X)

rate_label = Label(f1, text="Курс долара:", fg="gold", bg="saddle brown")
rate_label.pack(pady=(10, 0))
ent_rate = Entry(f1, justify=CENTER)
ent_rate.insert(0, "43.40")
ent_rate.pack(pady=5, fill=X)

name_label = Label(f1, text="Ім'я клієнта:", fg="white", bg="saddle brown")
name_label.pack(pady=(10, 0))
ent_name = Entry(f1)
ent_name.pack(pady=5, fill=X)

# Верхня панель (Вибір складності)
f2 = Frame(root, bg="peru", padx=10, pady=5)
f2.pack(side=TOP, fill=X)
complexity_label = Label(f2, text="Складність:", bg="peru")
complexity_label.pack(side=LEFT)
var_r1 = IntVar(value=1)
r1 = Radiobutton(f2, text="Стандарт", variable=var_r1, value=1, bg="peru")
r2 = Radiobutton(f2, text="Ексклюзив (+40%)", variable=var_r1, value=2, bg="peru")
r1.pack(side=LEFT, padx=10); r2.pack(side=LEFT)

# Панель вибору міста та типу оплати
f_new = Frame(root, bg="#d2b48c", padx=10, pady=5)
f_new.pack(side=TOP, fill=X)
Label(f_new, text="Місто:", bg="#d2b48c").pack(side=LEFT)
combo_city = ttk.Combobox(f_new, values=list(cities_delivery.keys()), state="readonly", width=15)
combo_city.current(0)
combo_city.pack(side=LEFT, padx=5)

Label(f_new, text="Оплата:", bg="#d2b48c").pack(side=LEFT, padx=(10, 5))
var_pay = StringVar(value="Готівка")
opt_pay = OptionMenu(f_new, var_pay, "Готівка", "Карта", "ФОП")
opt_pay.config(bg="#d2b48c")
opt_pay.pack(side=LEFT)

# Панель додаткових послуг (Чекбокси та повзунок поверхів)
f3 = Frame(root, bg="tan", padx=10, pady=5)
f3.pack(side=TOP, fill=X)
var_c1, var_c2, var_c3 = IntVar(), IntVar(), IntVar()
c1 = Checkbutton(f3, text="Підйом", variable=var_c1, bg="tan")
c2 = Checkbutton(f3, text="Матеріали", variable=var_c2, bg="tan")
c3 = Checkbutton(f3, text="Терміново", variable=var_c3, bg="tan", fg="red")
c1.grid(row=0, column=0, sticky=W); c2.grid(row=1, column=0, sticky=W); c3.grid(row=2, column=0, sticky=W)

scale_floor = Scale(f3, from_=1, to=25, orient=HORIZONTAL, label="Оберіть поверх", bg="tan", length=200)
scale_floor.grid(row=0, column=1, rowspan=3, padx=20)

# Панель вибору кількості
f_extra = Frame(root, bg="gray90", padx=10, pady=5)
f_extra.pack(side=TOP, fill=X)
spin_label = Label(f_extra, text="Кількість:", bg="gray90")
spin_label.pack(side=LEFT)
spin_count = Spinbox(f_extra, from_=1, to=50, width=5)
spin_count.pack(side=LEFT, padx=10)

# Поле для виведення результату
result_text = StringVar(value="Сформуйте замовлення...")
l5 = Label(root, textvariable=result_text, bg="white", anchor="nw", justify=LEFT, padx=10, pady=10, relief=SUNKEN)
l5.pack(side=TOP, expand=1, fill=BOTH, padx=10, pady=10)

# Нижня панель з кнопками управління
f4 = Frame(root, bg="gray80")
f4.pack(side=BOTTOM, fill=X)

btn_calc = Button(f4, text="РОЗРАХУВАТИ", bg="orange", command=calculate)
btn_calc.pack(side=LEFT, expand=1, fill=BOTH)

btn_clear = Button(f4, text="ОЧИСТИТИ", bg="lightblue", command=clear_all)
btn_clear.pack(side=LEFT, expand=1, fill=BOTH)

btn_about = Button(f4, text="?", bg="gray70", width=3, command=about)
btn_about.pack(side=LEFT, fill=Y)

btn_zoom_in = Button(f4, text="+", bg="lightgreen", width=3, command=zoom_in)
btn_zoom_in.pack(side=LEFT, fill=Y)

btn_zoom_out = Button(f4, text="-", bg="tomato", width=3, command=zoom_out)
btn_zoom_out.pack(side=LEFT, fill=Y)

# Перший запуск оновлення шрифтів та запуск циклу програми
update_fonts()
root.mainloop()