from db_connect import db

'''
model.py
이 파일은 데이터베이스의 제약 조건을 명시하는 파일입니다.
관계형 데이터베이스의 데이터를 객체랑 연결 시켜주는 것을 ORM (Object Relational Mapping) 이라고 불러요.
즉, 이 파일은 외부에 존재하는 DB를 서버에서 사용하기 위해, DB와 동일한 제약조건을 객체에 걸어버리는 겁니다.
'''

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

class LibraryReview(db.Model):

    __tablename__ = 'libraryReview'

    id              = db.Column(db.Integer, primary_key=True, nullable=False) 
    user_name       = db.Column(db.String(255), nullable=False)
    user_email      = db.Column(db.String(255), nullable=False)
    content         = db.Column(db.Text(), nullable=False)
    rating          = db.Column(db.Integer, nullable=False)
    book_id         = db.Column(db.Integer, nullable=False)
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