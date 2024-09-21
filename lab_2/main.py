import numpy as np
import matplotlib.pyplot as plt
import time


# Функція для генерації вхідного сигналу
def generate_signal(N):
    return np.random.random(N)


# Функція для обчислення одного члена ДПФ у тригонометричній формі
def dft_single_k(f, k, N):
    Ak = 0
    Bk = 0
    for i in range(N):
        Ak += f[i] * np.cos(2 * np.pi * k * i / N)
        Bk -= f[i] * np.sin(2 * np.pi * k * i / N)
    Ak /= N
    Bk /= N
    return Ak, Bk


# Функція для обчислення ДПФ
def dft(f):
    N = len(f)
    Ck = np.zeros(N, dtype=complex)
    for k in range(N):
        Ak, Bk = dft_single_k(f, k, N)
        Ck[k] = Ak + 1j * Bk
    return Ck


# Функція для побудови графіків спектра амплітуд та фаз
def plot_spectrum(Ck):
    N = len(Ck)
    k_vals = np.arange(N)

    amplitude_spectrum = np.abs(Ck)
    phase_spectrum = np.angle(Ck)

    # Графік амплітудного спектра
    plt.figure()
    plt.stem(k_vals, amplitude_spectrum)
    plt.title("Амплітудний спектр")
    plt.xlabel("Номер гармоніки k")
    plt.ylabel("|Ck|")
    plt.grid(True)

    # Графік фазового спектра
    plt.figure()
    plt.stem(k_vals, phase_spectrum)
    plt.title("Фазовий спектр")
    plt.xlabel("Номер гармоніки k")
    plt.ylabel("arg(Ck)")
    plt.grid(True)

    plt.show()


# Функція для обчислення часу виконання та кількості операцій
def calculate_time_and_operations(f):
    N = len(f)
    start_time = time.time()

    num_multiplications = 0
    num_additions = 0

    # Обчислення коефіцієнтів
    for k in range(N):
        Ak, Bk = 0, 0
        for i in range(N):
            Ak += f[i] * np.cos(2 * np.pi * k * i / N)
            Bk -= f[i] * np.sin(2 * np.pi * k * i / N)
            num_multiplications += 2  # Одне множення для cos та одне для sin
            num_additions += 2  # Додавання до Ak і Bk

    time_taken = time.time() - start_time
    return time_taken, num_multiplications, num_additions


# Головна програма
def main():
    n = 12
    N = 10 + n  # Число членів ряду

    # Генерація сигналу
    f = generate_signal(N)
    print(f"Вхідний сигнал: {f}")

    # Обчислення ДПФ
    Ck = dft(f)

    # Виведення коефіцієнтів
    print("\nКоефіцієнти Фур'є (Ck):")
    for k in range(N):
        print(f"C{k} = {Ck[k]}")

    # Обчислення часу та кількості операцій
    time_taken, num_multiplications, num_additions = calculate_time_and_operations(f)
    print(f"\nЧас обчислення: {time_taken:.6f} секунд")
    print(f"Кількість множень: {num_multiplications}")
    print(f"Кількість додавань: {num_additions}")

    # Побудова графіків
    plot_spectrum(Ck)


if __name__ == "__main__":
    main()
