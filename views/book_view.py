from flask import Blueprint, render_template, request, url_for, session, flash, redirect
from models import *

bp = Blueprint('book', __name__, url_prefix='/')

rows_page = 8

@bp.route('/bookList')
def books_list():
    books_val = LibraryBook.query.count()

    page = request.args.get('page', 1, type=int)
    book_list = LibraryBook.query.order_by(LibraryBook.id.desc()).paginate(page=page, per_page=rows_page)

    print(books_val)

    return render_template('bookList.html', book_list = book_list, books_val = books_val)