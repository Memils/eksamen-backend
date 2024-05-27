import sqlite3

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

books = [
    ('Skråpånatta', 'Lars Mytting', 9788205548387, 3),
    ('Atlas: Historien om Pa Salt', 'Lucinda Riley', 9788205548387, 4),
    ('Maskinen som tenker', 'Inga Strümke', 9788248926741, 6)
]

cursor.executemany('INSERT INTO Books(title, author, isbn, booknumber) VALUES (?, ?, ?, ?)', books)

conn.commit()
conn.close()