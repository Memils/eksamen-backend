import sqlite3
import csv 

conn = sqlite3.connect('library-books.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Bok (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn INTEGER,
    booknumber INTEGER,
    image_path TEXT
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Låntakere (
    id INTEGER PRIMARY KEY,
    fornavn TEXT NOT NULL,
    etternavn TEXT NOT NULL,
    number TEXT NOT NULL,
    image_path TEXT,
    photo TEXT
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

cursor.executemany('INSERT INTO Bok(title, author, isbn, booknumber, image_path) VALUES (?, ?, ?, ?, ?)', books)

with open('låntakere.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    users = []
    for row in reader:
        fornavn = row['Fornavn']
        etternavn = row['Etternavn']
        number = int(row['Strekkode'])
        image_path = f'static/barcode/{number}.png'  
        photo = f'static/bilder/{number}.png'
        users.append((fornavn, etternavn, number, image_path, photo))

cursor.executemany('INSERT INTO Låntakere(fornavn, etternavn, number, image_path, photo) VALUES (?, ?, ?, ?, ?)', users)



conn.commit()
conn.close()