import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import math, random, os
from datetime import datetime

import matplotlib
matplotlib.use("TkAgg")  # Використовуємо TkAgg як бекенд для matplotlib (сумісний з tkinter)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# ─────────────────────────── ПАЛІТРА КОЛЬОРІВ ───────────────────────────────
# Усі кольори зберігаємо у константах, щоб легко змінювати тему програми
BG      = "#0d1117"   # Фон головного вікна
PANEL   = "#161b22"   # Фон панелей
CARD    = "#1c2128"   # Фон карток/блоків
CARD2   = "#1f2630"   # Альтернативний фон карток
BORDER  = "#30363d"   # Колір рамок і роздільників
ACCENT  = "#58a6ff"   # Акцентний синій (вхідні поля, кнопки)
GREEN   = "#3fb950"   # Зелений (результати, успіх)
YELLOW  = "#d29922"   # Жовтий (константи, попередження)
RED     = "#f85149"   # Червоний (помилки, вихід)
PURPLE  = "#bc8cff"   # Фіолетовий (символьні вирази)
CYAN    = "#39d3f0"   # Блакитний (допоміжний)
FG      = "#e6edf3"   # Основний колір тексту (майже білий)
FG2     = "#8b949e"   # Другорядний текст (сірий)

# Кольорове кодування за змістом поля
CLR_INPUT  = "#58a6ff"   # Вхідні дані — синій
CLR_CONST  = "#d29922"   # Константи — жовтий
CLR_RESULT = "#3fb950"   # Результати (read-only) — зелений

# ШРИФТИ
# Використовуємо Courier New (моноширинний) для читабельності чисел
FN   = ("Courier New", 11)           # Звичайний
FNB  = ("Courier New", 11, "bold")   # Жирний
FNS  = ("Courier New", 10)            # Малий
FH   = ("Courier New", 15, "bold")   # Заголовок
FHS  = ("Courier New", 10, "bold")    # Маленький заголовок секції
FBIG = ("Courier New", 22, "bold")   # Великий (для героя-результату)

# СТИЛЬ MATPLOTLIB
# Налаштовуємо глобальний стиль графіків, щоб вони відповідали темній темі
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": CARD,
    "axes.edgecolor": BORDER, "axes.labelcolor": FG2,
    "xtick.color": FG2, "ytick.color": FG2,
    "grid.color": BORDER, "grid.linestyle": "--", "grid.alpha": 0.5,
    "text.color": FG, "lines.linewidth": 1.8,
    "font.family": "monospace", "font.size": 9,
})


# ═══════════════════════════════════════════════════════════════════════════
#  СПІЛЬНІ ПОМІЧНИКИ — функції, які використовуються в усіх вкладках
# ═══════════════════════════════════════════════════════════════════════════

def section_label(parent, text, pady_top=10):
    """Малює горизонтальний роздільник із підписом секції (для pack-контейнерів)."""
    f = tk.Frame(parent, bg=BG)
    f.pack(fill="x", pady=(pady_top, 2))
    tk.Label(f, text=text, font=FHS, bg=BG, fg=FG2).pack(side="left")
    # Лінія-роздільник праворуч від тексту
    tk.Frame(f, bg=BORDER, height=1).pack(side="left", fill="x", expand=True, padx=(6, 0))

def section_grid(parent, text, row, col=0, colspan=2, pady_top=8):
    """Аналог section_label, але для grid-контейнерів."""
    f = tk.Frame(parent, bg=BG)
    f.grid(row=row, column=col, columnspan=colspan, sticky="ew", pady=(pady_top, 2))
    tk.Label(f, text=text, font=FHS, bg=BG, fg=FG2).pack(side="left")
    tk.Frame(f, bg=BORDER, height=1).pack(side="left", fill="x", expand=True, padx=(6, 0))

def mkbtn(parent, text, cmd, color=ACCENT, bold=False, big=False):
    """
    Фабрична функція для створення стилізованих кнопок.
    color — акцентний колір рамки та тексту (ACCENT, GREEN, RED тощо).
    big=True — збільшений розмір кнопки (для головних дій).
    """
    pady = 10 if big else 5
    font = ("Courier New", 11, "bold") if big else (FNB if bold else FN)
    # Темний відтінок акцентного кольору для фону кнопки
    bg_c = "#0d2340" if color == ACCENT else ("#0d2d1a" if color == GREEN else CARD)
    return tk.Button(parent, text=text, command=cmd,
                     font=font, bg=bg_c, fg=color,
                     activebackground=PANEL, activeforeground=color,
                     relief="flat", cursor="hand2", pady=pady,
                     highlightbackground=color, highlightthickness=1)

def mkentry(parent, val="", width=10, color=CLR_INPUT):
    """Створює стилізоване поле введення з кольоровою рамкою."""
    e = tk.Entry(parent, font=FN, bg=CARD, fg=color,
                 insertbackground=color, relief="flat",
                 highlightbackground=color, highlightthickness=1, width=width)
    e.insert(0, val)
    return e

def mkentry_ro(parent, val="", width=14):
    """
    Поле результату — тільки для читання (read-only), зелений колір.
    Значення можна побачити, але не редагувати.
    """
    e = tk.Entry(parent, font=FNB, bg=CARD2, fg=CLR_RESULT,
                 relief="flat", highlightbackground=CLR_RESULT,
                 highlightthickness=1, width=width, state="readonly")
    e.configure(state="normal")
    e.insert(0, val)
    e.configure(state="readonly")
    return e

def dot_label(parent, color, text, **kw):
    """Кольорова крапка-маркер + підпис поруч (для позначення типу поля)."""
    f = tk.Frame(parent, bg=BG)
    tk.Label(f, text="●", font=FNS, bg=BG, fg=color).pack(side="left")
    tk.Label(f, text=text, font=FNS, bg=BG, fg=FG2, **kw).pack(side="left", padx=(2, 0))
    return f

def log_write(widget, msg):
    """Додає рядок у консоль-лог з часовою міткою. Після запису автоскролить вниз."""
    widget.configure(state="normal")
    widget.insert("end", f"[{datetime.now():%H:%M:%S}] {msg}\n")
    widget.see("end")
    widget.configure(state="disabled")

def make_log(parent, height=3):
    """Створює й відразу пакує scrolled-віджет консолі (read-only, зелений текст)."""
    w = scrolledtext.ScrolledText(parent, height=height, font=FNS,
                                   bg=CARD, fg=GREEN, relief="flat",
                                   highlightbackground=BORDER, highlightthickness=1,
                                   state="disabled")
    w.pack(fill="x")
    return w

def style_tree(tree):
    """Застосовує темну тему до Treeview (таблиці), щоб відповідало загальній палітрі."""
    s = ttk.Style()
    s.configure("PL.Treeview", background=CARD, foreground=FG,
                fieldbackground=CARD, rowheight=20, font=FNS)
    s.configure("PL.Treeview.Heading", background=PANEL, foreground=ACCENT, font=FHS)
    s.map("PL.Treeview", background=[("selected", BORDER)])
    tree.configure(style="PL.Treeview")

def embed_figure(fig, parent, toolbar=True):
    """
    Вбудовує matplotlib-фігуру в tkinter-контейнер.
    Повертає canvas для подальшого виклику canvas.draw().
    """
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    if toolbar:
        tb = NavigationToolbar2Tk(canvas, parent)
        tb.configure(bg=PANEL)
        tb.update()
    return canvas

def placeholder(ax, text):
    """Відображає текст-заглушку у порожньому графіку (до першого розрахунку)."""
    ax.text(0.5, 0.5, text, ha="center", va="center",
            transform=ax.transAxes, color=FG2, fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])

def nb_style():
    """Стиль для дочірніх Notebook (суб-вкладки всередині вкладок)."""
    s = ttk.Style()
    s.configure("Sub.TNotebook", background=CARD, borderwidth=0)
    s.configure("Sub.TNotebook.Tab", background=PANEL, foreground=FG2,
                 font=FNS, padding=[10, 5], borderwidth=0)
    s.map("Sub.TNotebook.Tab",
          background=[("selected", BG)], foreground=[("selected", ACCENT)])


# ═══════════════════════════════════════════════════════════════════════════
#  КОНВЕРТЕР ОДИНИЦЬ — дані та логіка
# ═══════════════════════════════════════════════════════════════════════════

# Словник груп одиниць: ключ = назва групи, значення = словник {одиниця: коефіцієнт до SI}
UNIT_GROUPS = {
    "Швидкість":   {"м/с":1.,"км/год":1/3.6,"миль/год":0.44704,"вузол":0.514444,"фут/с":0.3048},
    "Довжина":     {"м":1.,"км":1e3,"см":1e-2,"мм":1e-3,"дюйм":0.0254,"фут":0.3048,"миля":1609.34,"а.о.":1.496e11},
    "Маса":        {"кг":1.,"г":1e-3,"мг":1e-6,"фунт":0.453592,"унція":0.0283495,"т":1e3},
    "Час":         {"с":1.,"мс":1e-3,"мкс":1e-6,"хв":60.,"год":3600.,"доба":86400.},
    "Енергія":     {"Дж":1.,"кДж":1e3,"МДж":1e6,"еВ":1.60218e-19,"МеВ":1.60218e-13,"кал":4.184,"ккал":4184.,"ерг":1e-7},
    "Тиск":        {"Па":1.,"кПа":1e3,"МПа":1e6,"атм":101325.,"бар":1e5,"мм рт.ст.":133.322,"пси":6894.76},
    "Температура": {"°C":"C","K":"K","°F":"F"},
    "Кут":         {"рад":1.,"°":math.pi/180,"'":math.pi/10800,"\"":math.pi/648000},
}

def convert_value(value, from_u, to_u, group):
    """
    Перетворює значення між одиницями однієї групи.
    Температура обробляється окремо через нелінійні формули (°C ↔ K ↔ °F).
    Для решти груп: множимо на коефіцієнт from_u та ділимо на коефіцієнт to_u.
    """
    if group == "Температура":
        codes = {"°C": "C", "K": "K", "°F": "F"}
        fc, tc = codes[from_u], codes[to_u]
        if fc == tc:
            return value
        # Спочатку переводимо все в Кельвіни
        kelvin = value + 273.15 if fc == "C" else (value if fc == "K" else (value - 32) * 5 / 9 + 273.15)
        # Потім конвертуємо з Кельвінів у цільову одиницю
        return kelvin - 273.15 if tc == "C" else (kelvin if tc == "K" else (kelvin - 273.15) * 9 / 5 + 32)
    f = UNIT_GROUPS[group]
    return value * f[from_u] / f[to_u]

