from flask import Blueprint
from app.books.utils import is_isbn_or_key

books = Blueprint('books', __name__)


@books.route('/book/search/<q>/<page>')
def search(q, page):
    is_isbn_or_key(q)
    pass
