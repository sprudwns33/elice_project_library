from flask import Blueprint, render_template, request, url_for, session, flash, redirect
from models import *
from datetime import datetime

bp = Blueprint('rent', __name__, url_prefix='/')

@bp.route('/rentalList')
def rental_list():
    return render_template('rental_list.html')

@bp.route('/rentalBook')
def rental_book():
    book_id = request.args.get('book_id')
    current_path = request.args.get('current_path')

    book_info = LibraryBook.query.filter(LibraryBook.id == book_id).first()
    if book_info.remaining == 0:
        flash("재고가 없어 대여가 불가능합니다.", 'error')
        return redirect(f'{current_path}')
    book_info.remaining -= 1
    book_info.rental_val += 1

    rental_books = RentalBook.query.filter(RentalBook.user_email == session['user_email']).all()
    print(rental_books)

    for book in rental_books:
        if book.book_id == int(book_id):
            flash("이미 대여한 책입니다. 대여기록에서 확인 바랍니다.", 'error')
            return redirect(f'{current_path}')

    if len(rental_books) >= 5:
        flash("대여 가능한 책은 5권까지 입니다. 대여 중인 책을 반납 후 이용해주세요.", 'error')
        return redirect(f'{current_path}')

    current_date = datetime.now()
    current_date = f'{current_date.year}-{current_date.month}-{current_date.day}'

    rental_info = RentalBook(user_email=session['user_email'],book_id=book_id,rental_date=current_date)
    db.session.add(rental_info)
    db.session.commit()

    flash("대여 완료하였습니다. 대여기록에서 확인 바랍니다.")
    return redirect(f'{current_path}')

@bp.route('/returnBook')
def return_book():
    return render_template('return_book.html')