def unit_popup(parent, group_hint=None, callback=None):
    """
    Відкриває спливаюче вікно конвертера одиниць.
    callback — функція, яку викликають після натискання «Використати»
    (передає рядок результату назад у поле, звідки відкрили конвертер).
    """
    win = tk.Toplevel(parent) #Вікриття спливаючого вікна для конвертації
    win.title("⚖ Конвертер")
    win.configure(bg=BG)
    win.resizable(False, False)
    win.grab_set()  # Блокує взаємодію з головним вікном поки відкрите це

    tk.Label(win, text="⚖  Конвертер одиниць", font=FNB, bg=BG, fg=ACCENT).pack(pady=(10, 4), padx=16)

    # Вибір групи одиниць
    grp_var = tk.StringVar(value=group_hint or list(UNIT_GROUPS.keys())[0])
    grp_cb = ttk.Combobox(win, textvariable=grp_var, values=list(UNIT_GROUPS.keys()),
                           font=FN, state="readonly", width=20)
    grp_cb.pack(padx=16, pady=4)

    # Рядок: значення → від → до
    mid = tk.Frame(win, bg=BG)
    mid.pack(padx=16, pady=4)
    val_e = mkentry(mid, "1.0", width=12)
    val_e.pack(side="left")
    from_cb = ttk.Combobox(mid, font=FN, state="readonly", width=10)
    from_cb.pack(side="left", padx=4)
    tk.Label(mid, text="→", font=FNB, bg=BG, fg=YELLOW).pack(side="left")
    to_cb = ttk.Combobox(mid, font=FN, state="readonly", width=10)
    to_cb.pack(side="left", padx=4)

    # Мітка результату
    res_lbl = tk.Label(win, text="", font=FH, bg=BG, fg=GREEN)
    res_lbl.pack(pady=6)

    def refresh(*_):
        """Оновлює списки одиниць при зміні групи."""
        g = grp_var.get()
        units = list(UNIT_GROUPS[g].keys())
        from_cb["values"] = units
        from_cb.set(units[0])
        to_cb["values"] = units
        to_cb.set(units[1] if len(units) > 1 else units[0])
        do_convert()

    def do_convert(*_):
        """Виконує конвертацію і показує результат у res_lbl."""
        try:
            v = float(val_e.get())
            r = convert_value(v, from_cb.get(), to_cb.get(), grp_var.get())
            res_lbl.config(text=f"{v} {from_cb.get()}  =  {r:.6g} {to_cb.get()}")
        except Exception as e:
            res_lbl.config(text=f"Помилка: {e}")

    def use_result():
        """Передає результат у поле-джерело через callback і закриває вікно."""
        txt = res_lbl.cget("text")
        if "=" in txt and callback:
            result = txt.split("=")[1].strip().split()[0]
            callback(result)
            win.destroy()

    # Прив'язуємо події
    grp_cb.bind("<<ComboboxSelected>>", refresh)
    val_e.bind("<KeyRelease>", do_convert)
    from_cb.bind("<<ComboboxSelected>>", do_convert)
    to_cb.bind("<<ComboboxSelected>>", do_convert)
    refresh()

    # Кнопки управління
    row = tk.Frame(win, bg=BG)
    row.pack(pady=(4, 12), padx=16)
    mkbtn(row, "🔄 Конвертувати", do_convert, ACCENT).pack(side="left", padx=4)
    if callback:
        mkbtn(row, "✅ Використати", use_result, GREEN).pack(side="left", padx=4)
    mkbtn(row, "✖ Закрити", win.destroy, RED).pack(side="left", padx=4)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  ВКЛАДКА 1 — СТАТИСТИКА                                                 ║
