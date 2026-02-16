# Індивідуальне творче завдання
# Варіант завдання: фізик

# --- Функції для обчислень ---

def calculate_kinetic_energy():
    #Обчислює та виводить кінетичну енергію.
    print("--- 1. Кінетична енергія ---")
    print("Формула: E = 1/2 * m * v^2")

    m = float(input("Маса m (кг): "))
    v = float(input("Швидкість v (м/с): "))

    if m > 0 and v >= 0:
        E = 0.5 * m * v * v
        print(f"Кінетична енергія E = {E:.2f} Дж")
    else:
        print("Помилка: маса має бути >0, швидкість ≥0.")


def calculate_potential_energy():
    #Обчислює та виводить потенціальну енергію.
    print("--- 2. Потенціальна енергія ---")
    print("Формула: E = m * g * h (g ≈ 9.81 м/с²)")

    m = float(input("Маса m (кг): "))
    h = float(input("Висота h (м): "))

    if m > 0 and h >= 0:
        g = 9.81
        E = m * g * h
        print(f"Потенціальна енергія E = {E:.2f} Дж")
    else:
        print("Помилка: маса має бути >0, висота ≥0.")


def calculate_ohm_law():
    #Обчислює та виводить силу струму за законом Ома.
    print("--- 3. Закон Ома ---")
    print("Формула: I = U / R")

    U = float(input("Напруга U (В): "))
    R = float(input("Опір R (Ом): "))

    if R > 0:
        I = U / R
        print(f"Сила струму I = {I:.2f} А")
    else:
        print("Помилка: опір має бути >0!")


def calculate_force():
    #Обчислює та виводить силу за другим законом Ньютона.
    print("--- 4. Сила ---")
    print("Формула: F = m * a")

    m = float(input("Маса m (кг): "))
    a = float(input("Прискорення a (м/с^2): "))

    if m > 0:
        F = m * a
        print(f"Сила F = {F:.2f} Н")
    else:
        print("Помилка: маса має бути >0!")


def calculate_pressure():
    #Обчислює та виводить тиск.
    print("--- 5. Тиск ---")
    print("Формула: p = F / S")

    F = float(input("Сила F (Н): "))
    S = float(input("Площа S (м^2): "))

    if S > 0:
        p = F / S
        print(f"Тиск p = {p:.2f} Па")
    else:
        print("Помилка: площа має бути >0!")


def calculate_density():
    #Обчислює та виводить густину.
    print("--- 6. Густина ---")
    print("Формула: ρ = m / V")

    m = float(input("Маса m (кг): "))
    V = float(input("Об'єм V (м^3): "))

    if V > 0:
        ro = m / V
        print(f"Густина ρ = {ro:.2f} кг/м^3")
    else:
        print("Помилка: об'єм має бути >0!")


def calculate_frequency():
    #Обчислює та виводить частоту коливань.
    print("--- 7. Частота ---")
    print("Формула: ν = 1/T")

    T = float(input("Період T (с): "))

    if T > 0:
        nu = 1 / T
        print(f"Частота ν = {nu:.2f} Гц")
    else:
        print("Помилка: період має бути >0!")


def display_info():
    #Виводить інформацію про програму.
    print("--- 8. Про програму ---")
    print("Розробив: Назарій Сауляк")
    print("Група: Б25_д/F3 (Б)")
    print('Програма "Фізик-помічник"')


def display_menu():
    #Виводить головне меню програми.
    print("\n-----------------------------")
    print('  Програма "Фізик-помічник"  ')
    print("-----------------------------")
    print("\n1. Кінетична енергія")
    print("2. Потенціальна енергія")
    print("3. Закон Ома")
    print("4. Сила (F = m*a)")
    print("5. Тиск (p = F/S)")
    print("6. Густина (ρ = m/V)")
    print("7. Частота (ν = 1/T)")
    print("8. Про програму")
    print("0. Вихід")
    print()


# --- Основна функція програми (Main Loop) ---

def main():
    #Головний цикл програми.
    # Словник, що зіставляє вибір користувача з відповідною функцією
    menu_actions = {
        "1": calculate_kinetic_energy,
        "2": calculate_potential_energy,
        "3": calculate_ohm_law,
        "4": calculate_force,
        "5": calculate_pressure,
        "6": calculate_density,
        "7": calculate_frequency,
        "8": display_info,
    }

    while True:
        display_menu()
        choice = input("Оберіть пункт меню -> ")

        if choice == "0":
            print("Програму завершено.")
            break
        elif choice in menu_actions:
            menu_actions[choice]()  # Виклик відповідної функції
        else:
            print("Невірний вибір. Спробуйте ще раз.")

        print()
        input("Натисніть Enter для продовження.")


# Запуск головної функції
if __name__ == "__main__":
    main()
