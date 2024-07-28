import numpy as np
import matplotlib.pyplot as plt

# Генерация двух наборов случайных данных
num_samples = 100

# Первый набор случайных данных
x = np.random.rand(num_samples)

# Второй набор случайных данных
y = np.random.rand(num_samples)

# Печать примера случайного массива
random_array = np.random.rand(5)
print(random_array)

# Создание диаграммы рассеяния
plt.scatter(x, y, alpha=0.7, edgecolors='b')

# Добавление заголовка и меток осей
plt.title('Диаграмма рассеяния случайных данных')
plt.xlabel('X данные')
plt.ylabel('Y данные')

# Показать диаграмму
plt.show()