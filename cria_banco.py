import sqlite3

connection = sqlite3.connect('banco.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (user_id text PRIMARY KEY, login text, keyword text)"
