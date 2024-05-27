import sqlite3
import csv 

conn = sqlite3.connect('library-books.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn INTEGER,
    booknumber INTEGER
)''')

with open('bøker.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    books = [(row['Tittel'], row['Forfatter'], int(row['ISBN']), int(row['Strekkode'])) for row in reader]

cursor.executemany('INSERT INTO Books(title, author, isbn, booknumber) VALUES (?, ?, ?, ?)', books)

conn.commit()
conn.close()