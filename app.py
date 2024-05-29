from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)
port = 3000

@app.route('/Bok')
@app.route('/')
def get_books():
    # ↓ Bruk denne om du ønsker at APIen skal fungere med ubuntu serveren
    #with sqlite3.connect('/var/www/html/Backend/library-books.db', check_same_thread=False) as db:
    # ↓ Bruk denne om du ønsker at APIen skal fungere lokalt
    with sqlite3.connect('./library-books.db', check_same_thread=False) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Bok')
        rows = cursor.fetchall()
    return jsonify(rows)

@app.route('/Bok/<int:booknumber>', methods=['GET'])
def get_book_by_number(booknumber):
    with sqlite3.connect('./library-books.db', check_same_thread=False) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Bok WHERE booknumber = ?', (booknumber,))
        book = cursor.fetchone()
    if book:
        return jsonify({
            'success': True,
            'book': {
                'title': book[1],
                'author': book[2],
                'isbn': book[3],
                'booknumber': book[4],
                'image_path': book[5]
            }
        })
    else:
        return jsonify({'success': False, 'message': 'Bok ikke funnet'}), 404


@app.route('/filter/<string:search_string>')
def filter_books(search_string):
    # ↓ Bruk denne om du ønsker at APIen skal fungere med ubuntu serveren
    #with sqlite3.connect('/var/www/html/Backend/library-books.db', check_same_thread=False) as db:
    # ↓ Bruk denne om du ønsker at APIen skal fungere lokalt
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
    # ↓ Bruk denne om du ønsker at APIen skal fungere med ubuntu serveren
    #with sqlite3.connect('/var/www/html/Backend/library-books.db', check_same_thread=False) as db:
    # ↓ Bruk denne om du ønsker at APIen skal fungere lokalt
    with sqlite3.connect('./library-books.db', check_same_thread=False) as db:
        cursor = db.cursor()
        cursor.execute('DELETE FROM Bok WHERE booknumber = ?', (booknumber,))
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Boken finnes ikke i databasen'}), 404
    return jsonify({'message': 'Boken ble slettet fra databasen.'})

@app.route('/leggtilbok', methods=['POST'])
def add_book():
    if not request.json:
        return jsonify({'success': False, 'message': 'Request must be JSON'}), 400
    
    required_fields = ['title', 'author', 'isbn', 'booknumber']
    for field in required_fields:
        if field not in request.json:
            return jsonify({'success': False, 'message': f'Mangler verdien til: {field}'}), 400
    
    title = request.json['title']
    author = request.json['author']
    isbn = request.json['isbn']
    booknumber = request.json['booknumber']
    image_path = f'static/barcode/{booknumber}.png'
    
    try:
        # ↓ Bruk denne om du ønsker at APIen skal fungere med ubuntu serveren
        #with sqlite3.connect('/var/www/html/Backend/library-books.db', check_same_thread=False) as db:
        # ↓ Bruk denne om du ønsker at APIen skal fungere lokalt    
        with sqlite3.connect('./library-books.db', check_same_thread=False) as db:
            cursor = db.cursor()
            
            cursor.execute('''
            SELECT * FROM Bok
            WHERE title = ? AND author = ? AND isbn = ? AND booknumber = ?
            ''', (title, author, isbn, booknumber))
            
            if cursor.fetchone() is not None:
                return jsonify({'success': False, 'message': 'Boka finnes fra før'}), 409
      
            cursor.execute('''
            INSERT INTO Bok (title, author, isbn, booknumber, image_path)
            VALUES (?, ?, ?, ?, ?)
            ''', (title, author, isbn, booknumber, image_path))
            
            db.commit()
        
        return jsonify({'success': True, 'message': f'{title} ble registrert'}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/Låntakere')
def get_users():
    # ↓ Bruk denne om du ønsker at APIen skal fungere med ubuntu serveren
    #with sqlite3.connect('/var/www/html/Backend/library-books.db', check_same_thread=False) as db:
    # ↓ Bruk denne om du ønsker at APIen skal fungere lokalt
    with sqlite3.connect('./library-books.db', check_same_thread=False) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Låntakere')
        rows = cursor.fetchall()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True, port=port)