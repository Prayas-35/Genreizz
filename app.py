from flask import Flask, render_template, request, redirect, session, jsonify
from flask_session import Session
from helpers import search_books, login_required, best_sellers, fetch_books
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
import random
import asyncio


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.permanent_session_lifetime = timedelta(days=5)

db = SQL("sqlite:///genreizz.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    '''redirects to the login page if not signed in else shows bestseller books'''

    if session.permanent:
        return redirect('/bestsellers')

    return redirect('/login')

@app.route('/login', methods=["GET", "POST"])
def login():
    '''log users in'''

    if request.method == 'GET':
        if session.permanent:
            return redirect('/bestsellers')
        
        else:
            return render_template('login.html')
    
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        users = db.execute("SELECT username FROM users")
        for i in users:
            if username == i['username']:
                user = db.execute("SELECT password, user_id FROM users WHERE username = ?", username)
                if check_password_hash(user[0]['password'], password):
                    session['user_id'] = user[0]['user_id']
                    session.permanent = True
                    return redirect('/bestsellers')
            
                else:
                    alert = "Incorrect username or password!"
                    return render_template('login.html', alert = alert) #to add a msg if login credentials are incorrect
        
        alert = "Incorrect username or password!"
        return render_template('login.html', alert = alert)

@app.route('/register', methods=["GET", "POST"])
def register():
    '''register users'''

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = generate_password_hash(request.form.get("password"))
        confirm_password = request.form.get("confirm_password")

        if not check_password_hash(password, confirm_password):
            return render_template('signup.html', alert = "Passwords do not match. Please try again.")

        users = db.execute("SELECT username, email FROM users")

        for user in users:
            if username == user['username']:
                return render_template('signup.html', alert = "Username already exists. Try a different username.") #to add a msg if username already exists
            
            elif email == user['email']:
                return render_template('signup.html', alert = "The account already exists with this email.") #to add a msg if email already exists
            
        db.execute("INSERT INTO users (username, email, password) VALUES(?, ?, ?)", username, email, password)
        id = db.execute("SELECT user_id FROM users WHERE username = ?", username)
        session['user_id'] = id[0]['user_id']
        session.permanent = True
        return redirect('/bestsellers')
    
    return render_template("signup.html")

@app.route('/recommendations')
@login_required
def dashboard():
    '''gives recommendations based on users most read genres and authors'''

    user_id = session['user_id']
    user_books = db.execute("SELECT genre, author FROM books WHERE user_id = ?", user_id)

    genres = []
    for book in user_books:
        genres.append(book['genre'])
    unique_genres = list(set(genres))

    authors = []
    for book in user_books:
        authors.append(book['author'])
    unique_authors = list(set(authors))

    books_genres, books_authors = asyncio.run(fetch_books(unique_genres, unique_authors))

    books = books_genres + books_authors
    random.shuffle(books)
    
    unique_books = []
    seen_ids = set()
    for book in books:
        if book['id'] not in seen_ids:
            unique_books.append(book)
            seen_ids.add(book['id'])

    # return unique_books
    return render_template('dashboard.html', books=unique_books, length=len(books))

@app.route('/bookshelf')
@login_required
def bookshelf():
    '''shows users books'''

    user_id = session['user_id']
    books = db.execute("SELECT * FROM books WHERE user_id = ?", user_id)
    return render_template('mybooks.html', books = books)

@app.route('/search', methods=["GET", "POST"])
@login_required
def search():
    '''search books on given query'''

    if request.method == "POST":
        query = request.form.get("query")
        books = search_books(query)

        # return books
        return render_template('search.html', books = books)
    
    return render_template('search.html')

@app.route('/add', methods=["POST"])
@login_required
def add_book():
    '''adds books to bookshelf'''

    user_id = session['user_id']
    title = request.form.get("title")
    author = request.form.get("author")
    genre = request.form.get("genre")
    isbn = request.form.get("isbn")
    image = request.form.get("image")

    try:
        db.execute("INSERT INTO books (user_id, title, author, genre, isbn, image) VALUES (?, ?, ?, ?, ?, ?)",
                   user_id, title, author, genre, isbn, image)
        return jsonify({"success": True, "message": 'Book added to your library!'}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route('/readlist')
def readlist():
    '''shows users readlist'''

    user_id = session['user_id']
    books = db.execute("SELECT * FROM readlist WHERE user_id = ?", user_id)
    return render_template('readlist.html', books = books)
    
@app.route('/add_read', methods=["POST"])
@login_required
def add_book_readlist():
    '''adds book to readlist'''

    user_id = session['user_id']
    title = request.form.get("title")
    author = request.form.get("author")
    genre = request.form.get("genre")
    isbn = request.form.get("isbn")
    image = request.form.get("image")

    try:
        db.execute("INSERT INTO readlist (user_id, title, author, genre, isbn, image) VALUES (?, ?, ?, ?, ?, ?)",
                   user_id, title, author, genre, isbn, image)
        return jsonify({"success": True, "message": 'Book added to readlist!'}), 200
    except Exception as e:
        print(e)
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/delete/<int:id>', methods=["POST"])
@login_required
def delete_book(id):
    '''removes book from bookshelf'''

    db.execute("DELETE FROM books WHERE id = ?", id)
    return redirect('/bookshelf')

@app.route('/delete_readlist/<int:id>', methods=["POST"])
@login_required
def delete_read(id):
    '''removes book from readlist'''

    db.execute("DELETE FROM readlist WHERE id = ?", id)
    return redirect('/readlist')

@app.route('/bestsellers')
@login_required
def bestsellers():
    '''shows best-selling books'''

    bestbooks = best_sellers()
    random.shuffle(bestbooks)
    unique_books = []

    seen_isbns = set()
    seen_ids = set()
    seen_authors = set()
    seen_title = set()
    for book in bestbooks:
        author = book['authors'][0] if book.get('authors') and len(book['authors']) > 0 else None
        if (
            book['id'] not in seen_ids and
            book['isbn'] not in seen_isbns and
            author is not None and
            author not in seen_authors and
            book['title'] not in seen_title
        ):
            unique_books.append(book)
            seen_ids.add(book['id'])
            seen_isbns.add(book['isbn'])
            seen_authors.add(author)
            seen_title.add(book['title'])

    return render_template('bestsellers.html', books=unique_books, length=len(bestbooks))

@app.route('/logout')
def logout():
    '''log users out'''
    
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
