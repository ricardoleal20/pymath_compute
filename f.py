import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson

# Definir la función inicial f(x)


def f_initial(x):
    return np.exp(-x**2)

# Discretizar la función en n puntos


def discretize_function(f, a, b, n):
    x = np.linspace(a, b, n)
    y = f(x)
    return x, y

# Calcular la derivada numérica de la función discretizada


def numerical_derivative(y, x):
    dy = np.gradient(y, x)
    return dy

# Calcular el área del sólido de revolución


def area_of_revolution(x, y):
    dy = numerical_derivative(y, x)
    integrand = y * np.sqrt(1 + dy**2)
    area = 2 * np.pi * simpson(integrand, x=x)
    return area

# Método de descenso de gradiente para minimizar el área


def gradient_descent(x, y, lr=0.01, epochs=100):
    areas = []
    for epoch in range(epochs):
        current_area = area_of_revolution(x, y)
        areas.append(current_area)

        # Calcular el gradiente
        dy = numerical_derivative(y, x)
        dA_dy = 2 * np.pi * np.sqrt(1 + dy**2)

        # Actualizar los valores de y usando el gradiente
        y -= lr * dA_dy

    return y, areas


# Parámetros del problema
a, b = -1, 1
n = 100  # número de puntos de discretización
learning_rate = 0.01
epochs = 100

# Inicializar la función discretizada
x, y = discretize_function(f_initial, a, b, n)

# Ejecutar el descenso de gradiente
y_opt, areas = gradient_descent(x, y, lr=learning_rate, epochs=epochs)

# Graficar los resultados
plt.figure(figsize=(14, 8))

# Subplot 1: f(x) vs x
plt.subplot(3, 1, 1)
plt.plot(x, f_initial(x), label='f(x) = e^{-x^2}')
plt.plot(x, y_opt, label='f(x) optimizado', linestyle='--')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.title('f(x) vs x')

# Subplot 2: Área vs Iteraciones
plt.subplot(3, 1, 2)
plt.plot(range(epochs), areas)
plt.xlabel('Iteraciones')
plt.ylabel('Área')
plt.title('Área vs Iteraciones')

# Subplot 3: Valor mínimo del área obtenido
plt.subplot(3, 1, 3)
plt.plot(range(epochs), areas)
min_area_idx = np.argmin(areas)
plt.axhline(areas[min_area_idx], color='r', linestyle='--',
            label=f'Mínimo área: {areas[min_area_idx]:.4f}')
plt.xlabel('Iteraciones')
plt.ylabel('Área')
plt.legend()
plt.title('Valor mínimo del área obtenido')

plt.tight_layout()
plt.show()

print(f"El área mínima obtenida es: {areas[min_area_idx]}")
