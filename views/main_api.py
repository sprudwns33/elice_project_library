from flask import Blueprint, render_template, request, url_for, session, flash, redirect
from models import *

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def home():
    recent_book = LibraryBook.query.order_by(LibraryBook.id.desc()).limit(3)
    best_book = LibraryBook.query.order_by(LibraryBook.rental_val.desc()).limit(5)
    return render_template('main.html', recent_book = recent_book, best_book = best_book)
