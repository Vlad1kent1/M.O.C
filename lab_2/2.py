from math import cos, sin, pi, sqrt, atan
import numpy as np
import matplotlib.pyplot as plt


# Генерація випадкового двійкового сигналу (0 або 1)
def generate_binary_signal(N):
    return np.random.randint(0, 2, N)


# Обчислення коефіцієнтів А і B для ДПФ
def calculate_coefficients(signal):
    N = len(signal)
    coefficients = []

    # A0 і B0 для постійної складової
    A0 = 1 / N * sum(signal[i] for i in range(N))
    B0 = 0
    coefficients.append((A0, B0))

    # Обчислюємо для кожної частоти k від 1 до N//2
    for k in range(1, N // 2 + 1):
        A = 1 / N * sum(signal[i] * cos(2 * pi * k * i / N) for i in range(N))
        B = 1 / N * sum(signal[i] * sin(2 * pi * k * i / N) for i in range(N))
        coefficients.append((A, B))

    return coefficients


# Обчислення амплітуд і фаз для кожної гармоніки
def calculate_phases_and_amplitudes(coefficients):
    amplitudes = []
    phases = []

    for A, B in coefficients:
        C = sqrt(A ** 2 + B ** 2)
        phi = atan(B / A) if A != 0 else 0

        amplitudes.append(C)
        phases.append(phi)

    return amplitudes, phases


# Побудова графіків амплітудного і фазового спектрів
def plot_amplitudes_and_phases(amplitudes, phases):
    plt.figure(figsize=(10, 6))
    plt.stem(range(len(amplitudes)), amplitudes, "b", markerfmt="bo",
             basefmt=" ", label="|C_k|")
    plt.title("Спектр амплітуд")
    plt.xlabel("k")
    plt.ylabel("Амплітуда")
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.stem(range(len(phases)), phases, "b", markerfmt="bo",
             basefmt=" ", label="arg(C_k)")
    plt.title("Спектр фаз")
    plt.xlabel("k")
    plt.ylabel("Фаза")
    plt.grid(True)
    plt.legend()
    plt.show()


# Функція для відновлення сигналу s(t) на основі коефіцієнтів
def s(t, amplitudes, phases, Tc, N):
    s = amplitudes[0]
    for k in range(1, len(amplitudes)):
        s += 2 * amplitudes[k] * cos(2 * pi * k * t / Tc + phases[k])
    return s


# Побудова графіка відновленого сигналу
def plot_signal(amplitudes, phases, Tc, N):
    t_values = np.linspace(0, Tc, 500)
    s_values = [s(t, amplitudes, phases, Tc, N) for t in t_values]

    plt.figure(figsize=(10, 6))
    plt.plot(t_values, s_values, label="s(t)")
    plt.title("Відновлений сигнал s(t)")
    plt.xlabel("Час t")
    plt.ylabel("s(t)")
    plt.grid(True)
    plt.legend()
    plt.show()


# Виведення табличних значень та формули
def print_table_and_formula(amplitudes, phases, Tc):
    t_values = np.linspace(0, Tc, 8)
    s_values = [s(t, amplitudes, phases, Tc, len(amplitudes)) for t in t_values]

    print("Часові відмітки:")
    for t in t_values:
        print(f"{t:.5f} | ", end="")
    print("\n" + "-" * (len(t_values) * 10 - 1))

    print("Значення сигналу:")
    for s_val in s_values:
        print(f"{s_val:.5f} | ", end="")
    print()

    print("Формула для s(t):")
    formula = f"s(t) = {amplitudes[0]}"
    for i in range(1, len(amplitudes)):
        formula += f" + 2*{amplitudes[i]:.4f}*cos({2 * i}*pi*t/{Tc} + {phases[i]:.4f})"
    print(formula)


def main():
    Tc = 1
    n = 12
    N = 96 + n

    signal = generate_binary_signal(N)

    coefficients = calculate_coefficients(signal)

    for i, (A, B) in enumerate(coefficients):
        print(f"C{i} = {A} + i*{B}")

    amplitudes, phases = calculate_phases_and_amplitudes(coefficients)

    plot_amplitudes_and_phases(amplitudes, phases)

    print_table_and_formula(amplitudes, phases, Tc)

    plot_signal(amplitudes, phases, Tc, N)


if __name__ == "__main__":
    main()
