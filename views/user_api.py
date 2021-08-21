from flask import Blueprint, render_template, request, url_for, session, flash, redirect
from models import *
import re
from bcrypt import hashpw, checkpw, gensalt

bp = Blueprint('user', __name__, url_prefix='/')

# 로그인 api
@bp.route('/login', methods=['POST'])
def login():
    current_path  = request.form['current_path']
    user_email    = request.form['login_email']
    
    user_data = LibraryUser.query.filter(LibraryUser.email == user_email).first()

    session.clear()
    session['user_name'] = user_data.name
    session['user_email'] = user_data.email

    return redirect(f'{current_path}')

# 로그아웃 api
@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# 회원가입 api
@bp.route('/register', methods=['POST'])
def register():
    user_email    = request.form['regi_email']
    user_name     = request.form['regi_name']
    password      = request.form['regi_password']
    current_path  = request.form['current_path']

    # 회원가입 도중 user_email이 중복되었을 경우 에러 반환
    email_ck = LibraryUser.query.filter(LibraryUser.email == user_email).first()
    if email_ck:
        flash("아이디 중복이 발생하였습니다. 회원가입을 재시도 해주세요.", 'error')
        return redirect(f'{current_path}')

    password = hashpw(password.encode('utf-8'), gensalt())
    password = password.decode('utf-8')
    user = LibraryUser(email=user_email, password=password, name=user_name)
    db.session.add(user)
    db.session.commit()

    flash("회원가입이 완료되었습니다. 로그인 해주세요.")
    return redirect(f'{current_path}')

# 회원가입의 아이디 중복체크 api
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

# 로그인 시 ajax를 통해 데이터가 일치하는지 확인하는 api
@bp.route('/loginCheck', methods=['POST'])
def login_check():
    user_email = request.form['login_email']
    password  = request.form['login_password']
    # return 2 : 비밀번호 8자리 이하 입력시 / 에러
    # return 0 : 존재하지 않는 아이디 / 에러
    # return 1 : 로그인 성공
    # return 3 : 비밀번호 일치 하지 않음 / 에러
    if len(password) < 8: return '2'

    result = LibraryUser.query.filter(LibraryUser.email == user_email).first()

    if result == None: return '0'

    if checkpw(password.encode('utf-8'), result.password.encode('utf-8')):
        return '1'
    else: return '3'

