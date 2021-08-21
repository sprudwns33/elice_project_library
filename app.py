from flask import Flask
from db_connect import db
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    # 무한루프 방지를 위해 creat_app 내부에 import 선언 / api를 연동
    from views import user_api, book_api, rent_api, main_api
    app.register_blueprint(main_api.bp)
    app.register_blueprint(user_api.bp)
    app.register_blueprint(book_api.bp)
    app.register_blueprint(rent_api.bp)

    # session 사용을 위한 코드
    app.secret_key = "testestsetestestst"
    app.config['SESSION_TYPE'] = 'filesystem'

    return app

if __name__ == "__main__":
    create_app().run(debug=True, port=1234)