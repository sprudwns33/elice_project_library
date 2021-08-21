from flask import Blueprint, render_template, request, url_for, session, flash, redirect
from models import *

bp = Blueprint('main', __name__, url_prefix='/')

# 메인페이지 / 이곳에는 최근 등록된 책의 목록(3가지?) - [슬라이드 형태] 및 대여가 가장 많았던 목록을 출력할 예정 
@bp.route('/')
def home():
    return render_template('main.html')
