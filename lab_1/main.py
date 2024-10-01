from math import sin, cos, pi
import matplotlib.pyplot as plt
import numpy as np

f = lambda x: x * 12 * np.exp(-x ** 2 / 12)

# Функція для отримання коефіцієнтів Фур'є
def get_coefficients(N):
    a_N = (1 / pi) * np.trapezoid(
        [f(x) * cos(N * x) for x in np.linspace(-pi, pi, 1000)],
        np.linspace(-pi, pi, 1000)
    )

    if N == 0:
        return a_N

    b_N = (1 / pi) * np.trapezoid(
        [f(x) * sin(N * x) for x in np.linspace(-pi, pi, 1000)],
        np.linspace(-pi, pi, 1000)
    )

    return a_N, b_N

# Функція для обчислення наближення функції f за допомогою ряду Фур'є
def fourier(x, N):
    a_0 = get_coefficients(0)
    f_approx = a_0 / 2

    for i in range(1, N + 1):
        a_N, b_N = get_coefficients(i)
        f_approx += a_N * cos(i * x) + b_N * sin(i * x)

    return f_approx

# Функція для обчислення відносної похибки
def relative_error(N):
    x = np.linspace(-pi, pi, 1000)
    return sum(abs(f(val) - fourier(val, N)) / abs(f(val)) for val in x) / 1000

# Функція для обчислення абсолютної похибки
def absolute_error(N):
    x = np.linspace(-pi, pi, 1000)
    return sum(abs(f(val) - fourier(val, N)) for val in x) / 1000

# Функція для збереження результатів у файл
def save_to_file(N):
    with open("save.txt", "w") as file:
        file.write(f"Order N: {N}\n")
        file.write("Coefficients:\n")
        a_0 = get_coefficients(0)
        file.write(f"a_0 = {a_0:.6f}\n")
        for k in range(1, N + 1):
            a_N, b_N = get_coefficients(k)
            file.write(f"a_{k} = {a_N:.6f}, b_{k} = {b_N:.6f}\n")
        r_error = relative_error(N)
        a_error = absolute_error(N)
        file.write(f"Relative error of approximation: {r_error:.6f}\n")
        file.write(f"Absolute error of approximation: {a_error:.6f}\n")

# Функція для побудови гармонік
def plot_harmonics(N):
    x = np.linspace(-pi, pi, 1000)

    plt.figure(figsize=(14, 10))
    a0 = get_coefficients(0)
    harmonic = [a0 / 2 for _ in x]
    plt.plot(x, harmonic, label="Harmonic 0")

    for k in range(1, N + 1):
        a_N, b_N = get_coefficients(k)
        harmonic = [a_N * cos(k * val) + b_N * sin(k * val) for val in x]
        plt.plot(x, harmonic, label=f"Harmonic {k}")

    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.show()

# Функція для побудови спектру коефіцієнтів Фур'є
def plot_spectrum():
    a_coefficients = []
    b_coefficients = []
    ks = list(range(11))

    for k in ks:
        if k == 0:
            a_k = get_coefficients(k)
            b_k = 0
        else:
            a_k, b_k = get_coefficients(k)
        a_coefficients.append(abs(a_k))
        b_coefficients.append(abs(b_k))

    # Побудова графіка спектру
    plt.figure(figsize=(10, 6))
    plt.stem(ks, a_coefficients, "b", markerfmt="bo", basefmt=" ", label="|a_N|")
    plt.stem(ks[1:], b_coefficients[1:], "r", markerfmt="ro", basefmt=" ", label="|b_N|")
    plt.title("Частотний спектр коефіцієнтів Фур'є")
    plt.xlabel("N")
    plt.ylabel("Амплітуда")
    plt.grid(True)
    plt.legend()
    plt.show()

# Функція для побудови графіка ряду Фур'є
def plot_fourier(N):
    x = np.linspace(-pi, pi, 1000)
    y_original = [f(val) for val in x]
    y_fourier = [fourier(val, N) for val in x]

    plt.figure(figsize=(10, 6))
    plt.plot(x, y_original, label=r"$x \cdot 12 \cdot e^{-x^2 / 12}$")
    plt.plot(x, y_fourier, label=f"Fourier Series of Order {N}", color="orange", lw=1)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()
    plt.show()

def main():
    N = 10
    save_to_file(N)
    plot_harmonics(N)
    plot_spectrum()
    plot_fourier(N)

if __name__ == "__main__":
    main()
