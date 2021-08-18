from flask import Blueprint, render_template, request, url_for, session, flash, redirect
from models import *
from datetime import datetime

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
    review_info = LibraryReview.query.filter(LibraryReview.book_id == book_id).order_by(LibraryReview.write_time.desc()).all()

    return render_template('book_info.html', book_info = book_info, review_info=review_info)

@bp.route('/write_review/<int:book_id>', methods=['POST'])
def write_review(book_id):
    rating = int(request.form['star'])
    content = request.form['review']

    now = datetime.now()
    write_time = f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}"
    user_email = session['user_email'].split('@')
    user_email_code = len(user_email[0]) // 2
    user_email = user_email[0][:user_email_code] + '*'*user_email_code + '@' + ''.join(user_email[1:])

    review = LibraryReview(user_name=session['user_name'], user_email=session['user_email'], content=content, rating=rating, book_id=book_id, write_time=write_time, user_email_code=user_email)

    db.session.add(review)

    # book_id rating을 변경해주는 로직
    book_rating = 0
    books_rating = LibraryReview.query.filter(LibraryReview.book_id == book_id).all()
    for rat in books_rating:
        book_rating += rat.rating
    book_rating = book_rating // len(books_rating)

    update_rating_query = LibraryBook.query.filter(LibraryBook.id == book_id).first()
    update_rating_query.star = book_rating

    db.session.commit()
    flash("리뷰가 성공적으로 작성되었습니다.")
    return redirect(f'/bookList/{book_id}')

@bp.route('/delete_review/<int:review_id>/<int:book_id>')
def delete_review(review_id, book_id):
    review_info = LibraryReview.query.filter(LibraryReview.id == review_id).first()

    db.session.delete(review_info)
    db.session.commit()
    flash("삭제가 완료되었습니다.")
    
    return redirect(f'/bookList/{book_id}')