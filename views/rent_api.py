from flask import Blueprint, render_template, request, url_for, session, flash, redirect
from models import *
from datetime import datetime

bp = Blueprint('rent', __name__, url_prefix='/')

# 책의 대여 현황 리스트를 출력하는 api
@bp.route('/rentalList')
def rental_list():

    rental_book = RentalBook.query.filter(RentalBook.return_date == None).filter(RentalBook.user_email == session['user_email']).all()

    return render_template('rental_list.html', rental_book = rental_book)

# 대여하기 버튼을 눌렀을 때 동작하는 api
@bp.route('/rentalBook')
def rental_book():
    book_id = request.args.get('book_id')
    current_path = request.args.get('current_path')

    # 대여하기 도중 책의재고가 모두 소진되었을 경우 에러 반환
    book_info = LibraryBook.query.filter(LibraryBook.id == book_id).first()
    if book_info.remaining == 0:
        flash("재고가 없어 대여가 불가능합니다.", 'error')
        return redirect(f'{current_path}')
    book_info.remaining -= 1
    book_info.rental_val += 1

    rental_books = RentalBook.query.filter(RentalBook.return_date == None).filter(RentalBook.user_email == session['user_email']).all()

    for book in rental_books:
        if book.book_id == int(book_id):
            flash("이미 대여한 책입니다. 반납하기 목록에서 현재 대여목록을 확인 바랍니다.", 'error')
            return redirect(f'{current_path}')

    if len(rental_books) >= 4:
        flash("대여 가능한 책은 4권까지 입니다. 대여 중인 책을 반납 후 이용해주세요.", 'error')
        return redirect(f'{current_path}')

    current_date = datetime.now()
    current_date = f'{current_date.year}-{current_date.month}-{current_date.day}'

    rental_info = RentalBook(user_email=session['user_email'],book_id=book_id,rental_date=current_date)
    db.session.add(rental_info)
    db.session.commit()

    flash("대여 완료하였습니다. 반납하기 목록에서 현재 대여목록을 확인 바랍니다.")
    return redirect(f'{current_path}')

# 대여 현황에서 반납하기 버튼을 클릭하였을 때 동작하는 api
@bp.route('/returnBook')
def return_book():
    book_id = request.args.get('book_id')

    # 반납되는 현재시간을 가져오는 로직
    now = datetime.now()
    return_time = f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}"

    rental_book = RentalBook.query.filter(RentalBook.user_email == session['user_email']).filter(RentalBook.return_date == None).filter(RentalBook.book_id == book_id).first()
    rental_book.return_date = return_time

    book_info = LibraryBook.query.filter(LibraryBook.id == book_id).first()
    book_info.remaining += 1

    db.session.commit()
    
    flash("반납이 완료되었습니다.")
    return redirect('/rentalList')

# 대여기록 출력하는 api
@bp.route('/returnList')
def return_list():

    return_book = RentalBook.query.filter(RentalBook.return_date != None).filter(RentalBook.user_email == session['user_email']).order_by(RentalBook.return_date.desc()).all()

    return render_template('return_book.html', return_book = return_book)