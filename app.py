from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
port = 3000

@app.route('/Bok')
@app.route('/')
def get_books():
    with sqlite3.connect('./library-books.db', check_same_thread=False) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Bok')
        rows = cursor.fetchall()
    return jsonify(rows)

@app.route('/Bok/<int:booknumber>')
def get_booknumber(booknumber):
    print(booknumber)
    with sqlite3.connect('./library-books.db', check_same_thread=False) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Bok WHERE booknumber = ?', (booknumber,))
        rows = cursor.fetchall()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True, port=port)