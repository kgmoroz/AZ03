from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
import pandas as pd
import matplotlib.pyplot as plt

# Настройки Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск браузера в фоновом режиме

driver = webdriver.Chrome(options=chrome_options)

base_url = "https://www.divan.ru/category/divany-i-kresla/page-"
page_number = 1
product_info_list = []

while True:
    url = f"{base_url}{page_number}"
    print(f"\nЗагружаем страницу {url}")
    driver.get(url)

    # Ожидание загрузки элементов на странице
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[itemprop='itemListElement']"))
        )
    except Exception as e:
        print("Товары не найдены.")
        #traceback.print_exc()  # Вывод полного стека вызовов ошибки
        try:
            p404 = driver.find_element(By.CLASS_NAME, "MAb3P")
            if p404:
                print(f"Страница {url} не существует")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        break # Если товаров нет, выходим из цикла

    products = driver.find_elements(By.CSS_SELECTOR, "div[itemprop='itemListElement']")
    if not products:
        print("Товары не найдены")
        break  # Если товаров нет, выходим из цикла

    print(f"Найдено {len(products)} товаров на странице {page_number}. Начинаем парсинг...")
    for product in products:
        try:
            # Поиск элемента с классом 'wYUX2'
            container = product.find_element(By.CLASS_NAME, "wYUX2")
            # Поиск вложенного элемента span с itemprop='name' внутри контейнера
            name = container.find_element(By.CSS_SELECTOR, "span[itemprop='name']").text
        except Exception as e:
            name = "N/A"
            print(f"Ошибка при получении наименования: {e}")
        try:
            price = product.find_element(By.CSS_SELECTOR, "meta[itemprop='price']").get_attribute("content")
        except Exception as e:
            price = "N/A"
            print(f"Ошибка при получении цены: {e}")
        try:
            link = product.find_element(By.CSS_SELECTOR, "a.ui-GPFV8").get_attribute("href")
        except Exception as e:
            link = "N/A"
            print(f"Ошибка при получении ссылки: {e}")
        # если наименование содержит "диван", добавляем его в список
        if "диван" in name.lower():
            product_info_list.append([name, price, link])

    print(f"Страница {page_number} успешно обработана. Переходим на следующую страницу...")
    page_number += 1

# Закрытие браузера
driver.quit()

# Сохранение данных в CSV-файл
csv_file = 'product_data.csv'
csv_columns = ['name', 'price', 'url']

try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_columns) # Создаём первый ряд
        writer.writerows(product_info_list) # Прописываем использование списка как источника для рядов таблицы
    print(f"\nДанные успешно сохранены в {csv_file}")
except IOError:
    print("\nОшибка при записи в файл")

# Чтение данных из CSV-файла
df = pd.read_csv('product_data.csv')

# Вычисление средней цены
average_price = df['price'].mean()
print(f'Средняя цена: {average_price:.2f} руб.')

# Построение гистограммы цен
plt.figure(figsize=(10, 6))
plt.hist(df['price'], bins=10, edgecolor='black')
plt.title('Гистограмма цен')
plt.xlabel('Цена (руб.)')
plt.ylabel('Количество моделей диванов')
plt.axvline(average_price, color='r', linestyle='dashed', linewidth=1, label=f'Средняя цена: {average_price:.2f} руб.')
plt.legend()
plt.grid(True)
plt.show()