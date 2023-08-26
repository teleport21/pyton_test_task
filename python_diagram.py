#Встановлюєм бібліотеки для роботи
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

#Беремо дані з excel, я виніс аркуш Sales в інший файл для зручності   
excel_file = 'C://Users//User//Desktop//Data.xlsx'
df = pd.read_excel(excel_file)

# Конвертування з таблиці дати в тип даних "дата", також вказав формат даних в таблиці
df['Дата'] = pd.to_datetime(df['Дата'], format='%d.%m.%Y')

# Додавання стовпця "Місяць-Рік" для групування за ним
df['Місяць-Рік'] = df['Дата'].dt.to_period('M')

# Групування за країною та місяцем-роком і підрахунок сумарних продаж для кожного місяця
grouped_sales = df.groupby(['Країна', 'Місяць-Рік'])['Продажі'].sum().reset_index()

# Конвертування типу даних "Місяць-Рік" в рядки для подальшого використання
grouped_sales['Місяць-Рік'] = grouped_sales['Місяць-Рік'].astype(str)

# Створюєм зміну країни, та дістаємо унікальні країни зі зміної grouped_sales
countries = sorted(grouped_sales['Країна'].unique())

# Індекс поточної країни для графіка
current_country_index = 0

# Функція для оновлення графіку при натисканні кнопки "Наступний", а також використання оператора % коли при буде 5 країна, ми отримаємо 0 і повернемось знову до початкового індекс
def next_country(event):
    global current_country_index
    current_country_index = (current_country_index + 1) % len(countries)
    update_graph()

# Функція для оновлення графіку при натисканні кнопки "Попередній"
def prev_country(event):
    global current_country_index
    current_country_index = (current_country_index - 1) % len(countries)
    update_graph()

# Функція для оновлення графіку з поточною країною
def update_graph():
    #Зі зміної countries з використанням індексу отримуєм країну для створення поточного графіку 
    selected_country = countries[current_country_index]
    #З зміної grouped_sales вибираємо країну за допомогою зміної selected_country
    country_data = grouped_sales[grouped_sales['Країна'] == selected_country]
    # Побудова графіку з попереднім очищенням 
    ax.clear()
    ax.plot(country_data['Місяць-Рік'], country_data['Продажі'], marker='o')
    ax.set_title(f'Помісячні продажі у {selected_country}')
    ax.set_xlabel('Місяць-Рік')
    ax.set_ylabel('Продажі')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)
    plt.tight_layout()
    plt.draw()

# Створення кнопок "Наступний" та "Попередній"
fig, ax = plt.subplots(figsize=(12, 8))
button_next = Button(plt.axes([0.81, 0.05, 0.1, 0.04]), 'Наступний')
button_prev = Button(plt.axes([0.7, 0.05, 0.1, 0.04]), 'Попередній')

# Функції для кнопок
button_next.on_clicked(next_country)
button_prev.on_clicked(prev_country)

# Перша ініціалізація графіку
update_graph()

# Функція для відображення загального графіку з усіма країнами
def show_all_countries(event):
    ax.clear()
    for country in countries:
        country_data = grouped_sales[grouped_sales['Країна'] == country]
        ax.plot(country_data['Місяць-Рік'], country_data['Продажі'], label=country, marker='o')

    ax.set_title('Помісячні продажі за країнами')
    ax.set_xlabel('Місяць-Рік')
    ax.set_ylabel('Продажі')
    ax.tick_params(axis='x', rotation=45)
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.draw()

# Створення кнопки для відображення загального графіку
button_show_all = Button(plt.axes([0.45, 0.05, 0.15, 0.04]), 'Загальний графік')
button_show_all.on_clicked(show_all_countries)

plt.show()