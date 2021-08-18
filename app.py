from flask import Flask
from db_connect import db
import config

def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    from views import user_view, book_view
    app.register_blueprint(user_view.bp)
    app.register_blueprint(book_view.bp)

    # session 사용을 위한
    app.secret_key = "testestsetestestst"
    app.config['SESSION_TYPE'] = 'filesystem'

    return app

if __name__ == "__main__":
    create_app().run(debug=True, port=1234)