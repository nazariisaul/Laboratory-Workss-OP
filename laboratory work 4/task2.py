 a1, a2, a3 = 2, 1, 4  # Задані розряди числа A
A = a1*100 + a2*10 + a3  # Саме число A
f = False  # Прапорець завершення циклів
count = 0  # Лічильник підходящих чисел

i1 = 0
while i1 <= 9:
    i2 = 0
    while i2 <= 9:
        i3 = 0
        while i3 <= 9:
            n = i1*100 + i2*10 + i3  # Поточне число
            # Перевіряємо усі перестановки цифр n
            j1 = 1
            found = False
            while j1 <= 3:
                j2 = 1
                while j2 <= 3:
                    j3 = 1
                    while j3 <= 3:
                        if j1 != j2 and j1 != j3 and j2 != j3:
                            # Вибір цифр за позиціями
                            if j1 == 1: d1 = i1
                            elif j1 == 2: d1 = i2
                            else: d1 = i3

                            if j2 == 1: d2 = i1
                            elif j2 == 2: d2 = i2
                            else: d2 = i3

                            if j3 == 1: d3 = i1
                            elif j3 == 2: d3 = i2
                            else: d3 = i3

                            num = d1*100 + d2*10 + d3
                            if num % 70 == 0:
                                found = True
                        j3 += 1
                    j2 += 1
                j1 += 1

            if found:
                count += 1  # збільшуємо лічильник

            if i1 == a1 and i2 == a2 and i3 == a3:
                f = True
            if f == True: break
            i3 += 1
        if f == True: break
        i2 += 1
    if f == True: break
    i1 += 1

print("Кількість чисел, із цифр яких можна скласти число, кратне 70:", count)
