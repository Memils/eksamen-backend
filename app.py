from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
port = 3000

@app.route('/Books')
@app.route('/')
def get_books():
    with sqlite3.connect('./library-books.db', check_same_thread=False) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Books')
        rows = cursor.fetchall()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True, port=port)