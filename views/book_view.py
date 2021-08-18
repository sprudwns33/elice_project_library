from flask import Blueprint, render_template, request, url_for, session, flash, redirect
from models import *

bp = Blueprint('book', __name__, url_prefix='/')

rows_page = 8

@bp.route('/bookList')
def books_list():
    books_val = LibraryBook.query.count()

    page = request.args.get('page', 1, type=int)
    book_list = LibraryBook.query.order_by(LibraryBook.id.desc()).paginate(page=page, per_page=rows_page)

    return render_template('book_list.html', book_list = book_list, books_val = books_val)

@bp.route('/bookList/<int:book_id>')
def book_info(book_id):
    book_info = LibraryBook.query.filter(LibraryBook.id == book_id).first()
    return render_template('book_info.html', book_info = book_info)