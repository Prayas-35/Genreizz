import requests
from functools import wraps
from flask import session, redirect
import random
import math
import asyncio
import aiohttp


async def fetch_books(unique_genres, unique_authors):
    books_genres_task = get_books_by_genre(unique_genres)
    books_authors_task = get_books_by_authors(unique_authors)
    
    books_genres, books_authors = await asyncio.gather(books_genres_task, books_authors_task)
    
    return books_genres, books_authors


async def fetch(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        else:
            return {"error": response.status}


async def get_books_by_genre(genres):
    """This function takes a list of genres as an argument and returns a list of books in that genre."""
    books = []
    print("getting books by genre")
    async with aiohttp.ClientSession() as session:
        tasks = []
        for genre in genres:
            url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&printType=books"
            tasks.append(fetch(session, url))

        responses = await asyncio.gather(*tasks)

        for response, genre in zip(responses, genres):
            if "error" in response:
                continue

            total_items = response.get('totalItems', 0)
            if total_items == 0:
                continue

            results = random.randint(10, 20)
            max_results = results if results % 2 == 0 else results + 1
            start_index = random.randint(0, max(math.floor((total_items - max_results) / 10), 0))

            url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&maxResults={max_results}&printType=books&startIndex={start_index}"
            second_response = await fetch(session, url)

            if 'items' in second_response:
                for item in second_response['items']:
                    volume_info = item['volumeInfo']
                    book = {
                        'title': volume_info['title'],
                        'image': volume_info.get('imageLinks', {}).get('thumbnail', "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"),
                        'id': item['id'],
                        'authors': volume_info.get('authors', []),
                        'genre': volume_info.get('categories', []),
                        'isbn': next((identifier['identifier'] for identifier in volume_info.get('industryIdentifiers', [])), None)
                    }
                    books.append(book)
    print("got books by genre")
    return books

async def get_books_by_authors(authors):
    """This function takes a list of authors as an argument and returns a list of books by those authors."""
    books = []
    print("getting books by authors")
    async with aiohttp.ClientSession() as session:
        tasks = []
        for author in authors:
            url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}&printType=books"
            tasks.append(fetch(session, url))

        responses = await asyncio.gather(*tasks)

        for response, author in zip(responses, authors):
            if "error" in response:
                continue

            total_items = response.get('totalItems', 0)
            if total_items == 0:
                continue

            results = random.randint(10, 20)
            max_results = results if results % 2 == 0 else results + 1
            start_index = random.randint(0, max(math.floor((total_items - max_results) / 10), 0))

            url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}&maxResults={max_results}&printType=books&startIndex={start_index}"
            second_response = await fetch(session, url)

            if 'items' in second_response:
                for item in second_response['items']:
                    volume_info = item['volumeInfo']
                    book = {
                        'title': volume_info['title'],
                        'image': volume_info.get('imageLinks', {}).get('thumbnail', "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"),
                        'id': item['id'],
                        'authors': volume_info.get('authors', []),
                        'genre': volume_info.get('categories', []),
                        'isbn': next((identifier['identifier'] for identifier in volume_info.get('industryIdentifiers', [])), None)
                    }
                    books.append(book)
    print("got books by authors")
    return books


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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

if __name__ == '__main__':
    pass