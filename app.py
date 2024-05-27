from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)
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

@app.route('/filter/<string:search_string>')
def filter_books(search_string):
    with sqlite3.connect('./library-books.db', check_same_thread=False) as db:
        cursor = db.cursor()
        query = '''
        SELECT * FROM Bok
        WHERE title LIKE ? OR author LIKE ?
        '''
        like_string = f'%{search_string}%'
        cursor.execute(query, (like_string, like_string))
        rows = cursor.fetchall()
    return jsonify(rows)

@app.route('/slett/<int:booknumber>', methods=['DELETE'])
def delete_book(booknumber):
    with sqlite3.connect('./library-books.db', check_same_thread=False) as db:
        cursor = db.cursor()
        cursor.execute('DELETE FROM Bok WHERE booknumber = ?', (booknumber,))
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Boken finnes ikke i databasen'}), 404
    return jsonify({'message': 'Boken ble slettet fra databasen.'})


if __name__ == '__main__':
    app.run(debug=True, port=port)