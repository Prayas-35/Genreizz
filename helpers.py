import requests
from functools import wraps
from flask import session, redirect
import random
import math

def get_genre_by_book(title):
    """this function takes a book title as an argument and returns the genre of the book."""

    url = f"https://www.googleapis.com/books/v1/volumes?q={title}"

    response = requests.get(url)
    categories = []
    
    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            for i in range(len(data['items'])):
                book_info = data['items'][i]
                volume_info = book_info['volumeInfo']
            
                # Categories usually contain the genres
                categories.append(volume_info.get('categories', []))
                
            categories_flat = list(set([genre for sublist in categories for genre in sublist]))    
            return categories_flat
        else:
            return "No items found for the given title."
        
    else:
        return f"Error: {response.status_code}"


def get_book_by_genre(genres):
    """this function takes a genre as an argument and returns a list of books in that genre."""
    books = []    
    for genre in genres:
        results = random.randint(10, 20)
        url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&maxResults={results if results%2 == 0 else results+1}&printType=books&startIndex={random.randint(0, math.floor(random.random()*100))}"

        response = requests.get(url)

        if response.status_code == 200:
                data = response.json()
                
                if 'items' in data:
                    for item in data['items']:
                        volume_info = item['volumeInfo']
                        book = {}

                        title = volume_info['title']
                        book['title'] = title
                        # book['image'] = volume_info.get('imageLinks', {}).get('thumbnail', None)
                        book['image'] = volume_info['imageLinks']['thumbnail'] if 'imageLinks' in volume_info else "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"
                        book['id'] = item['id']
                        book['authors'] = volume_info.get('authors', [])
                        book['genre'] = volume_info.get('categories', [])
                        isbn = volume_info.get('industryIdentifiers', [])
                        if isbn:
                            isbn = isbn[0].get('identifier')
                            book['isbn'] = isbn

                        else:
                            book['isbn'] = None
                        
                        books.append(book)

                # length = len(books)
                # return books
        else:
            return f"Error: {response.status_code}"
        
    return books


def get_book_by_isbn(isbn):
    """this function takes an ISBN as an argument and returns the title, author(s), and description of the book."""

    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            book_info = data['items'][0]
            volume_info = book_info['volumeInfo']
            book = {}

            title = volume_info['title']
            book['title'] = title
            authors = volume_info.get('authors')
            # for author in authors:
            #     book['authors'] = author
            book['authors'] = authors
            # description = volume_info.get('description', "")
            # book['description'] = description
            return book
        else:
            return "No items found for the given ISBN."
    else:
        return f"Error: {response.status_code}"


def search_books(query):
    """this function takes a query as an argument and returns a list of books that match the query."""
    results = random.randint(10, 20)
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults={results if results%2 == 0 else results+1}&printType=books"

    response = requests.get(url)

    if response.status_code == 200:
        print('here1')
        data = response.json()
        books = []
        if 'items' in data:
            for item in data['items']:
                volume_info = item['volumeInfo']
                book = {}

                book['message'] = None
                book['code'] = 200
                title = volume_info['title']
                book['title'] = title
                isbn = volume_info.get('industryIdentifiers', [])
                id = item['id']
                book['id'] = id
                book['image'] = volume_info['imageLinks']['thumbnail'] if 'imageLinks' in volume_info else "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"
                book['genre'] = volume_info.get('categories', [])

                authors = volume_info.get('authors') if 'authors' in volume_info else []
                book['authors'] = authors

                if isbn:
                    isbn = isbn[0].get('identifier')
                    book['isbn'] = isbn

                else:
                    book['isbn'] = None
                
                books.append(book)

        return books
    
    elif response.status_code == 400:
        print('here')
        data = response.json()
        books = []
        book = {}
        book['message'] = "Missing Book Name"
        book['code'] = data['error']['code']
        book['title'] = None
        book['authors'] = None
        book['genre'] = None
        book['isbn'] = None
        book['image'] = None
        book['id'] = None
        books.append(book)

        return books

    else:
        return f"Error: {response.status_code}"

def get_book_by_id(book_id):
    url = f"https://www.googleapis.com/books/v1/volumes/{book_id}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # print(data)
        if data:
            book_info = data
            volume_info = book_info['volumeInfo']
            book = {}

            title = volume_info['title']
            book['title'] = title
            authors = volume_info.get('authors')
            book['authors'] = authors
            book['genre'] = volume_info.get('categories', [])
            return book
        else:
            return "No items found for the given id."
    else:
        return f"Error: {response.status_code}"

def get_image_by_id(book_id):
    url = f"https://www.googleapis.com/books/v1/volumes/{book_id}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # print(data)
        if data:
            book_info = data
            volume_info = book_info['volumeInfo']

            image = volume_info.get('imageLinks', {}).get('large', None)
            return image
        else:
            return "No items found for the given id."
    else:
        return f"Error: {response.status_code}"
    
def best_sellers():
    url = "https://www.googleapis.com/books/v1/volumes?q=best+sellers&orderBy=newest&langRestrict=en&maxResults=40&printType=books"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        books = []
        if 'items' in data:
            for item in data['items']:
                volume_info = item['volumeInfo']
                book = {}

                title = volume_info['title']
                book['title'] = title
                isbn = volume_info.get('industryIdentifiers', [])
                id = item['id']
                book['id'] = id
                book['image'] = get_image_by_id(id)

                authors = volume_info.get('authors')
                book['authors'] = authors

                if isbn:
                    isbn = isbn[0].get('identifier')
                    book['isbn'] = isbn

                else:
                    book['isbn'] = None
                
                books.append(book)

        length = len(books)
        return books, length
    else:
        return f"Error: {response.status_code}"


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

if __name__ == '__main__':
    # print(get_genre_by_book("goosebumps"))
    # print(get_book_by_genre("fiction"))
    # print(get_book_by_isbn("9780439554930"))
    print(search_books("harry potter"))
    # print(get_book_by_id("icKmd-tlvPMC"))
    pass