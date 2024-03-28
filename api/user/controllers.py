from http import HTTPStatus  # HTTP 상태 코드를 사용하기 위한 라이브러리

from flask_restx import Resource, fields # Flask RESTful API 구축을 위한 라이브러리
from api.user.services import create_user, delete_user, get_user_by_email, sign_in, update_user, get_user_by_id # 사용자 서비스 함수
from util.logging_util import logger  # 로깅 유틸리티

from api.user import user_api
from flask_jwt_extended import get_jwt_identity, jwt_required  # JWT 토큰에서 신원 정보(일반적으로 사용자 식별자)를 추출하는 함수


# 사용자 이메일 필드 정의
email_field = fields.String(
    required=True,
    title="사용자 이메일",
    description="아이디로 사용됨",
    example="dev@52g.team",
    pattern="([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+",
)

# 사용자 비밀번호 필드 정의
password_field = fields.String(
    required=True,
    title="사용자 비밀번호",
    description="4자리 이상",
    example="1234",
    min_length=4,
)

# 사용자 전화번호 필드 정의
mobile_field = fields.String(
    required=True,
    title="사용자 전화번호",
    description="- 없음, 비번찾기 시 사용",
    example="01012345678",
    pattern="^[0-9]+$",
    min_length=11,
    max_length=11,
)

# 사용자 이름 필드 정의
name_field = fields.String(
    required=True, title="사용자 이름", description="사용자 이름", example="홍길동"
)

# 사용자 읽기 전용 모델 정의
user_read_model = user_api.model(
    "UserReadOnlyModel",
    {
        "email": email_field,
        "name": name_field,
        "mobile": mobile_field,
    },
)

# 수정 모델
user_update_model = user_api.model(
    "UserUpdateOnlyModel",
    {
        "email": email_field,
        "name": name_field,
        "mobile": mobile_field,
    },
)


# 성공 응답 모델 정의
ok_response_model = user_api.model(
    "OKResponseModel",
    {
        "status": fields.String(
            required=True, title="상태 설명", description="성공시 OK", example="OK"
        )
    },
)

# 사용자 생성 요청 모델 재정의
user_readonly_model = user_api.model(
    "UserPostRequestModel",
    {
        "email": email_field,
        "password": password_field,
        "name": name_field,
        "mobile": mobile_field
    },
)

# 로그인 요청 모델 정의
sign_in_request_model = user_api.model('SignInRequestModel', {
    'email': email_field,
    'password': fields.String(**password_field.schema(), required=False)
})

# 로그인 응답 모델 정의
sign_in_response_model = user_api.model('SignInResponseModel', {
    'jwt_token': fields.String(title='JWT 토큰', description="세션 키로서 사용됨"),
    'user': fields.Nested(user_readonly_model)
})


@user_api.route("/", strict_slashes=False)
class User(Resource):

    @jwt_required()
    @user_api.expect(user_update_model, validate=True)
    @user_api.marshal_with(user_update_model, envelope='data')
    def put(self):
        """사용자 정보 수정"""
        user_id = get_jwt_identity()
        update_post_request = user_api.payload
        user = update_user(user_id, update_post_request)  # 사용자 조회 함수 호출

        return user, HTTPStatus.OK  # 사용자 정보와 함께 성공 응답 반환

    @jwt_required()
    def delete(self):
        """사용자 삭제"""
        user_id = get_jwt_identity()  # JWT 토큰에서 사용자 이메일(신원) 추출
        delete_user(user_id)  # 사용자 삭제 함수 호출
        return {"status" : "OK"}, HTTPStatus.OK


@user_api.route('/signin', strict_slashes=False)
class UserSignIn(Resource):
    @user_api.expect(sign_in_request_model, validate=True)
    @user_api.marshal_with(sign_in_response_model, envelope='data')
    def post(self):
        """로그인 메소드"""
        signin_post_request = user_api.payload  # 요청 본문에서 로그인 정보를 가져옴

        email = signin_post_request.get('email')
        password = signin_post_request.get('password')

        access_token = sign_in(email, password)  # 로그인 함수 호출

        return {'jwt_token': access_token}, HTTPStatus.OK  # JWT 토큰과 함께 성공 응답 반환


@user_api.route('/signup', strict_slashes=False)
class UserSignUp(Resource):
    @user_api.expect(user_readonly_model)
    def post(self):
        """회원가입"""
        signup_post_request = user_api.payload  # 요청 본문에서 사용자 정보를 가져옴
        logger.debug(f"signup_post_request:{signup_post_request}")  # 로깅
        user = create_user(signup_post_request)  # 사용자 생성 함수 호출
        if user:
            return {"user_id": user.id, "status" : "OK"}, HTTPStatus.CREATED  # 성공 응답
        else:
            return {"status" : "FAIL"}, HTTPStatus.BAD_REQUEST  # 실패 응답