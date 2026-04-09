from tkinter import *
from math import *

root = Tk()
root.title("Лабораторна робота №16 - Варіант 12")

# 1. Розміри віджета Canvas
xx_max, yy_max = 800, 600
xx0, yy0 = xx_max / 2, yy_max / 2  # Центр координат

c1 = Canvas(root, width=xx_max, height=yy_max, bg="white")
c1.pack()

# Побудова осей (X та Y)
c1.create_line(10, yy0, xx_max - 10, yy0, width=1, arrow=LAST)  # Вісь X
c1.create_line(xx0, yy_max - 10, xx0, 10, width=1, arrow=LAST)  # Вісь Y

# 2. Розмітка осей (додаємо по 2-3 позначки)
# Позначки на осі X (1 та 2 одиниці масштабу)
for i in [-2, -1, 1, 2]:
    tick_x = xx0 + i * 80
    c1.create_line(tick_x, yy0 - 5, tick_x, yy0 + 5)
    c1.create_text(tick_x, yy0 + 15, text=str(i), font="Arial 8")

# Позначки на осі Y
for i in [-2, -1, 1, 2]:
    tick_y = yy0 - i * 80
    c1.create_line(xx0 - 5, tick_y, xx0 + 5, tick_y)
    c1.create_text(xx0 - 15, tick_y, text=str(i), font="Arial 8")

# 3. Параметри побудови
t1, t2 = 0, 2 * pi  # Повний період для тригонометричних функцій
dt = 0.005  # Крок для плавності ліній
kx, ky = 80, 80  # Коефіцієнти масштабування

# 4. Цикл побудови графіка
t = t1
while (t <= t2):
    # Функції згідно з варіантом 12
    x = 2 * (cos(t) + cos(5 * t) / 3)
    y = 2 * (sin(t) - sin(5 * t) / 3)

    # Перерахунок у екранні координати
    xx = kx * x + xx0
    yy = ky * y * (-1) + yy0  # Множимо на -1, бо в Canvas Y росте вниз

    # Малюємо точку
    c1.create_oval(xx, yy, xx, yy, outline="blue", width=2)
    t = t + dt

# 5. Додавання формул на полотно
formula_text = "x = 2 * (cos(t) + cos(5*t)/3)\ny = 2 * (sin(t) - sin(5*t)/3)"
c1.create_text(150, 50, text=formula_text, font="Times 12 italic", justify=LEFT)

# 6. Прізвище та ініціали студента (правий нижній кут)
c1.create_text(xx_max - 100, yy_max - 20, text="Сауляк Н.", font="Arial 10")

root.mainloop()