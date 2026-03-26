import random
import time


def solve():
    # --- НАЛАШТУВАННЯ ---
    M = 500  # Кількість рядків
    N = 200000  # Кількість стовпців
    MIN_LENGTH = 6  # Мінімальна довжина

    input_file = "input2.txt"
    output_file = "output2.txt"

    try:
        start_time = time.time()

        # 1. ГЕНЕРАЦІЯ ЧИСТОЇ МАТРИЦІ
        print(f"Генеруємо абсолютно випадкову матрицю {M}x{N}...")
        with open(input_file, "w", encoding="utf-8") as f:
            f.write(f"{M} {N}\n")
            for _ in range(M):
                # Тільки випадкові числа, ніякої підміни
                row = [random.randint(1, 100) for _ in range(N)]
                f.write(" ".join(map(str, row)) + "\n")

        mid_gen = time.time()
        print(f"Генерація завершена за {mid_gen - start_time:.2f} сек.")

        # 2. АНАЛІЗ
        print(f"Аналізуємо на прогресії довжиною >= {MIN_LENGTH}...")
        with open(input_file, "r", encoding="utf-8") as f_in, \
                open(output_file, "w", encoding="utf-8") as f_out:

            header = f_in.readline()  # Пропускаємо заголовок

            f_out.write(f"РЕЗУЛЬТАТИ АНАЛІЗУ (ЧИСТИЙ РАНДОМ)\n")
            f_out.write(f"Матриця: {M}x{N}, Шукана довжина: >= {MIN_LENGTH}\n")
            f_out.write("-" * 80 + "\n")

            total_found = 0
            for i in range(M):
                line = f_in.readline()
                if not line: break

                # Перетворюємо рядок у числа
                row = [int(x) for x in line.split()]

                j = 0
                while j <= N - 2:
                    d = row[j + 1] - row[j]
                    count = 2
                    k = j + 2

                    # Шукаємо ланцюжок
                    while k < N:
                        if row[k] - row[k - 1] == d:
                            count += 1
                            k += 1
                        else:
                            break

                    # Якщо раптом рандом видав довгу прогресію
                    if count >= MIN_LENGTH:
                        progression_elements = row[j:k]

                        f_out.write(f"РЯДОК {i + 1}:\n")
                        f_out.write(f"  Позиція: №{j + 1}\n")
                        f_out.write(f"  Кількість елементів: {count}\n")
                        f_out.write(f"  Крок: {d}\n")
                        f_out.write(f"  Елементи: {progression_elements}\n")
                        f_out.write("-" * 40 + "\n")

                        total_found += 1
                        j = k - 1
                    else:
                        j += 1

            end_time = time.time()
            if total_found == 0:
                f_out.write(f"\nЗа результатами аналізу жодної прогресії довжиною {MIN_LENGTH}+ не знайдено.\n")


            f_out.write(f"\nВсього знайдено: {total_found}\n")
            f_out.write(f"Час аналізу: {end_time - mid_gen:.4f} сек.")

        print(f"Готово! Перевірте файл '{output_file}'")

    except Exception as e:
        print(f"Помилка: {e}")


if __name__ == "__main__":
    solve()