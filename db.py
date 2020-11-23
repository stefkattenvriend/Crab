import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")
cursor = conn.cursor()

sql_file = open("schema.sql")
sql_as_string = sql_file.read()
cursor.executescript(sql_as_string)
print("Table created successfully")

conn.close()