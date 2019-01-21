from flask import Blueprint, jsonify, request

from app.books.forms import Book
from app.books.utils import is_isbn_or_key
from app.books.forms import SearchForm

books = Blueprint('books', __name__)


@books.route('/book/search')
def search():
    form = SearchForm(request.args)
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        if isbn_or_key == 'isbn':
            result = Book.search_by_isbn(q)
        else:
            result = Book.search_by_keyword(q)
        return jsonify(result)
    else:
        return jsonify(form.errors)
