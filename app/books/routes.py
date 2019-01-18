from flask import Blueprint, jsonify

from app.books.forms import Book
from app.books.utils import is_isbn_or_key

books = Blueprint('books', __name__)


@books.route('/book/search/<q>/<page>')
def search(q, page):
    isbn_or_key = is_isbn_or_key(q)
    if isbn_or_key == 'isbn':
        result = Book.search_by_isbn(q)
    else:
        result = Book.search_by_keyword(q)
    return jsonify(result)
