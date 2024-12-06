import sqlite3

# Подключение к базе данных (или создание, если её нет)
conn = sqlite3.connect('db.sqlite3')

# Создание курсора для выполнения SQL-запросов
cursor = conn.cursor()

# Выполнение SQL-запроса для выбора данных из столбца username таблицы users
cursor.execute("SELECT task FROM tasks")

# Получение всех строк результата запроса
rows = cursor.fetchall()

# Вывод данных
for row in rows:
    print(row[0])

# Закрытие курсора и соединения
cursor.close()
conn.close()