# ╚══════════════════════════════════════════════════════════════════════════╝
class StatisticsTab(tk.Frame):
    """
    Вкладка статистичної обробки вимірювань.
    Обчислює: середнє, стандартне відхилення, похибку середнього,
    довірчий інтервал (критерій Стьюдента), будує гістограму + криву Гаусса.
    """
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.data: list[float] = []   # Масив числових вимірювань
        self.last_stats = None        # Останній результат розрахунку (для звіту)
        self._build()

    def _build(self):
        """Будує інтерфейс вкладки: ліва панель (введення) + права (графік)."""
        # PanedWindow дозволяє юзеру змінювати ширину лівої/правої панелі
        pw = tk.PanedWindow(self, orient="horizontal", bg=BG, sashwidth=4)
        pw.pack(fill="both", expand=True, padx=6, pady=6)
        left = tk.Frame(pw, bg=BG, width=300)
        pw.add(left, minsize=265)

        # ── ЛІВА ПАНЕЛЬ: джерело даних ───────────────────────────────
        section_label(left, "ДЖЕРЕЛО ДАНИХ", pady_top=4)
        mkbtn(left, "📂 Читати з файлу",    self._load_file, ACCENT).pack(fill="x", pady=2)
        mkbtn(left, "🎲 Генерувати випадкові", self._generate, GREEN).pack(fill="x", pady=2)

        dot_label(left, CLR_INPUT, "Введіть вручну (по рядку):").pack(fill="x", pady=(6, 1))
        # Текстове поле для ручного введення — кожне значення з нового рядка
        self.manual = scrolledtext.ScrolledText(left, height=6, font=FNS,
                       bg=CARD, fg=CLR_INPUT, insertbackground=ACCENT, relief="flat",
                       highlightbackground=CLR_INPUT, highlightthickness=1)
        self.manual.pack(fill="x", pady=(0, 3))
        mkbtn(left, "✏️ Застосувати введені", self._apply_manual, YELLOW).pack(fill="x", pady=2)

        # ── Налаштування рівня довіри ─────────────────────────────────
        section_label(left, "НАЛАШТУВАННЯ")
        row = tk.Frame(left, bg=BG)
        row.pack(fill="x", pady=4)
        tk.Label(row, text="Рівень довіри:", font=FNS, bg=BG, fg=FG2).pack(side="left")
        self.conf_var = tk.StringVar(value="0.95")
        ttk.Combobox(row, textvariable=self.conf_var, values=["0.90", "0.95", "0.99"],
                     width=7, font=FN, state="readonly").pack(side="left", padx=6)

        # ── Головна кнопка дії ────────────────────────────────────────
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=(10, 4))
        mkbtn(left, "⚙️  РОЗРАХУВАТИ", self._calculate, ACCENT, big=True).pack(fill="x", pady=2)
        mkbtn(left, "💾 Зберегти звіт у файл", self._save_report, GREEN).pack(fill="x", pady=2)
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=(4, 2))

        # ── Блок результатів (read-only мітки) ───────────────────────
        section_label(left, "РЕЗУЛЬТАТИ")
        card = tk.Frame(left, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x", pady=4)
        self.rlbl = {}  # Словник міток результату: ключ → Label
        rows_def = [("n", "Кількість n"), ("mean", "Середнє x̄"), ("std", "Відхилення σ"),
                    ("dm", "Похибка Δx̄"), ("ci", "Інтервал ±"), ("res", "Результат")]
        for i, (k, l) in enumerate(rows_def):
            bg = CARD if i % 2 == 0 else CARD2   # Чергування фону рядків
            r = tk.Frame(card, bg=bg)
            r.pack(fill="x")
            tk.Label(r, text=l, font=FNS, bg=bg, fg=FG2, anchor="w", padx=8, pady=4, width=16).pack(side="left")
            color = CLR_RESULT if k == "res" else ACCENT
            v = tk.Label(r, text="—", font=FNB, bg=bg, fg=color, anchor="e", padx=8)
            v.pack(side="right")
            self.rlbl[k] = v

        section_label(left, "КОНСОЛЬ")
        self.log = make_log(left, height=6)

        # ── ПРАВА ПАНЕЛЬ: дані та графік ─────────────────────────────
        right = tk.Frame(pw, bg=BG)
        pw.add(right, minsize=420)

        section_label(right, "ДАНІ", pady_top=4)
        # Показ масиву у форматі 6 чисел на рядок
        self.data_disp = scrolledtext.ScrolledText(right, height=4, font=FNS,
                          bg=CARD, fg=FG2, relief="flat",
                          highlightbackground=BORDER, highlightthickness=1, state="disabled")
        self.data_disp.pack(fill="x", pady=(0, 6))

        section_label(right, "ГРАФІК РОЗПОДІЛУ (гістограма + Гаусс)")
        chart_f = tk.Frame(right, bg=BG)
        chart_f.pack(fill="both", expand=True)
        self.fig, self.ax = plt.subplots(figsize=(5, 3.5), dpi=96)
        self.fig.tight_layout(pad=2)
        self.canvas = embed_figure(self.fig, chart_f, toolbar=True)
        placeholder(self.ax, "Завантажте дані та натисніть «Розрахувати»")

    # ── МЕТОДИ ЛОГІКИ ────────────────────────────────────────────────────

    def _load_file(self):
        """Читає числові дані з текстового файлу (по одному значенню на рядок)."""
        path = filedialog.askopenfilename(title="Відкрити файл вимірювань",
               filetypes=[("Текстові файли", "*.txt"), ("Усі файли", "*.*")])
        if not path:
            return
        try:
            vals = []
            with open(path, encoding="utf-8") as f:
                for line in f:
                    s = line.strip()
                    # Ігноруємо порожні рядки та коментарі (починаються з #)
                    if s and not s.startswith("#"):
                        vals.append(float(s))
            self.data = vals
            self._show_data()
            log_write(self.log, f"✔ Прочитано {len(vals)} значень: {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def _generate(self):
        """Генерує псевдовипадковий набір гауссово розподілених чисел для тестування."""
        mu = random.uniform(1., 20.)
        sigma = random.uniform(0.02, 0.2) * mu
        n = random.randint(20, 50)
        self.data = [round(random.gauss(mu, sigma), 5) for _ in range(n)]
        self._show_data()
        log_write(self.log, f"✔ Згенеровано {n} значень (μ≈{mu:.3f}, σ≈{sigma:.4f})")

    def _apply_manual(self):
        """Зчитує значення з ручного текстового поля і зберігає в self.data."""
        raw = self.manual.get("1.0", "end").strip()
        if not raw:
            messagebox.showwarning("Увага", "Поле порожнє.")
            return
        try:
            vals = [float(x) for x in raw.splitlines() if x.strip()]
            if len(vals) < 2:
                raise ValueError("Мінімум 2 значення.")
            self.data = vals
            self._show_data()
            log_write(self.log, f"✔ Прийнято {len(vals)} значень.")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def _show_data(self):
        """Відображає масив self.data у текстовому полі (6 чисел на рядок)."""
        self.data_disp.configure(state="normal")
        self.data_disp.delete("1.0", "end")
        for i, v in enumerate(self.data):
            self.data_disp.insert("end", f"{v:12.5f}")
            if (i + 1) % 6 == 0:
                self.data_disp.insert("end", "\n")
        self.data_disp.configure(state="disabled")

    def _calculate(self):
        """
        Основний розрахунок статистики:
        n, x̄ (середнє), σ (відхилення), Δx̄ (похибка середнього),
        довірчий інтервал через t-критерій Стьюдента.
        """
        if len(self.data) < 2:
            messagebox.showwarning("Увага", "Спочатку завантажте дані.")
            return
        n = len(self.data)
        mean = sum(self.data) / n
        # Дисперсія (несмщена) — ділимо на (n-1) за формулою Бесселя
        var = sum((x - mean) ** 2 for x in self.data) / (n - 1)
        std = math.sqrt(var)
        dm = std / math.sqrt(n)       # Похибка середнього
        alpha = 1. - float(self.conf_var.get())
        t = self._student_t(n - 1, alpha)  # t-коефіцієнт для n-1 ступенів свободи
        delta = t * dm                # Довірчий інтервал

        # Зберігаємо для звіту
        self.last_stats = dict(n=n, mean=mean, std=std, dm=dm, delta=delta, t=t,
                               conf=float(self.conf_var.get()))

        # Оновлюємо мітки результатів
        self.rlbl["n"].config(text=str(n))
        self.rlbl["mean"].config(text=f"{mean:.5f}")
        self.rlbl["std"].config(text=f"{std:.5f}")
        self.rlbl["dm"].config(text=f"{dm:.5f}")
        self.rlbl["ci"].config(text=f"{delta:.5f}  (t={t:.3f})")
        self.rlbl["res"].config(text=f"({mean:.4f} ± {delta:.4f})", fg=CLR_RESULT)

        self._draw_histogram(mean, std)
        log_write(self.log, f"✔ x̄={mean:.5f}, σ={std:.5f}, Δ={delta:.5f}")

    def _draw_histogram(self, mean, std):
        """
        Малює гістограму розподілу і накладає теоретичну криву Гаусса.
        Кількість класів визначається за формулою Стерджеса: k = 1 + 3.322·log₁₀(n).
        """
        ax = self.ax
        ax.clear()
        data = np.array(self.data)
        n_bins = max(5, int(1 + 3.322 * math.log10(len(data))))
        # density=True нормує гістограму так, щоб площа = 1 (для порівняння з Гаусом)
        ax.hist(data, bins=n_bins, density=True, color=ACCENT, alpha=0.65,
                edgecolor=BORDER, linewidth=0.6)
        # Будуємо теоретичну криву Гаусса
        xs = np.linspace(data.min() - std, data.max() + std, 300)
        gauss = (1 / (std * np.sqrt(2 * math.pi))) * np.exp(-0.5 * ((xs - mean) / std) ** 2)
        ax.plot(xs, gauss, color=GREEN, linewidth=2, label="Гаусс")
        ax.axvline(mean, color=YELLOW, linewidth=1.5, linestyle="--", label=f"x̄={mean:.4f}")
        ax.axvspan(mean - std, mean + std, alpha=0.08, color=YELLOW, label="±σ")
        ax.set_xlabel("Значення")
        ax.set_ylabel("Щільність")
        ax.set_title("Гістограма розподілу + крива Гаусса", color=FG, pad=6)
        ax.legend(fontsize=7)
        ax.grid(True)
        self.fig.tight_layout(pad=1.5)
        self.canvas.draw()

    def _save_report(self):
        """Зберігає текстовий звіт із усіма результатами і масивом даних у .txt файл."""
        if not self.last_stats:
            messagebox.showwarning("Увага", "Спочатку виконайте розрахунок.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt",
               filetypes=[("Текстові файли", "*.txt")])
        if not path:
            return
        s = self.last_stats
        lines = ["=" * 52, "  ЗВІТ СТАТИСТИЧНОЇ ОБРОБКИ",
                 f"  Дата: {datetime.now():%Y-%m-%d %H:%M:%S}", "=" * 52,
                 f"  n={s['n']}, x̄={s['mean']:.6f}, σ={s['std']:.6f}",
                 f"  Δx̄={s['dm']:.6f}, γ={s['conf']}, t={s['t']:.3f}, Δ={s['delta']:.6f}", "",
                 f"  РЕЗУЛЬТАТ: ({s['mean']:.4f} ± {s['delta']:.4f})", "=" * 52, "",
                 "  Масив:"] + [f"  {i+1:3d}.  {v}" for i, v in enumerate(self.data)]
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        log_write(self.log, f"✔ Збережено: {os.path.basename(path)}")
        messagebox.showinfo("Успішно", f"Звіт збережено:\n{path}")

    @staticmethod
    def _student_t(df, alpha):
        """
        Повертає t-коефіцієнт Стьюдента для заданої кількості ступенів свободи (df)
        і рівня значущості (alpha = 1 - довірчий рівень).
        Таблиця вбудована безпосередньо (без scipy), щоб не потребувати зайвих бібліотек.
        """
        T = {
            0.10: {1:6.314, 2:2.920, 3:2.353, 4:2.132, 5:2.015, 6:1.943, 7:1.895,
                   8:1.860, 9:1.833, 10:1.812, 15:1.753, 20:1.725, 30:1.697, 60:1.671, 120:1.658},
            0.05: {1:12.706, 2:4.303, 3:3.182, 4:2.776, 5:2.571, 6:2.447, 7:2.365,
                   8:2.306, 9:2.262, 10:2.228, 15:2.131, 20:2.086, 30:2.042, 60:2.000, 120:1.980},
            0.01: {1:63.657, 2:9.925, 3:5.841, 4:4.604, 5:4.032, 6:3.707, 7:3.499,
                   8:3.355, 9:3.250, 10:3.169, 15:2.947, 20:2.845, 30:2.750, 60:2.660, 120:2.617}
        }
        row = T.get(alpha, T[0.05])
        keys = sorted(row)
        for k in keys:
            if df <= k:
                return row[k]
        return row[keys[-1]]  # Якщо df > 120, беремо граничне значення


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  ВКЛАДКА 2 — КІНЕМАТИКА                                                  ║
# ╚══════════════════════════════════════════════════════════════════════════╝
class KinematicsTab(tk.Frame):
    """
    Вкладка розрахунку траєкторії кидання тіла.
    Підтримує: кут, початкова швидкість, висота, сила тяжіння,
    опціонально — опір повітря (модель квадратичного тертя).
    Виводить: траєкторію y(x), графік швидкості v(t), прискорення a(t),
    таблицю даних і аналітику екстремумів/енергій.
    """
    def __init__(self, master):
        super().__init__(master, bg=BG)
        # Масиви точок траєкторії (заповнюються при розрахунку)
        self.xs = self.ys = self.ts = self.vxs = self.vys = []
        self.entries = {}   # Словник полів введення: ключ → Entry
        self._build()

    def _build(self):
        """Будує інтерфейс вкладки з лівою формою та правим блоком підвкладок."""
        pw = tk.PanedWindow(self, orient="horizontal", bg=BG, sashwidth=5)
        pw.pack(fill="both", expand=True, padx=6, pady=6)

        # ══ ЛІВА ПАНЕЛЬ — форма введення параметрів ════════════════════
        left = tk.Frame(pw, bg=BG, width=290)
        pw.add(left, minsize=255)

        # Grid для рівного вирівнювання підписів і полів
        inp = tk.Frame(left, bg=BG)
        inp.pack(fill="x", pady=(4, 0))
        inp.columnconfigure(1, weight=1)

        tk.Label(inp, text="ПАРАМЕТРИ", font=FHS, bg=BG, fg=FG2).grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(4, 4))

        # Визначення полів: (ключ, підпис, значення за замовчуванням, група конвертера, колір)
        fields = [
            ("v0",    "v₀ (м/с)",  "20",   "Швидкість", CLR_INPUT),
            ("angle", "α (°)",     "45",   None,         CLR_INPUT),
            ("h0",    "h₀ (м)",    "0",    "Довжина",    CLR_INPUT),
            ("g",     "g (м/с²)", "9.81",  None,         CLR_CONST),
        ]
        for i, (key, lbl, val, grp, clr) in enumerate(fields):
            tk.Label(inp, text="●", font=FNS, bg=BG, fg=clr).grid(row=i+1, column=0, padx=(0, 4), pady=3)
            tk.Label(inp, text=lbl, font=FNS, bg=BG, fg=FG2, anchor="w", width=9).grid(row=i+1, column=1, sticky="w")
            e = mkentry(inp, val, width=8, color=clr)
            e.grid(row=i+1, column=2, sticky="ew", padx=(4, 0))
            self.entries[key] = e
            # Кнопка виклику конвертера (тільки для полів з одиницями)
            if grp:
                def _popup(g=grp, k=key):
                    unit_popup(self, group_hint=g,
                               callback=lambda v, k=k: (self.entries[k].delete(0, "end"),
                                                        self.entries[k].insert(0, v)))
                tk.Button(inp, text="⚖", font=FNS, bg=PANEL, fg=YELLOW, relief="flat",
                          cursor="hand2", padx=2, command=_popup).grid(row=i+1, column=3, padx=(3, 0))

        # ── Блок опору повітря (розкривається/закривається) ─────────
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=6)
        air_hdr = tk.Frame(left, bg=BG)
        air_hdr.pack(fill="x")
        self.air_var = tk.BooleanVar(value=False)
        tk.Checkbutton(air_hdr, text="⚙ Опір повітря", variable=self.air_var,
                       bg=BG, fg=FG, selectcolor=CARD, activebackground=BG,
                       font=FN, command=self._toggle_air).pack(side="left")
        self.air_f = tk.Frame(left, bg=BG)
        air_inner = tk.Frame(self.air_f, bg=BG)
        air_inner.pack(fill="x")
        air_inner.columnconfigure(1, weight=1)
        for i, (key, lbl, val) in enumerate([("k", "k (кг/м)", "0.1"), ("mass", "m (кг)", "1.0")]):
            tk.Label(air_inner, text="●", font=FNS, bg=BG, fg=CLR_INPUT).grid(row=i, column=0, padx=(0, 4), pady=2)
            tk.Label(air_inner, text=lbl, font=FNS, bg=BG, fg=FG2, anchor="w", width=9).grid(row=i, column=1, sticky="w")
            e = mkentry(air_inner, val, width=8)
            e.grid(row=i, column=2, sticky="ew", padx=(4, 0))
            self.entries[key] = e

        # ── Кнопки дій ───────────────────────────────────────────────
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=(8, 4))
        mkbtn(left, "⚙️  РОЗРАХУВАТИ ТРАЄКТОРІЮ", self._calculate, ACCENT, big=True).pack(fill="x", pady=2)
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=4)
        mkbtn(left, "💾 Експортувати",        self._export,       GREEN).pack(fill="x", pady=2)
        mkbtn(left, "📂 Параметри з файлу",   self._load_params,  YELLOW).pack(fill="x", pady=2)
        mkbtn(left, "⚖ Конвертер одиниць",   lambda: unit_popup(self), PURPLE).pack(fill="x", pady=2)

        # ── Зведення (read-only поля швидкого погляду) ────────────────
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=(8, 2))
        tk.Label(left, text="ЗВЕДЕННЯ", font=FHS, bg=BG, fg=FG2).pack(anchor="w", pady=(2, 4))
        qs = tk.Frame(left, bg=BG)
        qs.pack(fill="x")
        qs.columnconfigure(1, weight=1)
        self.qv = {}
        for i, (k, lbl) in enumerate([("R", "Дальність (м)"), ("H", "Висота (м)"),
                                       ("T", "Час (с)"),       ("pts", "Точок")]):
            tk.Label(qs, text=lbl, font=FNS, bg=BG, fg=FG2, anchor="w").grid(row=i, column=0, sticky="w", pady=1)
            e = mk_ro_small(qs, "—", width=10)
            e.grid(row=i, column=1, sticky="ew", padx=(6, 0), pady=1)
            self.qv[k] = e

        section_label(left, "КОНСОЛЬ")
        self.log = make_log(left, height=9)

        # ══ ПРАВА ПАНЕЛЬ — підвкладки ══════════════════════════════════
        right = tk.Frame(pw, bg=BG)
        pw.add(right, minsize=500)
        nb_style()
        self.sub_nb = ttk.Notebook(right, style="Sub.TNotebook")
        self.sub_nb.pack(fill="both", expand=True)

        # — Підвкладка 1: Візуалізація (три графіки) ──────────────────
        vis_tab = tk.Frame(self.sub_nb, bg=BG)
        self.sub_nb.add(vis_tab, text="  📈  Візуалізація  ")
        self.fig, axes = plt.subplots(1, 3, figsize=(10, 3.8), dpi=90)
        self.ax_traj, self.ax_v, self.ax_a = axes
        self.fig.tight_layout(pad=2., w_pad=2.5)
        self.canvas_k = embed_figure(self.fig, vis_tab, toolbar=True)
        for ax, t in zip(axes, ["Траєкторія y(x)", "Швидкість v(t)", "Прискорення a(t)"]):
            placeholder(ax, t)

        # — Підвкладка 2: Таблиця даних ───────────────────────────────
        tbl_tab = tk.Frame(self.sub_nb, bg=BG)
        self.sub_nb.add(tbl_tab, text="  📋  Таблиця даних  ")
        tf = tk.Frame(tbl_tab, bg=BG)
        tf.pack(fill="both", expand=True, padx=4, pady=4)
        cols = ("t", "x", "y", "vx", "vy", "v", "a")
        self.tree = ttk.Treeview(tf, columns=cols, show="headings")
        style_tree(self.tree)
        for c, w, nm in zip(cols, [70, 85, 85, 85, 85, 85, 75],
                             ["t (с)", "X (м)", "Y (м)", "Vx (м/с)", "Vy (м/с)", "V (м/с)", "a (м/с²)"]):
            self.tree.heading(c, text=nm)
            self.tree.column(c, width=w, anchor="center")
        vsb = ttk.Scrollbar(tf, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tf, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tf.rowconfigure(0, weight=1)
        tf.columnconfigure(0, weight=1)

        # — Підвкладка 3: Аналітика ───────────────────────────────────
        ana_tab = tk.Frame(self.sub_nb, bg=BG)
        self.sub_nb.add(ana_tab, text="  🔬  Аналітика  ")
        self._build_analytics(ana_tab)

    def _build_analytics(self, parent):
        """Будує таблицю аналітичних показників (екстремуми, енергії) у вкладці Аналітика."""
        tk.Label(parent, text="Аналіз екстремумів та енергій",
                 font=FNB, bg=BG, fg=ACCENT).pack(pady=(12, 6))
        card = tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x", padx=12, pady=4)
        self.ana = {}
        rows = [("hmax",       "Максимальна висота H_max (м)"),
                ("xmax",       "Дальність польоту X (м)"),
                ("tmax",       "Час до макс. висоти (с)"),
                ("tfull",      "Повний час польоту (с)"),
                ("v_land",     "Швидкість приземлення (м/с)"),
                ("angle_land", "Кут приземлення (°)"),
                ("ek_max",     "Макс. кінетична енергія (Дж)"),
                ("ep_max",     "Макс. потенц. енергія (Дж)")]
        for i, (k, lbl) in enumerate(rows):
            bg = CARD if i % 2 == 0 else CARD2
            r = tk.Frame(card, bg=bg)
            r.pack(fill="x")
            tk.Label(r, text=lbl, font=FNS, bg=bg, fg=FG2, anchor="w", padx=10, pady=5, width=34).pack(side="left")
            v = tk.Label(r, text="—", font=FNB, bg=bg, fg=CLR_RESULT, anchor="e", padx=10)
            v.pack(side="right")
            self.ana[k] = v
        tk.Label(parent, text="* Для розрахунку енергії вкажіть масу у полі «m (кг)» (опір повітря)",
                 font=FNS, bg=BG, fg=FG2, wraplength=500).pack(pady=(8, 4))

    def _update_analytics(self, xs, ys, ts, vxs, vys, vs, g):
        """Оновлює мітки аналітики після розрахунку траєкторії."""
        imax = int(np.argmax(ys))
        hmax = max(ys)
        xend = xs[-1]
        tmax = ts[imax]
        tfull = ts[-1]
        v_land = vs[-1]
        vy_land = vys[-1]
        vx_land = vxs[-1]
        angle_land = abs(math.degrees(math.atan2(vy_land, vx_land)))
        m = 1.0  # Маса за замовчуванням
        try:
            m = float(self.entries.get("mass", type("_", (), {"get": lambda s: "1.0"})()).get())
        except:
            pass
        ek_max = 0.5 * m * max(vs) ** 2   # Ek = mv²/2
        ep_max = m * g * hmax              # Ep = mgh
        self.ana["hmax"].config(text=f"{hmax:.4f}")
        self.ana["xmax"].config(text=f"{xend:.4f}")
        self.ana["tmax"].config(text=f"{tmax:.4f}")
        self.ana["tfull"].config(text=f"{tfull:.4f}")
        self.ana["v_land"].config(text=f"{v_land:.4f}")
        self.ana["angle_land"].config(text=f"{angle_land:.2f}°")
        self.ana["ek_max"].config(text=f"{ek_max:.4f}")
        self.ana["ep_max"].config(text=f"{ep_max:.4f}")

    def _toggle_air(self):
        """Показує або приховує поля параметрів опору повітря."""
        if self.air_var.get():
            self.air_f.pack(fill="x", pady=2)
        else:
            self.air_f.pack_forget()

    def _calculate(self):
        """
        Числове інтегрування траєкторії методом Ейлера (крок dt=0.002 с).
        Без опору: ax=0, ay=-g.
        З опором: ax = -(k/m)*vx*|v|, ay = -g - (k/m)*vy*|v|.
        Зупиняється коли y ≤ 0 (приземлення).
        """
        try:
            v0 = float(self.entries["v0"].get())
            angle = math.radians(float(self.entries["angle"].get()))
            h0 = float(self.entries["h0"].get())
            g = float(self.entries["g"].get())
        except ValueError:
            messagebox.showerror("Помилка", "Перевірте параметри.")
            return

        use_air = self.air_var.get()
        k = m_ = 0.
        if use_air:
            try:
                k = float(self.entries["k"].get())
                m_ = float(self.entries["mass"].get())
            except:
                k, m_ = 0.1, 1.

        dt = 0.002   # Крок інтегрування (секунди)
        # Початкові складові швидкості
        vx = v0 * math.cos(angle)
        vy = v0 * math.sin(angle)
        xs = [0.]; ys = [h0]; ts = [0.]; vxs = [vx]; vys = [vy]
        x = 0.; y = h0; t = 0.

        for _ in range(200_000):  # Захист від нескінченного циклу
            vm = math.sqrt(vx ** 2 + vy ** 2)
            if use_air and vm > 0:
                ax_ = -(k / m_) * vx * vm
                ay_ = -g - (k / m_) * vy * vm
            else:
                ax_ = 0.
                ay_ = -g
            vx += ax_ * dt; vy += ay_ * dt
            x += vx * dt;   y += vy * dt
            t += dt
            xs.append(round(x, 5)); ys.append(round(y, 5))
            ts.append(round(t, 5)); vxs.append(round(vx, 5)); vys.append(round(vy, 5))
            if y <= 0 and t > 0.01:  # Тіло досягло землі
                break

        self.xs, self.ys, self.ts, self.vxs, self.vys = xs, ys, ts, vxs, vys
        vs = [math.sqrt(a ** 2 + b ** 2) for a, b in zip(vxs, vys)]
        accs = [abs(g)] + [abs((vs[i] - vs[i-1]) / dt) for i in range(1, len(vs))]

        # Оновлюємо зведення
        set_ro(self.qv["R"], f"{xs[-1]:.3f}")
        set_ro(self.qv["H"], f"{max(ys):.3f}")
        set_ro(self.qv["T"], f"{ts[-1]:.3f}")
        set_ro(self.qv["pts"], str(len(xs)))

        self._draw_charts(xs, ys, ts, vs, accs)
        self._fill_table(xs, ys, ts, vxs, vys, vs, accs)
        self._update_analytics(xs, ys, ts, vxs, vys, vs, g)
        mode = "з опором" if use_air else "без опору"
        log_write(self.log, f"✔ {len(xs)} точок ({mode}). R={xs[-1]:.2f} м, T={ts[-1]:.3f} с")

    def _draw_charts(self, xs, ys, ts, vs, accs):
        """Перемальовує три графіки: траєкторія, швидкість, прискорення."""
        xa, ya, ta = np.array(xs), np.array(ys), np.array(ts)
        va, aa = np.array(vs), np.array(accs)

        # Графік 1: траєкторія y(x)
        ax = self.ax_traj; ax.clear()
        ax.plot(xa, ya, color=ACCENT, linewidth=1.8)
        ax.fill_between(xa, ya, alpha=0.12, color=ACCENT)
        ax.set_xlabel("x (м)"); ax.set_ylabel("y (м)")
        ax.set_title("Траєкторія y(x)", color=FG, pad=4); ax.grid(True)
        imax = int(np.argmax(ya))
        ax.plot(xa[imax], ya[imax], "o", color=YELLOW, markersize=5)
        ax.annotate(f"H={ya[imax]:.2f}", xy=(xa[imax], ya[imax]), xytext=(0, 8),
                    textcoords="offset points", color=YELLOW, fontsize=7, ha="center")

        # Графік 2: швидкість v(t)
        ax = self.ax_v; ax.clear()
        ax.plot(ta, va, color=GREEN, linewidth=1.8)
        ax.set_xlabel("t (с)"); ax.set_ylabel("v (м/с)")
        ax.set_title("Швидкість v(t)", color=FG, pad=4); ax.grid(True)

        # Графік 3: прискорення a(t)
        ax = self.ax_a; ax.clear()
        ax.plot(ta, aa, color=RED, linewidth=1.5)
        ax.set_xlabel("t (с)"); ax.set_ylabel("a (м/с²)")
        ax.set_title("Прискорення a(t)", color=FG, pad=4); ax.grid(True)

        self.fig.tight_layout(pad=1.5, w_pad=2.)
        self.canvas_k.draw()

    def _fill_table(self, xs, ys, ts, vxs, vys, vs, accs):
        """
        Заповнює таблицю даних. Щоб таблиця не містила 200k рядків,
        показуємо кожен step-й рядок (максимум ~80 рядків).
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
        step = max(1, len(xs) // 80)
        for i in range(0, len(xs), step):
            self.tree.insert("", "end", values=(
                f"{ts[i]:.3f}", f"{xs[i]:.3f}", f"{ys[i]:.3f}",
                f"{vxs[i]:.3f}", f"{vys[i]:.3f}", f"{vs[i]:.3f}", f"{accs[i]:.3f}"))

    def _export(self):
        """Зберігає всі точки траєкторії у CSV файл для подальшого аналізу."""
        if not self.xs:
            messagebox.showwarning("Увага", "Спочатку виконайте розрахунок.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv",
               filetypes=[("CSV", "*.csv"), ("TXT", "*.txt")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write("t(s),X(m),Y(m),Vx(m/s),Vy(m/s),V(m/s)\n")
            for i in range(len(self.xs)):
                v = math.sqrt(self.vxs[i] ** 2 + self.vys[i] ** 2)
                f.write(f"{self.ts[i]:.5f},{self.xs[i]:.5f},{self.ys[i]:.5f},"
                        f"{self.vxs[i]:.5f},{self.vys[i]:.5f},{v:.5f}\n")
        log_write(self.log, f"✔ {len(self.xs)} точок → {os.path.basename(path)}")
        messagebox.showinfo("Успішно", f"Збережено:\n{path}")

    def _load_params(self):
        """
        Завантажує параметри з текстового файлу формату key=value.
        Рядки, що починаються з #, ігноруються як коментарі.
        """
        path = filedialog.askopenfilename(
               filetypes=[("Текстові файли", "*.txt"), ("Усі файли", "*.*")])
        if not path:
            return
        try:
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip().lower(); v = v.strip()
                        if k in self.entries:
                            self.entries[k].delete(0, "end")
                            self.entries[k].insert(0, v)
            log_write(self.log, f"✔ Параметри з: {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))


# ── Допоміжні функції для read-only Entry у вкладці Кінематика ─────────────

def mk_ro_small(parent, val, width=10):
    """Маленьке read-only поле (для зведення у лівій панелі Кінематики)."""
    e = tk.Entry(parent, font=FNB, bg=CARD2, fg=CLR_RESULT, relief="flat",
                 highlightbackground=BORDER, highlightthickness=1,
                 width=width, state="readonly")
    return e

def set_ro(widget, val):
    """Оновлює значення read-only поля (тимчасово знімає заборону редагування)."""
    widget.configure(state="normal")
    widget.delete(0, "end")
    widget.insert(0, val)
    widget.configure(state="readonly")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  ВКЛАДКА 3 — ДОВІДНИК КОНСТАНТ                                           ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# База фундаментальних констант: (символ, назва, SI-значення, SI-одиниця, СГС-значення, СГС-одиниця)
CONSTANTS = {
    "Механіка / Гравітація": [
        ("g",  "Прискорення вільного падіння", "9.80665",    "м/с²",       "9.80665e2", "Гал"),
        ("G",  "Стала гравітації",             "6.67430e-11","м³/(кг·с²)", "6.67430e-8","см³/(г·с²)"),
    ],
    "Електромагнетизм": [
        ("c",  "Швидкість світла",   "299792458",  "м/с",   "2.99792458e10","см/с"),
        ("e",  "Заряд електрона",    "1.60218e-19","Кл",    "4.80326e-10",  "ед. СГС"),
        ("ε₀", "Електрична стала",   "8.85419e-12","Ф/м",   "—",            "—"),
        ("μ₀", "Магнітна стала",     "1.25664e-6", "Гн/м",  "—",            "—"),
    ],
    "Термодинаміка": [
        ("kB", "Стала Больцмана",         "1.38065e-23","Дж/К",       "1.38065e-16","ерг/К"),
        ("R",  "Газова стала",            "8.31446",    "Дж/(моль·К)","8.31446e7",  "ерг/(моль·К)"),
        ("NA", "Число Авоґадро",          "6.02214e23", "моль⁻¹",     "6.02214e23", "моль⁻¹"),
        ("σ",  "Стала Стефана-Больцмана", "5.67037e-8", "Вт/(м²·К⁴)","5.67037e-5", "ерг/(с·см²·К⁴)"),
    ],
    "Квантова фізика": [
        ("h",  "Стала Планка",          "6.62607e-34","Дж·с","6.62607e-27","ерг·с"),
        ("ℏ",  "Зведена стала Планка",  "1.05457e-34","Дж·с","1.05457e-27","ерг·с"),
        ("me", "Маса електрона",        "9.10938e-31","кг",  "9.10938e-28","г"),
        ("mp", "Маса протона",          "1.67262e-27","кг",  "1.67262e-24","г"),
        ("a₀", "Боровський радіус",     "5.29177e-11","м",   "5.29177e-9", "см"),
        ("α",  "Стала тонкої структури","7.29735e-3", "—",   "7.29735e-3", "—"),
    ],
    "Атомна/Ядерна": [
        ("u",  "Атомна одиниця маси",   "1.66054e-27","кг",  "1.66054e-24","г"),
        ("eV", "Електронвольт",         "1.60218e-19","Дж",  "1.60218e-12","ерг"),
        ("re", "Класичний радіус е",    "2.81794e-15","м",   "2.81794e-13","см"),
    ],
}

class ConstantsTab(tk.Frame):
    """
    Вкладка-довідник фундаментальних фізичних констант.
    Підтримує: пошук у реальному часі, перемикання SI ↔ СГС,
    копіювання значення у буфер обміну.
    """
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.si_mode = tk.BooleanVar(value=True)  # True = SI, False = СГС
        self._build()

    def _build(self):
        """Будує заголовок, рядок пошуку, таблицю та нижню панель дій."""
        # Sticky заголовок (не прокручується разом з таблицею)
        hdr = tk.Frame(self, bg=PANEL)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📚  Довідник фундаментальних констант",
                 font=FNB, bg=PANEL, fg=ACCENT).pack(side="left", padx=10, pady=7)
        tk.Label(hdr, text="Система:", font=FNS, bg=PANEL, fg=FG2).pack(side="right", padx=(0, 6))
        tk.Radiobutton(hdr, text="СГС", variable=self.si_mode, value=False, bg=PANEL, fg=FG,
                       selectcolor=CARD, activebackground=PANEL, font=FN,
                       command=self._refresh).pack(side="right")
        tk.Radiobutton(hdr, text="SI", variable=self.si_mode, value=True, bg=PANEL, fg=ACCENT,
                       selectcolor=CARD, activebackground=PANEL, font=FNB,
                       command=self._refresh).pack(side="right")

        # Рядок пошуку — завжди видимий (sticky)
        sf = tk.Frame(self, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        sf.pack(fill="x", padx=6, pady=4)
        tk.Label(sf, text="🔍", font=FN, bg=CARD, fg=ACCENT).pack(side="left", padx=(8, 4), pady=4)
        self.search_var = tk.StringVar()
        # trace_add — викликає _refresh при кожній зміні пошукового рядка
        self.search_var.trace_add("write", lambda *_: self._refresh())
        tk.Entry(sf, textvariable=self.search_var, font=FN, bg=CARD, fg=FG,
                 insertbackground=ACCENT, relief="flat", bd=0).pack(
                 side="left", fill="x", expand=True, pady=4, padx=(0, 8))
        tk.Button(sf, text="✖", font=FNS, bg=CARD, fg=FG2, relief="flat", cursor="hand2",
                  command=lambda: (self.search_var.set(""), self._refresh())).pack(side="right", padx=4)

        # Таблиця констант
        tf = tk.Frame(self, bg=BG)
        tf.pack(fill="both", expand=True, padx=6, pady=2)
        cols = ("sym", "name", "value", "unit")
        self.tree = ttk.Treeview(tf, columns=cols, show="headings")
        style_tree(self.tree)
        for c, w, nm in zip(cols, [60, 230, 165, 210], ["Симв.", "Назва", "Значення", "Одиниця"]):
            self.tree.heading(c, text=nm)
            self.tree.column(c, width=w, anchor="w")
        vsb = ttk.Scrollbar(tf, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        # Подвійний клік = копіювати значення
        self.tree.bind("<Double-1>", lambda _: self._copy_selected())
        self.tree.bind("<ButtonRelease-1>", self._on_select)

        # Нижня панель (статус і кнопка копіювання)
        bot = tk.Frame(self, bg=PANEL)
        bot.pack(fill="x")
        self.detail_lbl = tk.Label(bot, text="Двічі клацніть — скопіювати значення в буфер",
                                    font=FNS, bg=PANEL, fg=FG2, anchor="w")
        self.detail_lbl.pack(side="left", padx=10, pady=6)
        mkbtn(bot, "📋 Копіювати", self._copy_selected, ACCENT).pack(side="right", padx=8, pady=4)
        self._refresh()

    def _refresh(self):
        """Перезаповнює таблицю з урахуванням поточного пошукового запиту та системи одиниць."""
        q = self.search_var.get().lower()
        si = self.si_mode.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for group, consts in CONSTANTS.items():
            tag_grp = True  # Заголовок групи показуємо один раз
            for sym, name, val_si, unit_si, val_cgs, unit_cgs in consts:
                val = val_si if si else val_cgs
                unit = unit_si if si else unit_cgs
                row = (sym, name, val, unit)
                # Фільтруємо: якщо рядок пошуку не порожній — перевіряємо всі поля
                if q and not any(q in str(x).lower() for x in row):
                    continue
                if tag_grp:
                    self.tree.insert("", "end", values=("", "── " + group + " ──", "", ""), tags=("grp",))
                    tag_grp = False
                self.tree.insert("", "end", values=row, tags=("row",))
        self.tree.tag_configure("grp", foreground=YELLOW)  # Заголовки груп — жовті
        self.tree.tag_configure("row", foreground=FG)

    def _on_select(self, _):
        """Показує деталі вибраного рядка у нижній панелі."""
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])["values"]
        if vals and vals[0]:
            self.detail_lbl.config(
                text=f"{vals[0]}  {vals[1]}  =  {vals[2]}  {vals[3]}", fg=ACCENT)

    def _copy_selected(self):
        """Копіює числове значення вибраної константи у буфер обміну."""
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])["values"]
        if vals and vals[2]:
            self.clipboard_clear()
            self.clipboard_append(str(vals[2]))
            self.detail_lbl.config(text=f"✔ Скопійовано: {vals[2]}", fg=GREEN)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  ВКЛАДКА 4 — ПОШИРЕННЯ ПОХИБОК                                           ║
# ╚══════════════════════════════════════════════════════════════════════════╝
class ErrorPropTab(tk.Frame):
    """
    Вкладка розрахунку похибок за формулою поширення невизначеності.
    Використовує sympy для символьного диференціювання:
    Δf = sqrt( Σ (∂f/∂xᵢ · Δxᵢ)² )
    """
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.var_rows: list[dict] = []   # Список рядків змінних (sym, val_e, err_e)
        self._last_result = None          # Останній результат (для збереження)
        self._build()

    def _build(self):
        """Будує ліву панель (формула + змінні) і праву (результат + внески)."""
        pw = tk.PanedWindow(self, orient="horizontal", bg=BG, sashwidth=4)
        pw.pack(fill="both", expand=True, padx=6, pady=6)
        left = tk.Frame(pw, bg=BG, width=340)
        pw.add(left, minsize=280)

        # Поле введення формули
        section_label(left, "ФОРМУЛА", pady_top=4)
        tk.Label(left, text="Введіть через sympy:", font=FNS, bg=BG, fg=FG2).pack(anchor="w")
        self.formula_e = tk.Entry(left, font=FN, bg=CARD, fg=CLR_INPUT,
                                   insertbackground=CLR_INPUT, relief="flat",
                                   highlightbackground=CLR_INPUT, highlightthickness=1)
        self.formula_e.insert(0, "U/I")
        self.formula_e.pack(fill="x", pady=4)

        # Кнопки-приклади для швидкого вибору формули
        ex_f = tk.Frame(left, bg=BG)
        ex_f.pack(fill="x", pady=2)
        tk.Label(ex_f, text="Приклади:", font=FNS, bg=BG, fg=FG2).pack(side="left")
        for ex in ["U/I", "m*v**2/2", "2*pi*sqrt(l/g)", "rho*v**2/2"]:
            tk.Button(ex_f, text=ex, font=FNS, bg=PANEL, fg=YELLOW, relief="flat", cursor="hand2",
                      padx=3, command=lambda x=ex: (self.formula_e.delete(0, "end"),
                                                    self.formula_e.insert(0, x),
                                                    self._parse_vars())).pack(side="left", padx=2)

        mkbtn(left, "🔍 Розпізнати змінні", self._parse_vars, YELLOW).pack(fill="x", pady=4)

        # Canvas зі скролбаром для динамічної кількості змінних
        section_label(left, "ЗМІННІ ТА ЇХ ПОХИБКИ")
        vars_outer = tk.Frame(left, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        vars_outer.pack(fill="x", pady=2)
        self.vars_canvas = tk.Canvas(vars_outer, bg=CARD, highlightthickness=0, height=140)
        vars_vsb = ttk.Scrollbar(vars_outer, orient="vertical", command=self.vars_canvas.yview)
        self.vars_canvas.configure(yscrollcommand=vars_vsb.set)
        self.vars_canvas.pack(side="left", fill="both", expand=True)
        vars_vsb.pack(side="right", fill="y")
        # Внутрішній фрейм для розміщення рядків змінних
        self.vars_inner = tk.Frame(self.vars_canvas, bg=CARD)
        self._vars_window = self.vars_canvas.create_window((0, 0), window=self.vars_inner, anchor="nw")
        self.vars_inner.bind("<Configure>", self._on_vars_configure)
        self.vars_canvas.bind("<Configure>", self._on_canvas_resize)

        # Кнопки дій
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=(8, 4))
        mkbtn(left, "⚙️  РОЗРАХУВАТИ ПОХИБКУ", self._calculate, ACCENT, big=True).pack(fill="x", pady=2)
        tk.Frame(left, bg=BORDER, height=1).pack(fill="x", pady=4)
        mkbtn(left, "💾 Зберегти результат", self._save, GREEN).pack(fill="x", pady=2)

        # ── Права панель ─────────────────────────────────────────────────
        right = tk.Frame(pw, bg=BG)
        pw.add(right, minsize=420)

        # Hero-блок результату (великий шрифт)
        res_hero = tk.Frame(right, bg="#0a1628",
                            highlightbackground=CLR_RESULT, highlightthickness=2)
        res_hero.pack(fill="x", padx=0, pady=(0, 8))
        tk.Label(res_hero, text="РЕЗУЛЬТАТ", font=FHS, bg="#0a1628", fg=FG2).pack(pady=(8, 0))
        self.hero_lbl = tk.Label(res_hero, text="f  =  ( — ± — )",
                                  font=FBIG, bg="#0a1628", fg=CLR_RESULT)
        self.hero_lbl.pack(pady=(2, 4))
        sub_row = tk.Frame(res_hero, bg="#0a1628")
        sub_row.pack(pady=(0, 8))
        tk.Label(sub_row, text="Δf =", font=FNB, bg="#0a1628", fg=FG2).pack(side="left", padx=(12, 4))
        self.hero_df = tk.Label(sub_row, text="—", font=FNB, bg="#0a1628", fg=RED)
        self.hero_df.pack(side="left")
        tk.Label(sub_row, text="   δf =", font=FNB, bg="#0a1628", fg=FG2).pack(side="left", padx=(12, 4))
        self.hero_rel = tk.Label(sub_row, text="—", font=FNB, bg="#0a1628", fg=YELLOW)
        self.hero_rel.pack(side="left")

        # Символьний вираз для Δf
        section_label(right, "СИМВОЛЬНИЙ ВИРАЗ")
        self.sym_disp = scrolledtext.ScrolledText(right, height=9, font=FNS, bg=CARD, fg=PURPLE,
                          relief="flat", highlightbackground=BORDER, highlightthickness=1,
                          state="disabled", wrap="word")
        self.sym_disp.pack(fill="x", pady=(0, 6))

        # Таблиця внесків кожної змінної
        section_label(right, "ВНЕСОК КОЖНОЇ ЗМІННОЇ")
        cf = tk.Frame(right, bg=BG)
        cf.pack(fill="both", expand=True)
        cols = ("var", "val", "err", "deriv", "contrib", "pct")
        self.ctree = ttk.Treeview(cf, columns=cols, show="headings")
        style_tree(self.ctree)
        for c, w, nm in zip(cols, [50, 90, 80, 130, 100, 70],
                             ["Змін.", "Значення", "Похибка", "∂f/∂x", "Внесок Δfᵢ", "%"]):
            self.ctree.heading(c, text=nm)
            self.ctree.column(c, width=w, anchor="center")
        vsb2 = ttk.Scrollbar(cf, orient="vertical", command=self.ctree.yview)
        self.ctree.configure(yscrollcommand=vsb2.set)
        self.ctree.pack(side="left", fill="both", expand=True)
        vsb2.pack(side="right", fill="y")

        section_label(right, "КОНСОЛЬ")
        self.log = make_log(right, height=6)

    def _on_vars_configure(self, _):
        """Оновлює scrollregion canvas при зміні розміру внутрішнього фрейму."""
        self.vars_canvas.configure(scrollregion=self.vars_canvas.bbox("all"))

    def _on_canvas_resize(self, event):
        """Розтягує внутрішній фрейм на всю ширину canvas при зміні розміру вікна."""
        self.vars_canvas.itemconfig(self._vars_window, width=event.width)

    @staticmethod
    def _safe_sympify(fs):
        """
        Безпечна версія sp.sympify: перевизначає зарезервовані назви (I, E, S тощо),
        щоб вони трактувались як звичайні символи, а не вбудовані константи sympy.
        """
        reserved = {n: sp.Symbol(n) for n in ("I", "E", "S", "N", "Q", "C", "O")}
        return sp.sympify(fs, locals=reserved)

    def _parse_vars(self):
        """Аналізує формулу і автоматично створює рядки для введення змінних та їх похибок."""
        fs = self.formula_e.get().strip()
        if not fs:
            return
        try:
            expr = self._safe_sympify(fs)
            # Отримуємо всі вільні символи та сортуємо за іменем
            syms = sorted(expr.free_symbols, key=lambda s: s.name)
        except Exception as e:
            messagebox.showerror("Помилка sympy", str(e))
            return

        # Очищаємо попередні рядки
        for w in self.vars_inner.winfo_children():
            w.destroy()
        self.var_rows.clear()

        # Заголовок таблиці змінних
        hdr = tk.Frame(self.vars_inner, bg=PANEL)
        hdr.pack(fill="x", pady=(0, 1))
        hdr.columnconfigure(1, weight=1)
        hdr.columnconfigure(2, weight=1)
        for c, (t, w) in enumerate([("Змінна", 8), ("Значення", 12), ("Похибка Δ", 12)]):
            tk.Label(hdr, text=t, font=FHS, bg=PANEL, fg=FG2, width=w).grid(row=0, column=c, padx=4, pady=3)

        # Створюємо рядок для кожного символу
        for sym in syms:
            row = tk.Frame(self.vars_inner, bg=CARD2)
            row.pack(fill="x", pady=1)
            tk.Label(row, text=sym.name, font=FNB, bg=CARD2, fg=ACCENT,
                     width=8, anchor="center").grid(row=0, column=0, padx=4, pady=3)
            ve = mkentry(row, "1.0", width=12, color=CLR_INPUT)
            ve.grid(row=0, column=1, padx=4, pady=3)
            de = mkentry(row, "0.01", width=12, color=CLR_INPUT)
            de.grid(row=0, column=2, padx=4, pady=3)
            self.var_rows.append({"sym": sym, "val_e": ve, "err_e": de})

        log_write(self.log, f"✔ Знайдено: {[s.name for s in syms]}")

    def _calculate(self):
        """
        Розраховує f та Δf за формулою поширення похибок:
        Δf = sqrt( Σ (∂f/∂xᵢ · Δxᵢ)² )
        Використовує sympy для точного символьного диференціювання.
        """
        fs = self.formula_e.get().strip()
        if not fs:
            messagebox.showwarning("Увага", "Введіть формулу.")
            return
        if not self.var_rows:
            self._parse_vars()
        if not self.var_rows:
            return
        try:
            expr = self._safe_sympify(fs)
            subs_val = {}   # Словник: символ → числове значення
            subs_err = {}   # Словник: символ → похибка
            for row in self.var_rows:
                subs_val[row["sym"]] = float(row["val_e"].get())
                subs_err[row["sym"]] = float(row["err_e"].get())

            # Символьні часткові похідні
            derivs = {row["sym"]: sp.diff(expr, row["sym"]) for row in self.var_rows}

            # Числове значення функції
            f_val = float(sp.re(expr.subs(subs_val)))

            # Квадратура: Δf² = Σ (∂f/∂xᵢ · Δxᵢ)²
            df_sq = 0.0
            for sym, d in derivs.items():
                d_num = complex(d.subs(subs_val)).real
                df_sq += (d_num * subs_err[sym]) ** 2
            df_val = math.sqrt(abs(df_sq))

            # Відносна похибка у відсотках
            df_rel = abs(df_val / f_val) * 100 if f_val != 0 else float("inf")

            # Оновлюємо hero-блок
            self.hero_lbl.config(text=f"f  =  ( {f_val:.4g} ± {df_val:.4g} )")
            self.hero_df.config(text=f"{df_val:.6g}")
            self.hero_rel.config(text=f"{df_rel:.3f} %")

            # Формуємо символьний текст у поле
            self.sym_disp.configure(state="normal")
            self.sym_disp.delete("1.0", "end")
            self.sym_disp.insert("end", f"f = {fs}\n\nΔf = sqrt(\n")
            for sym, d in derivs.items():
                self.sym_disp.insert("end",
                    f"  (∂f/∂{sym.name} · Δ{sym.name})²\n"
                    f"  де ∂f/∂{sym.name} = {sp.simplify(d)}\n\n")
            self.sym_disp.insert("end", ")")
            self.sym_disp.configure(state="disabled")

            # Заповнюємо таблицю внесків (відсортовано за спаданням внеску)
            for item in self.ctree.get_children():
                self.ctree.delete(item)
            contribs = []
            for sym in subs_val:
                d_num = complex(derivs[sym].subs(subs_val)).real
                contrib = abs(d_num * subs_err[sym])
                contribs.append((sym.name, subs_val[sym], subs_err[sym], d_num, contrib))
            total_c = sum(c[4] for c in contribs) or 1
            for name, val, err, d_num, contrib in sorted(contribs, key=lambda x: -x[4]):
                pct = contrib / total_c * 100
                self.ctree.insert("", "end", values=(
                    name, f"{val:.4g}", f"{err:.4g}", f"{d_num:.4g}", f"{contrib:.4g}", f"{pct:.1f}"))

            self._last_result = dict(formula=fs, f=f_val, df=df_val, rel=df_rel, vars=contribs)
            log_write(self.log, f"✔ f={f_val:.5g}, Δf={df_val:.5g}, δf={df_rel:.3f}%")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def _save(self):
        """Зберігає звіт розрахунку похибок у текстовий файл."""
        if not self._last_result:
            messagebox.showwarning("Увага", "Спочатку виконайте розрахунок.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt",
               filetypes=[("Текстові файли", "*.txt")])
        if not path:
            return
        r = self._last_result
        lines = ["=" * 52, "  ЗВІТ ПОШИРЕННЯ ПОХИБОК",
                 f"  Дата: {datetime.now():%Y-%m-%d %H:%M:%S}", "=" * 52,
                 f"  Формула: f = {r['formula']}",
                 f"  f = {r['f']:.6g}",
                 f"  Δf = {r['df']:.6g}",
                 f"  δf = {r['rel']:.3f} %",
                 f"  Результат: ({r['f']:.4g} ± {r['df']:.4g})",
                 "", "  Змінні:"] + \
                [f"    {n}: x={v:.4g}, Δx={e:.4g}, ∂f/∂x={d:.4g}, внесок={c:.4g}"
                 for n, v, e, d, c in r["vars"]]
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        log_write(self.log, f"✔ Збережено: {os.path.basename(path)}")
        messagebox.showinfo("Успішно", f"Збережено:\n{path}")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  ВКЛАДКА 5 — КОНВЕРТЕР ОДИНИЦЬ                                           ║
# ╚══════════════════════════════════════════════════════════════════════════╝
class ConverterTab(tk.Frame):
    """
    Повнофункціональна вкладка конвертера одиниць.
    Підтримує: швидкість, довжину, масу, час, енергію, тиск, температуру, кути.
    Автоматично перераховує при зміні значення або одиниці.
    """
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self._result_str = ""   # Рядок результату для копіювання
        self._build()

    def _build(self):
        """Будує інтерфейс конвертера: заголовок, grid "звідки/куди", таблиця множників."""
        tk.Label(self, text="⚖  Конвертер одиниць вимірювання",
                 font=("Courier New", 14, "bold"), bg=BG, fg=ACCENT).pack(pady=(14, 2))

        # Grid-блок: 2 колонки "звідки" і "куди" зі стрілкою між ними
        grid_f = tk.Frame(self, bg=BG)
        grid_f.pack(padx=20, pady=8, fill="x")
        grid_f.columnconfigure(0, weight=1, uniform="col")
        grid_f.columnconfigure(1, weight=0)
        grid_f.columnconfigure(2, weight=1, uniform="col")

        # Вибір категорії (над grid-блоком)
        cat_f = tk.Frame(self, bg=BG)
        cat_f.pack(pady=(0, 6))
        tk.Label(cat_f, text="Категорія:", font=FN, bg=BG, fg=FG2).pack(side="left")
        self.grp_var = tk.StringVar(value=list(UNIT_GROUPS.keys())[0])
        grp_cb = ttk.Combobox(cat_f, textvariable=self.grp_var,
                               values=list(UNIT_GROUPS.keys()),
                               font=FN, state="readonly", width=16)
        grp_cb.pack(side="left", padx=8)
        grp_cb.bind("<<ComboboxSelected>>", self._refresh_units)

        # Ліва картка "ЗВІДКИ"
        left_f = tk.Frame(grid_f, bg=CARD, highlightbackground=CLR_INPUT, highlightthickness=1)
        left_f.grid(row=0, column=0, sticky="nsew", padx=(0, 6), ipady=10)
        tk.Label(left_f, text="● ЗВІДКИ", font=FNB, bg=CARD, fg=CLR_INPUT).pack(pady=(10, 4))
        dot_label(left_f, CLR_INPUT, "Значення:").pack()
        self.val_e = mkentry(left_f, "1.0", width=16, color=CLR_INPUT)
        self.val_e.pack(pady=4, padx=12)
        tk.Label(left_f, text="Одиниця:", font=FNS, bg=CARD, fg=FG2).pack()
        self.from_cb = ttk.Combobox(left_f, font=FN, state="readonly", width=14)
        self.from_cb.pack(pady=4, padx=12)

        # Стрілка між картками
        tk.Label(grid_f, text="→", font=("Courier New", 24, "bold"),
                 bg=BG, fg=YELLOW).grid(row=0, column=1, padx=8)

        # Права картка "КУДИ"
        right_f = tk.Frame(grid_f, bg=CARD2, highlightbackground=CLR_RESULT, highlightthickness=1)
        right_f.grid(row=0, column=2, sticky="nsew", padx=(6, 0), ipady=10)
        tk.Label(right_f, text="● КУДИ", font=FNB, bg=CARD2, fg=CLR_RESULT).pack(pady=(10, 4))
        dot_label(right_f, CLR_RESULT, "Результат:").pack()
        self.result_val = tk.Label(right_f, text="—", font=("Courier New", 16, "bold"),
                                    bg=CARD2, fg=CLR_RESULT)
        self.result_val.pack(pady=4)
        tk.Label(right_f, text="Одиниця:", font=FNS, bg=CARD2, fg=FG2).pack()
        self.to_cb = ttk.Combobox(right_f, font=FN, state="readonly", width=14)
        self.to_cb.pack(pady=4, padx=12)

        # Рядок кнопок
        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(pady=6)
        mkbtn(btn_row, "⚙️  Конвертувати", self._convert, ACCENT, bold=True).pack(side="left", padx=6)
        mkbtn(btn_row, "📋 Скопіювати", self._copy, GREEN).pack(side="left", padx=6)

        # Рядок повного рівняння
        self.eq_lbl = tk.Label(self, text="", font=FH, bg=BG, fg=FG2)
        self.eq_lbl.pack(pady=2)

        # Блок швидких перетворень (кнопки-ярлики)
        section_label(self, "ШВИДКІ ПЕРЕТВОРЕННЯ")
        qf = tk.Frame(self, bg=BG)
        qf.pack(pady=4)
        quicks = [
            ("км/год→м/с", "Швидкість",    "км/год", "м/с"),
            ("°C→K",       "Температура",   "°C",     "K"),
            ("еВ→Дж",      "Енергія",       "еВ",     "Дж"),
            ("атм→Па",     "Тиск",          "атм",    "Па"),
            ("°→рад",      "Кут",           "°",      "рад"),
            ("фут→м",      "Довжина",       "фут",    "м"),
        ]
        for lbl, grp, fu, tu in quicks:
            def _q(g=grp, f=fu, t=tu):
                self.grp_var.set(g)
                self._refresh_units()
                self.from_cb.set(f)
                self.to_cb.set(t)
                self._convert()
            tk.Button(qf, text=lbl, font=FNS, bg=CARD, fg=YELLOW, relief="flat", cursor="hand2",
                      padx=8, pady=4, highlightbackground=BORDER, highlightthickness=1,
                      command=_q).pack(side="left", padx=3, pady=2)

        # Таблиця множників (1 базова одиниця → решта)
        section_label(self, "ТАБЛИЦЯ (1 одиниця → решта)")
        tf = tk.Frame(self, bg=BG)
        tf.pack(fill="both", expand=True, padx=8, pady=4)
        cols = ("from", "to", "factor")
        self.tab = ttk.Treeview(tf, columns=cols, show="headings", height=6)
        style_tree(self.tab)
        for c, w, nm in zip(cols, [140, 140, 230], ["З", "В", "Множник"]):
            self.tab.heading(c, text=nm)
            self.tab.column(c, width=w, anchor="center")
        vsb = ttk.Scrollbar(tf, orient="vertical", command=self.tab.yview)
        self.tab.configure(yscrollcommand=vsb.set)
        self.tab.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Ініціалізація та прив'язка подій
        self._refresh_units()
        self.val_e.bind("<KeyRelease>", lambda _: self._convert())
        self.from_cb.bind("<<ComboboxSelected>>", lambda _: self._convert())
        self.to_cb.bind("<<ComboboxSelected>>", lambda _: self._convert())

    def _refresh_units(self, *_):
        """Оновлює списки одиниць і таблицю множників при зміні категорії."""
        g = self.grp_var.get()
        units = list(UNIT_GROUPS[g].keys())
        self.from_cb["values"] = units; self.from_cb.set(units[0])
        self.to_cb["values"] = units;   self.to_cb.set(units[1] if len(units) > 1 else units[0])
        self._fill_table()
        self._convert()

    def _convert(self, *_):
        """Виконує конвертацію і оновлює результат та рівняння."""
        try:
            v = float(self.val_e.get())
            fu = self.from_cb.get()
            tu = self.to_cb.get()
            r = convert_value(v, fu, tu, self.grp_var.get())
            self.result_val.config(text=f"{r:.8g}")
            self.eq_lbl.config(text=f"{v} {fu}  =  {r:.8g} {tu}", fg=ACCENT)
            self._result_str = f"{r:.8g}"
        except Exception as e:
            self.result_val.config(text="Помилка")
            self.eq_lbl.config(text=str(e), fg=RED)

    def _copy(self):
        """Копіює числовий результат у буфер обміну."""
        if self._result_str:
            self.clipboard_clear()
            self.clipboard_append(self._result_str)
            self.eq_lbl.config(text=f"✔ Скопійовано: {self._result_str}", fg=GREEN)

    def _fill_table(self):
        """
        Заповнює таблицю множників: скільки одиниць to_unit відповідає 1 базовій одиниці.
        Для температури таблицю не показуємо (нелінійне перетворення).
        """
        g = self.grp_var.get()
        units = list(UNIT_GROUPS[g].keys())
        for item in self.tab.get_children():
            self.tab.delete(item)
        if g == "Температура":
            return
        factors = UNIT_GROUPS[g]
        base = units[0]
        for u in units:
            if u == base:
                continue
            f = factors[base] / factors[u]
            self.tab.insert("", "end", values=(f"1 {base}", u, f"{f:.6g}"))


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  ВКЛАДКА 6 — ПРО ПРОГРАМУ                                               ║
# ║  Автор: Сауляк Назарій, 1 курс, група F3, підгрупа Б                    ║
# ║  Варіант завдання: Помічник фізика                                       ║
# ╚══════════════════════════════════════════════════════════════════════════╝

class AboutTab(tk.Frame):
    """
    Вкладка «Про програму».
    Містить:
      - титульний блок з назвою, автором, групою та варіантом;
      - короткий опис кожного модуля програми;
      - технологічний стек;
      - кольорову легенду UI;
      - короткий посібник (як користуватись).
    """

    def __init__(self, master):
        super().__init__(master, bg=BG)
        self._build()

    # ── Побудова інтерфейсу ──────────────────────────────────────────────
    def _build(self):
        # Зовнішній прокручуваний контейнер, щоб весь вміст
        # не обрізався на маленьких вікнах
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        vsb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Внутрішній фрейм, який і скролиться
        inner = tk.Frame(canvas, bg=BG)
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        # Оновлення scrollregion при зміні розміру вмісту
        def _on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        # Оновлення ширини внутрішнього фрейму при зміні розміру canvas
        def _on_canvas_resize(event):
            canvas.itemconfig(win_id, width=event.width)

        inner.bind("<Configure>", _on_configure)
        canvas.bind("<Configure>", _on_canvas_resize)

        # Прокрутка колесом миші
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # ── 1. ТИТУЛЬНИЙ БЛОК ─────────────────────────────────────────
        title_card = tk.Frame(
            inner, bg=PANEL,
            highlightbackground=ACCENT, highlightthickness=2
        )
        title_card.pack(fill="x", padx=20, pady=(20, 8))

        # Назва програми — великий акцентний заголовок
        tk.Label(
            title_card,
            text="⚗  PhysicsHelper",
            font=("Courier New", 28, "bold"),
            bg=PANEL, fg=ACCENT
        ).pack(pady=(18, 2))

        # Підзаголовок — що це за програма одним реченням
        tk.Label(
            title_card,
            text="Комплексний помічник з фізики для студентів",
            font=("Courier New", 11),
            bg=PANEL, fg=FG2
        ).pack(pady=(0, 12))

        # Горизонтальний роздільник
        tk.Frame(title_card, bg=BORDER, height=1).pack(fill="x", padx=20)

        # Блок «хто зробив» — три колонки в одному рядку
        info_row = tk.Frame(title_card, bg=PANEL)
        info_row.pack(pady=12, padx=20)

        # Допоміжна функція: малює одну «картку» з іконкою, заголовком і значенням
        def _info_block(parent, icon, label, value, color=ACCENT):
            f = tk.Frame(parent, bg=CARD,
                         highlightbackground=BORDER, highlightthickness=1)
            f.pack(side="left", padx=8, ipadx=14, ipady=8)
            tk.Label(f, text=icon, font=("Courier New", 18), bg=CARD, fg=color).pack()
            tk.Label(f, text=label, font=FNS, bg=CARD, fg=FG2).pack()
            tk.Label(f, text=value, font=FNB, bg=CARD, fg=color).pack()

        _info_block(info_row, "👤", "Автор", "Сауляк Назарій", ACCENT)
        _info_block(info_row, "🎓", "Курс / Група", "1 курс · F3 · підгрупа Б", GREEN)
        _info_block(info_row, "📋", "Варіант завдання", "Помічник фізика", YELLOW)
        _info_block(info_row, "📅", "Рік", "2026", PURPLE)

        # ── 2. ОПИС МОДУЛІВ ───────────────────────────────────────────
        section_label(inner, "МОДУЛІ ПРОГРАМИ", pady_top=14)

        # Список (іконка, назва вкладки, колір, опис)
        modules = [
            (
                "📊", "Статистика", ACCENT,
                "Статистична обробка масивів вимірювань. "
                "Завантажуйте дані з файлу, генеруйте випадкові вибірки або вводьте "
                "вручну. Програма обчислює середнє, стандартне відхилення, "
                "похибку середнього та довірчий інтервал (розподіл Стьюдента). "
                "Результат відображається на гістограмі з кривою Гаусса."
            ),
            (
                "🚀", "Кінематика", GREEN,
                "Чисельне моделювання польоту тіла під кутом до горизонту. "
                "Підтримується як ідеальний випадок (без опору), так і модель "
                "з квадратичним опором повітря (k, m). "
                "Три графіки (траєкторія, швидкість, прискорення), "
                "детальна таблиця та аналіз енергій/екстремумів."
            ),
            (
                "📚", "Довідник констант", YELLOW,
                "База фундаментальних фізичних констант (механіка, електромагнетизм, "
                "термодинаміка, квантова і ядерна фізика). "
                "Миттєвий пошук по назві або символу, перемикання між системами SI і СГС, "
                "копіювання значення в буфер одним подвійним кліком."
            ),
            (
                "🔬", "Поширення похибок", RED,
                "Аналітичний розрахунок похибки складної функції методом "
                "квадратного кореня суми квадратів. "
                "Введіть формулу на мові sympy — програма автоматично знайде змінні, "
                "обчислить часткові похідні символьно і видасть "
                "абсолютну та відносну похибки, а також внесок кожної змінної."
            ),
            (
                "⚖", "Конвертер одиниць", PURPLE,
                "Конвертація між одиницями 8 категорій: швидкість, довжина, маса, "
                "час, енергія, тиск, температура (°C/K/°F), кут. "
                "Швидкі кнопки для найпоширеніших перетворень, "
                "таблиця множників та можливість підставити результат "
                "безпосередньо у поле кінематики."
            ),
        ]

        for icon, name, color, desc in modules:
            # Картка кожного модуля
            card = tk.Frame(
                inner, bg=CARD,
                highlightbackground=color, highlightthickness=1
            )
            card.pack(fill="x", padx=20, pady=4)

            hdr_row = tk.Frame(card, bg=CARD)
            hdr_row.pack(fill="x", padx=12, pady=(10, 2))

            # Кольорова крапка-іконка
            tk.Label(
                hdr_row, text=icon + "  " + name,
                font=FNB, bg=CARD, fg=color
            ).pack(side="left")

            # Текст опису під заголовком
            tk.Label(
                card, text=desc,
                font=FNS, bg=CARD, fg=FG,
                wraplength=900, justify="left", anchor="w"
            ).pack(fill="x", padx=20, pady=(0, 10))

        # ── 3. ТЕХНОЛОГІЧНИЙ СТЕК ─────────────────────────────────────
        section_label(inner, "ТЕХНОЛОГІЧНИЙ СТЕК", pady_top=14)

        tech_card = tk.Frame(
            inner, bg=CARD,
            highlightbackground=BORDER, highlightthickness=1
        )
        tech_card.pack(fill="x", padx=20, pady=4)

        tech_items = [
            ("🐍  Python 3.x",        "Основна мова програмування"),
            ("🖼  tkinter / ttk",      "Графічний інтерфейс (GUI)"),
            ("📦  math / random / os", "Вбудовані модулі Python"),
        ]

        # Виводимо у два стовпці для компактності
        grid_tech = tk.Frame(tech_card, bg=CARD)
        grid_tech.pack(fill="x", padx=16, pady=10)
        grid_tech.columnconfigure(0, weight=1, uniform="tc")
        grid_tech.columnconfigure(1, weight=1, uniform="tc")

        for i, (tech, note) in enumerate(tech_items):
            row_i = i // 2
            col_i = i % 2
            cell = tk.Frame(grid_tech, bg=CARD2,
                             highlightbackground=BORDER, highlightthickness=1)
            cell.grid(row=row_i, column=col_i, padx=6, pady=4, sticky="ew", ipadx=8, ipady=6)
            tk.Label(cell, text=tech, font=FNB, bg=CARD2, fg=CYAN).pack(anchor="w", padx=4)
            tk.Label(cell, text=note, font=FNS, bg=CARD2, fg=FG2).pack(anchor="w", padx=4)

        # ── 4. КОЛЬОРОВА ЛЕГЕНДА UI ───────────────────────────────────
        section_label(inner, "КОЛЬОРОВА СХЕМА ІНТЕРФЕЙСУ", pady_top=14)

        legend_card = tk.Frame(
            inner, bg=CARD,
            highlightbackground=BORDER, highlightthickness=1
        )
        legend_card.pack(fill="x", padx=20, pady=4)

        legend_items = [
            (CLR_INPUT,  "●  Синій",   "Вхідні дані — поля, які заповнює користувач"),
            (CLR_CONST,  "●  Жовтий",  "Фізичні константи — значення, які рідко змінюються"),
            (CLR_RESULT, "●  Зелений", "Результати — поля тільки для читання, обчислені програмою"),
            (RED,        "●  Червоний","Попередження / похибки / акцент на відхиленні"),
            (PURPLE,     "●  Фіолетовий", "Символьні вирази"),
            (CYAN,       "●  Блакитний", "Технічні підписи, назви компонентів"),
        ]

        for clr, dot_text, meaning in legend_items:
            row = tk.Frame(legend_card, bg=CARD)
            row.pack(fill="x", padx=16, pady=3)
            tk.Label(row, text=dot_text, font=FNB, bg=CARD, fg=clr, width=18, anchor="w").pack(side="left")
            tk.Label(row, text=meaning,  font=FNS, bg=CARD, fg=FG, anchor="w").pack(side="left", padx=8)

        # ── 5. КОРОТКИЙ ПОСІБНИК ──────────────────────────────────────
        section_label(inner, "ЯК КОРИСТУВАТИСЬ", pady_top=14)

        guide_card = tk.Frame(
            inner, bg=CARD,
            highlightbackground=BORDER, highlightthickness=1
        )
        guide_card.pack(fill="x", padx=20, pady=(4, 20))

        steps = [
            ("1", "Статистика",
             "Завантажте файл / введіть числа / згенеруйте вибірку → "
             "виберіть рівень довіри → натисніть «Розрахувати»."),
            ("2", "Кінематика",
             "Задайте v₀, кут, h₀, g (і опційно k, m) → «Розрахувати траєкторію» → "
             "перегляньте графіки, таблицю і аналітику у трьох підвкладках."),
            ("3", "Довідник",
             "Введіть ім'я або символ у рядок пошуку → виберіть SI/СГС → "
             "двічі клацніть на рядку, щоб скопіювати значення."),
            ("4", "Похибки",
             "Введіть формулу (напр. U/I або 2*pi*sqrt(l/g)) → «Розпізнати змінні» → "
             "заповніть значення та Δ → «Розрахувати похибку»."),
            ("5", "Конвертер",
             "Оберіть категорію → вкажіть значення та одиниці → "
             "результат оновлюється в реальному часі. "
             "Кнопка ⚖ у Кінематиці підставляє перетворене значення у поле."),
        ]

        for num, tab_name, hint in steps:
            step_row = tk.Frame(guide_card, bg=CARD2,
                                 highlightbackground=BORDER, highlightthickness=1)
            step_row.pack(fill="x", padx=12, pady=4)

            # Номер кроку у великому колі
            tk.Label(
                step_row, text=num,
                font=("Courier New", 13, "bold"),
                bg=ACCENT, fg=BG, width=3
            ).pack(side="left", ipadx=2, ipady=4)

            # Назва вкладки та підказка
            text_f = tk.Frame(step_row, bg=CARD2)
            text_f.pack(side="left", fill="x", expand=True, padx=10, pady=6)
            tk.Label(
                text_f, text=tab_name,
                font=FNB, bg=CARD2, fg=ACCENT, anchor="w"
            ).pack(anchor="w")
            tk.Label(
                text_f, text=hint,
                font=FNS, bg=CARD2, fg=FG, anchor="w", wraplength=820, justify="left"
            ).pack(anchor="w")

        # ── Підвал вкладки ────────────────────────────────────────────
        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", padx=20, pady=8)
        tk.Label(
            inner,
            text="PhysicsHelper  •  Індивідуальне творче завдання  "
                 "•  Сауляк Назарій  •  2026",
            font=FNS, bg=BG, fg=FG2
        ).pack(pady=(0, 16))


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  ГОЛОВНЕ ВІКНО — PhysicsLab                                              ║
# ╚══════════════════════════════════════════════════════════════════════════╝
class PhysicsLab(tk.Tk):
    """
    Головний клас програми. Успадковує tk.Tk (кореневе вікно tkinter).
    Створює заголовок, легенду кольорів, Notebook з 5 вкладками і статусбар.
    """
    def __init__(self):
        super().__init__()
        self.title("PhysicsHelper")
        self.geometry("1220x880")
        self.minsize(1000, 700)
        self.configure(bg=BG)
        # Перехоплюємо закриття вікна через X, щоб показати діалог підтвердження
        self.protocol("WM_DELETE_WINDOW", self._on_exit)
        self._build()

    def _on_exit(self):
        """
        Викликається при натисканні кнопки ✕ або 🚪 Вихід.
        Показує діалог підтвердження перед закриттям програми.
        """
        if messagebox.askyesno(
            title="Вихід з PhysicsHelper",
            message="Ви впевнені, що хочете вийти?\nНезбережені дані буде втрачено."
        ):
            self.destroy()   # Знищує вікно та завершує mainloop

    def _build(self):
        """Будує весь інтерфейс головного вікна."""
        # ── Заголовок програми ──────────────────────────────────────────
        hdr = tk.Frame(self, bg=PANEL)
        hdr.pack(fill="x")
        tk.Label(hdr, text="⚗  PhysicsHelper", font=("Courier New", 17, "bold"),
                 bg=PANEL, fg=ACCENT).pack(side="left", padx=14, pady=8)
        tk.Label(hdr, text="|  Статистика · Кінематика · Довідник · Похибки · Конвертер",
                 font=FNS, bg=PANEL, fg=FG2).pack(side="left")

        # ── Кнопка виходу (праворуч у заголовку) ─────────────────────
        # Розміщуємо ПЕРЕД легендою, щоб вона була крайньою правою
        exit_btn = tk.Button(
            hdr,
            text="🚪 Вихід",
            command=self._on_exit,
            font=FNB,
            bg="#2d1015",                # Темно-червоний фон
            fg=RED,                      # Червоний текст
            activebackground=PANEL,
            activeforeground=RED,
            relief="flat",
            cursor="hand2",
            padx=10, pady=6,
            highlightbackground=RED,
            highlightthickness=1
        )
        exit_btn.pack(side="right", padx=(6, 14), pady=4)

        # ── Легенда кольорів (правіша частина заголовку, ліворуч від кнопки виходу) ──
        leg = tk.Frame(hdr, bg=PANEL)
        leg.pack(side="right", padx=14)
        for clr, lbl in [(CLR_INPUT, "Вхідні дані"),
                          (CLR_CONST, "Константи"),
                          (CLR_RESULT, "Результати")]:
            f = tk.Frame(leg, bg=PANEL)
            f.pack(side="left", padx=6)
            tk.Label(f, text="●", font=FN, bg=PANEL, fg=clr).pack(side="left")
            tk.Label(f, text=lbl, font=FNS, bg=PANEL, fg=FG2).pack(side="left", padx=(2, 0))

        # Горизонтальний роздільник між заголовком і вкладками
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        # ── Notebook — 5 вкладок ────────────────────────────────────────
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=PANEL, foreground=FG2,
                         font=FN, padding=[14, 7], borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", CARD)], foreground=[("selected", ACCENT)])

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=6, pady=6)

        # Для кожної вкладки: (назва, клас)
        for name, Cls in [("  📊  Статистика  ", StatisticsTab),
                            ("  🚀  Кінематика  ", KinematicsTab),
                            ("  📚  Довідник    ", ConstantsTab),
                            ("  🔬  Похибки     ", ErrorPropTab),
                            ("  ⚖  Конвертер   ", ConverterTab),
                            ("  ℹ️  Про програму", AboutTab)]:
            frame = tk.Frame(nb, bg=BG)
            nb.add(frame, text=name)
            Cls(frame).pack(fill="both", expand=True)

        # ── Статусбар знизу ──────────────────────────────────────────────
        status = tk.Frame(self, bg=PANEL, height=22)
        status.pack(fill="x", side="bottom")
        tk.Label(status, text="PhysicsLab v3  |  tkinter",
                 font=FNS, bg=PANEL, fg=FG2).pack(side="left", padx=10)
        tk.Label(status, text=datetime.now().strftime("%Y-%m-%d"),
                 font=FNS, bg=PANEL, fg=FG2).pack(side="right", padx=10)


# ── ТОЧКА ВХОДУ ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = PhysicsLab()
    app.mainloop()