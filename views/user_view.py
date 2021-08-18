from flask import Blueprint, render_template, request, url_for, session, flash, redirect
from models import *
import re
from bcrypt import hashpw, checkpw, gensalt

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def home():
    user_list = LibraryUser.query.order_by(LibraryUser.id.asc()).all()
    return render_template('main.html', user_list=user_list)

@bp.route('/bookList')
def test1():
    return render_template('bookList.html')

@bp.route('/rentalList')
def test2():
    return render_template('rentalList.html')

@bp.route('/login', methods=['POST'])
def login():
    current_path = request.form['current_path']
    user_email    = request.form['login_email']
    
    user_data = LibraryUser.query.filter(LibraryUser.email == user_email).first()

    session.clear()
    session['user_name'] = user_data.name

    return redirect(f'{current_path}')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@bp.route('/register', methods=['POST'])
def register():
    user_email    = request.form['regi_email']
    user_name     = request.form['regi_name']
    password     = request.form['regi_password']
    current_path = request.form['current_path']

    password = hashpw(password.encode('utf-8'), gensalt())
    password = password.decode('utf-8')
    user = LibraryUser(email=user_email, password=password, name=user_name)
    db.session.add(user)
    db.session.commit()

    return redirect(f'{current_path}')

@bp.route('/idCheck', methods=['POST'])
def id_check():
    user_email = request.form['regi_email']
    regex = re.compile('.+[@]{1}.+[.].+')
    matchobj = regex.match(user_email)
    # return 0은 아이디 중복 없음 / 1은 아이디 중복 / 2는 이메일 형식 X
    if matchobj == None:
        return '2'
    result = LibraryUser.query.filter(LibraryUser.email == user_email).count()
    return str(result)

@bp.route('/loginCheck', methods=['POST'])
def login_check():
    user_email = request.form['login_email']
    password  = request.form['login_password']

    result = LibraryUser.query.filter(LibraryUser.email == user_email).first()

    if result == None: return '0'

    if checkpw(password.encode('utf-8'), result.password.encode('utf-8')):
        return '1'
    else: return '2'

