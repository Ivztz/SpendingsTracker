import sqlite3

# Connect to database
connection = sqlite3.connect("spendings.db")
cursor = connection.cursor()

# Create users table
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, \
               username TEXT NOT NULL, password TEXT NOT NULL)")

cursor.execute("CREATE UNIQUE INDEX username ON users (username)")

# Create budget table
cursor.execute("CREATE TABLE budgets (id INTEGER PRIMARY KEY AUTOINCREMENT, \
               user_id INTEGER NOT NULL, budget NUMERIC NOT NULL)")

# Create spendings table
cursor.execute("CREATE TABLE spendings (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
               user_id INTEGER NOT NULL, category TEXT NOT NULL, amount REAL NOT NULL, timestamp DATETIME NOT NULL)")

# Commit and close connection
connection.commit()
connection.close()