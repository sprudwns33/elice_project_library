# 어느 데이터베이스를 사용할지 연동해주는 코드
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost:3306/library_project'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 이걸 켜면 메모리 사용량이 늘어나서, 꺼주는게 좋아요.