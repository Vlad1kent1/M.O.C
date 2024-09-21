import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate


# Основна функція для n=12
def f(x, n):
    return x * n * np.exp(-x ** 2 / n)


# Функція для обчислення коефіцієнтів a_k
def a_k(k, n):
    result, _ = integrate.quad(lambda x: f(x, n) * np.cos(k * x), -np.pi, np.pi)
    return (1 / np.pi) * result


# Функція для обчислення коефіцієнтів b_k
def b_k(k, n):
    result, _ = integrate.quad(lambda x: f(x, n) * np.sin(k * x), -np.pi, np.pi)
    return (1 / np.pi) * result


# Функція для обчислення наближення функції рядом Фур'є до порядку N
def fourier_series(x, N, n):
    a0 = (1 / (2 * np.pi)) * integrate.quad(lambda x: f(x, n), -np.pi, np.pi)[0]
    sum_f = a0
    for k in range(1, N + 1):
        ak = a_k(k, n)
        bk = b_k(k, n)
        sum_f += ak * np.cos(k * x) + bk * np.sin(k * x)
    return sum_f


# Функція для оцінки похибки
def approximation_error(N, n):
    error = integrate.quad(lambda x: (f(x, n) - fourier_series(x, N, n)) ** 2, -np.pi, np.pi)[0]
    return np.sqrt(error / (2 * np.pi))


# Побудова графіків гармонік
def plot_fourier_series(N, n):
    x_vals = np.linspace(-np.pi, np.pi, 1000)
    f_vals = [f(x, n) for x in x_vals]
    approx_vals = [fourier_series(x, N, n) for x in x_vals]

    plt.plot(x_vals, f_vals, label='Original function')
    plt.plot(x_vals, approx_vals, label=f'Fourier series approximation, N={N}')
    plt.legend()
    plt.title('Fourier Series Approximation')
    plt.show()


# Головна функція
def main():
    n = 12  # Номер студента
    N = 10  # Порядок ряду Фур'є
    print(f"Обчислюємо наближення для n = {n} та N = {N}")

    # Обчислення та виведення коефіцієнтів
    a0 = (1 / (2 * np.pi)) * integrate.quad(lambda x: f(x, n), -np.pi, np.pi)[0]
    print(f"a0 = {a0}")
    for k in range(1, N + 1):
        ak = a_k(k, n)
        bk = b_k(k, n)
        print(f"a{k} = {ak}, b{k} = {bk}")

    # Оцінка похибки
    error = approximation_error(N, n)
    print(f"Похибка наближення: {error}")

    # Побудова графіка
    plot_fourier_series(N, n)

    # Збереження результатів у файл
    with open("fourier_results.txt", "w") as file:
        file.write(f"Порядок N: {N}\n")
        file.write(f"a0 = {a0}\n")
        for k in range(1, N + 1):
            file.write(f"a{k} = {a_k(k, n)}, b{k} = {b_k(k, n)}\n")
        file.write(f"Похибка наближення: {error}\n")


if __name__ == "__main__":
    main()
