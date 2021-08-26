from flask import Blueprint, render_template, request, url_for, session, flash, redirect
from werkzeug.utils import secure_filename
from models import *

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def home():
    recent_book = LibraryBook.query.order_by(LibraryBook.id.desc()).limit(3)
    best_book = LibraryBook.query.order_by(LibraryBook.rental_val.desc()).limit(5)
    return render_template('main.html', recent_book = recent_book, best_book = best_book)

#--------------------------------------관리자 기능------------------------------------------------------

@bp.route('/adminUser')
def admin_user():
    if session['user_email'] != 'admin@naver.com':
        return redirect('/')
    user_list = LibraryUser.query.filter(LibraryUser.email != session['user_email']).all()
    return render_template('admin_user.html', user_list=user_list)

@bp.route('/adminBook')
def admin_book():
    if session['user_email'] != 'admin@naver.com':
        return redirect('/')
    return render_template('admin_book.html')

@bp.route('/deleteUser/<int:user_id>')
def delete_user(user_id):
    print(user_id)
    user = LibraryUser.query.filter(LibraryUser.id == user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect('/adminUser')

@bp.route('/addBook', methods=["POST"])
def add_book():

    book_name        = request.form['book_name']
    publisher        = request.form['publisher']
    author           = request.form['author']
    publication_date = request.form['publication_date']
    pages            = request.form['pages']
    isbn             = request.form['isbn']
    description      = request.form['description']
    remaining        = request.form['remaining']

    img_file = request.files['img_file']
    img_file.save('D:\Project_Library\minkyungjun\static\img/' + secure_filename(img_file.filename))

    add_book = LibraryBook(book_name=book_name, publisher=publisher, author=author, publication_date=publication_date, pages=pages, isbn=isbn, description=description, img_link=img_file.filename, remaining=remaining)
    db.session.add(add_book)
    db.session.commit()

    return redirect('/adminBook')