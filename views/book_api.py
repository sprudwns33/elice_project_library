from flask import Blueprint, render_template, request, url_for, session, flash, redirect
from models import *
from datetime import datetime

bp = Blueprint('book', __name__, url_prefix='/')

rows_page = 8

# 책의 전체 리스트를 출력하는 api
@bp.route('/bookList')
def books_list():
    books_val = LibraryBook.query.count()
    # 페이지네이션 기능을 쉽게 해주는 코드
    page = request.args.get('page', 1, type=int)
    book_list = LibraryBook.query.order_by(LibraryBook.id.desc()).paginate(page=page, per_page=rows_page)

    return render_template('book_list.html', book_list = book_list, books_val = books_val)

# 책의 상세정보를 나타내는 api
@bp.route('/bookList/<int:book_id>')
def book_info(book_id):
    book_info = LibraryBook.query.filter(LibraryBook.id == book_id).first()
    review_info = LibraryReview.query.filter(LibraryReview.book_id == book_id).order_by(LibraryReview.write_time.desc()).all()

    return render_template('book_info.html', book_info = book_info, review_info=review_info)

# 책에 대한 리뷰를 작성하는 api
@bp.route('/write_review/<int:book_id>', methods=['POST'])
def write_review(book_id):
    rating = int(request.form['star'])
    content = request.form['review']

    rental_record = RentalBook.query.filter(RentalBook.book_id == book_id).filter(RentalBook.user_email == session['user_email']).all()
    if len(rental_record) == 0:
        flash('한번 이상 대여 후 리뷰를 작성해주세요.', 'error')
        return redirect(f'/bookList/{book_id}')

    review_record = LibraryReview.query.filter(LibraryReview.user_email == session['user_email']).first()
    if review_record:
        flash("이미 리뷰를 작성하였습니다.", 'error')
        return redirect(f'/bookList/{book_id}')

    # 현재 시간을 받아 f스트링을 이용하여 원하는 형식으로 변환
    now = datetime.now()
    write_time = f"{now.year}-{now.month}-{now.day} {now.hour}:{now.minute}:{now.second}"
    # 유저 이메일을 약간의 암호화를 거치는 과정
    user_email = session['user_email'].split('@')
    user_email_code = len(user_email[0]) // 2
    user_email = user_email[0][:user_email_code] + '*'*user_email_code + '@' + ''.join(user_email[1:])

    review = LibraryReview(user_name=session['user_name'], user_email=session['user_email'], content=content, rating=rating, book_id=book_id, write_time=write_time, user_email_code=user_email)

    db.session.add(review)

    # 댓글이 작성될 때 마다 book_id rating을 변경해주는 로직
    book_rating = 0
    books_rating = LibraryReview.query.filter(LibraryReview.book_id == book_id).all()
    for rat in books_rating:
        book_rating += rat.rating
    book_rating = round(book_rating / len(books_rating))

    update_rating_query = LibraryBook.query.filter(LibraryBook.id == book_id).first()
    update_rating_query.star = book_rating

    db.session.commit()
    flash("리뷰가 성공적으로 작성되었습니다.")
    return redirect(f'/bookList/{book_id}')

# 리뷰를 삭제하는 api / front에서 댓글을 작성한 유저에게만 삭제버튼이 활성화되도록 설정
@bp.route('/delete_review/<int:review_id>/<int:book_id>')
def delete_review(review_id, book_id):
    review_info = LibraryReview.query.filter(LibraryReview.id == review_id).first()
    db.session.delete(review_info)

    # 댓글이 삭제가 될 때에도 book_id rating을 변경해주는 로직
    book_rating = 0
    books_rating = LibraryReview.query.filter(LibraryReview.book_id == book_id).all()
    if not len(books_rating):
        book_rating = 0
    else:
        for rat in books_rating:
            book_rating += rat.rating
        book_rating = round(book_rating / len(books_rating))

    update_rating_query = LibraryBook.query.filter(LibraryBook.id == book_id).first()
    update_rating_query.star = book_rating

    db.session.commit()
    flash("삭제가 완료되었습니다.")
    
    return redirect(f'/bookList/{book_id}')

# 검색기능을 이용하여 book_list를 반환하는 api
@bp.route('/bookList/searchBook')
def search_book():
    radio_val = request.args.get('radios')
    search_val = request.args.get('search')
    page = request.args.get('page', 1, type=int)

    # radio_val 0 => 제목 기준으로 검색 / 1 => 출판사 기준으로 검색
    if radio_val == '0':
        books_val = LibraryBook.query.filter(LibraryBook.book_name.like(f"%{search_val}%")).count()
        book_list = LibraryBook.query.filter(LibraryBook.book_name.like(f"%{search_val}%")).order_by(LibraryBook.id.desc()).paginate(page=page, per_page=rows_page)
    else:
        books_val = LibraryBook.query.filter(LibraryBook.publisher.like(f"%{search_val}%")).count()
        book_list = LibraryBook.query.filter(LibraryBook.publisher.like(f"%{search_val}%")).order_by(LibraryBook.id.desc()).paginate(page=page, per_page=rows_page)
    return render_template('search_book.html', book_list=book_list, books_val = books_val, radio_val=radio_val, search_val = search_val)