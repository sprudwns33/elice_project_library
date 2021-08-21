from db_connect import db

'''
model.py
이 파일은 데이터베이스의 제약 조건을 명시하는 파일입니다.
관계형 데이터베이스의 데이터를 객체랑 연결 시켜주는 것을 ORM (Object Relational Mapping) 이라고 불러요.
즉, 이 파일은 외부에 존재하는 DB를 서버에서 사용하기 위해, DB와 동일한 제약조건을 객체에 걸어버리는 겁니다.
'''
# 사용자 유저 테이블
class LibraryUser(db.Model):

    __tablename__  = 'libraryUser'

    id          = db.Column(db.Integer, primary_key=True, nullable=False) 
    email       = db.Column(db.String(255), nullable=False)
    password    = db.Column(db.String(255), nullable=False)
    name        = db.Column(db.String(20), nullable=False)

    def __init__(self, email, password, name):
        self.email    = email
        self.password = password
        self.name     = name
# 전체 책 목록 테이블
class LibraryBook(db.Model):

    __tablename__ = 'libraryBook'

    id               = db.Column(db.Integer, primary_key=True, nullable=False) 
    book_name        = db.Column(db.String(255), nullable=False)
    publisher        = db.Column(db.String(255), nullable=False)
    author           = db.Column(db.String(255), nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    pages            = db.Column(db.Integer, nullable=False)
    isbn             = db.Column(db.Integer, nullable=False)
    description      = db.Column(db.Text(), nullable=False)
    star             = db.Column(db.Integer, nullable=False)
    img_link         = db.Column(db.String(255), nullable=False)
    rental_val       = db.Column(db.Integer, nullable=False)
    remaining        = db.Column(db.Integer, nullable=False)
# 책에 대한 리뷰 테이블
class LibraryReview(db.Model):

    __tablename__ = 'libraryReview'

    id              = db.Column(db.Integer, primary_key=True, nullable=False) 
    user_name       = db.Column(db.String(255), nullable=False)
    user_email      = db.Column(db.String(255), nullable=False)
    content         = db.Column(db.Text(), nullable=False)
    rating          = db.Column(db.Integer, nullable=False)
    book_id         = db.Column(db.Integer,db.ForeignKey('libraryBook.id'), nullable=False)
    write_time      = db.Column(db.DateTime, nullable=False)
    user_email_code = db.Column(db.String(255), nullable=False)

    def __init__(self, user_name, user_email, content, rating, book_id, write_time, user_email_code):
        self.user_name       = user_name
        self.user_email      = user_email
        self.content         = content
        self.rating          = rating
        self.book_id         = book_id
        self.write_time      = write_time
        self.user_email_code = user_email_code
# 책의 대여된 현황 테이블
class RentalBook(db.Model):

    __tablename__ = 'rentalBook'

    id             = db.Column(db.Integer, primary_key=True, nullable=False) 
    user_email     = db.Column(db.Integer, nullable=False)
    book_id        = db.Column(db.Integer, db.ForeignKey('libraryBook.id'), nullable=False)
    rental_date    = db.Column(db.Date, nullable=False)
    book_data      = db.relationship('LibraryBook', foreign_keys='RentalBook.book_id')

    def __init__(self, user_email, book_id, rental_date):
        self.user_email     = user_email
        self.book_id        = book_id
        self.rental_date    = rental_date