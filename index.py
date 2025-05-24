import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import time
import threading

# ===== Алгоритми сортування =====
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][1] < right[j][1]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def smooth_sort(arr):  # Заглушка, можна замінити на реальну реалізацію
    return sorted(arr, key=lambda x: x[1])

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2][1]
    left = [x for x in arr if x[1] < pivot]
    middle = [x for x in arr if x[1] == pivot]
    right = [x for x in arr if x[1] > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# ===== Генерація списку кораблів =====
def generate_ships(case, size, vmin, vmax):
    names = ["Альфа", "Бета", "Гамма", "Дельта", "Епсілон", "Зета", "Ікар", "Крон", "Левіафан", "Нова"]
    if case == "Initial":
        ship_data = [(random.choice(names), random.randint(vmin, vmax)) for _ in range(size)]
    elif case == "Updated":
        base = [(random.choice(names), random.randint(vmin, vmax)) for _ in range(size // 2)]
        base_sorted = sorted(base, key=lambda x: x[1])  # попередньо сортуємо частину
        updated = [(random.choice(names), random.randint(vmin, vmax)) for _ in range(size - len(base_sorted))]
        ship_data = base_sorted + updated
    elif case == "Final":
        ship_data = [(random.choice(names), random.randint(vmin, vmax)) for _ in range(size)]
    return ship_data

# ===== Сортування кораблів =====
def sort_ships(ship_list, algorithm):
    data = ship_list.copy()
    if algorithm == "Сортування злиттям":
        return merge_sort(data)
    elif algorithm == "Плавне сортування":
        return smooth_sort(data)
    elif algorithm == "Швидке сортування":
        return quick_sort(data)
    else:
        raise ValueError("Невідомий алгоритм")

# ===== Збереження в файл =====
def save_result_to_file(initial, sorted_arr, algo, elapsed):
    filename = f"fleet_sorted_{algo.replace(' ', '_')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"📋 Початковий список кораблів ({len(initial)}):\n")
        for name, sailors in initial:
            f.write(f"{sailors}; ")

        f.write(f"\n✅ Відсортований список ({algo}):\n")
        for name, sailors in sorted_arr:
            f.write(f"{sailors}; ")

        f.write(f"\n⏱ Час виконання: {elapsed:.3f} мс\n")
    return filename

# ===== Основна функція =====
def run_sort():
    try:
        case = case_combo.get()
        algo = algo_combo.get()
        size = int(size_entry.get())
        vmin = int(min_entry.get())
        vmax = int(max_entry.get())
        if size > 100000:
            raise ValueError("Максимальна кількість кораблів — 100000.")
        if vmin > vmax:
            raise ValueError("Мінімальне значення більше за максимальне.")
    except ValueError as e:
        output_text.config(state='normal')
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"❌ Помилка: {e}")
        output_text.config(state='disabled')
        return

    output_text.config(state='normal')
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"⚓ Генерація флоту з {size} кораблів...\n")
    output_text.config(state='disabled')

    ship_list = generate_ships(case, size, vmin, vmax)

    start = time.perf_counter()
    sorted_ships = sort_ships(ship_list, algo)
    elapsed = (time.perf_counter() - start) * 1000

    filename = save_result_to_file(ship_list, sorted_ships, algo, elapsed)

    output_text.config(state='normal')
    output_text.insert(tk.END, f"✅ Результати сортування збережено у файл:\n{filename}\n")
    output_text.insert(tk.END, f"⏱ Час виконання: {elapsed:.3f} мс\n")
    output_text.config(state='disabled')

def run_sort_threaded():
    threading.Thread(target=run_sort).start()

# ===== GUI =====
root = tk.Tk()
root.title("⚓ Сортування флоту: Візуалізація та аналіз")
root.geometry("1000x600")
root.configure(bg="#e1f5fe")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#e1f5fe", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
style.configure("TCombobox", padding=5)
style.configure("TLabelframe", background="#b3e5fc", font=("Segoe UI", 10, "bold"), relief="ridge")
style.configure("TLabelframe.Label", background="#b3e5fc")

main_frame = ttk.Frame(root, padding=15, style="TLabelframe")
main_frame.pack(fill=tk.BOTH, expand=True)

# Зображення "корабля"
header = ttk.Label(main_frame, text="⛵ Ревізія флоту — сортування кораблів за кількістю матросів", font=("Segoe UI", 14, "bold"))
header.pack(pady=10)

control_frame = ttk.Frame(main_frame)
control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

output_frame = ttk.LabelFrame(main_frame, text="Результат", padding=10)
output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=70, height=25, font=("Consolas", 10))
output_text.pack(fill=tk.BOTH, expand=True)
output_text.config(state='disabled')

# Ввід параметрів
ttk.Label(control_frame, text="Сценарій:").grid(row=0, column=0, sticky=tk.W, pady=2)
case_combo = ttk.Combobox(control_frame, values=["Initial", "Updated", "Final"], state="readonly", width=20)
case_combo.current(0)
case_combo.grid(row=0, column=1, pady=2)

ttk.Label(control_frame, text="Алгоритм сортування:").grid(row=1, column=0, sticky=tk.W, pady=2)
algo_combo = ttk.Combobox(control_frame, values=["Сортування злиттям", "Плавне сортування", "Швидке сортування"], state="readonly", width=25)
algo_combo.current(0)
algo_combo.grid(row=1, column=1, pady=2)

labels = ["Кількість кораблів:", "Мін. кількість матросів:", "Макс. кількість матросів:"]
defaults = ["1000", "50", "5000"]
entries = []
for i, (label, default) in enumerate(zip(labels, defaults)):
    ttk.Label(control_frame, text=label).grid(row=2+i, column=0, sticky=tk.W, pady=2)
    entry = ttk.Entry(control_frame, width=20)
    entry.insert(0, default)
    entry.grid(row=2+i, column=1, pady=2)
    entries.append(entry)

size_entry, min_entry, max_entry = entries

run_button = ttk.Button(control_frame, text="🚀 Запустити ревізію флоту", command=run_sort_threaded)
run_button.grid(row=6, column=0, columnspan=2, pady=15)

root.mainloop()
