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