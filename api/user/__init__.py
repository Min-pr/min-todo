from flask_restx import Namespace

user_api = Namespace(name='user', path='/user', description='사용자와 관련된 API 모음입니다.')

