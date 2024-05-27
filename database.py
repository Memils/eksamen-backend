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
    booknumber INTEGER,
    image_path TEXT
)''')

with open('bøker.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    books = []
    for row in reader:
        title = row['Tittel']
        author = row['Forfatter']
        isbn = int(row['ISBN'])
        booknumber = int(row['Strekkode'])
        image_path = f'static/barcode/{booknumber}.png'  
        books.append((title, author, isbn, booknumber, image_path))


cursor.executemany('INSERT INTO Books(title, author, isbn, booknumber, image_path) VALUES (?, ?, ?, ?, ?)', books)

conn.commit()
conn.close()