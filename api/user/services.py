import uuid
from flask_bcrypt import generate_password_hash, check_password_hash
from exceptions import EntityNotFoundException, UserAlreadyExistException, InvalidValueException
from api.user.models import UserModel
from util.model_utils import update_model_from_args
from flask_jwt_extended import create_access_token
from util.time_utils import get_now


#이메일 기준
def get_user_by_email(email: str) -> UserModel:

    conditions = None
    conditions &= UserModel.email == email
    user = UserModel.scan(filter_condition=conditions)

    for i in user :
        return UserModel(**i.attribute_values)
    else :
        raise EntityNotFoundException(
            f"User {email} does not exist", EntityNotFoundException.__qualname__

        )

def get_user_by_id(id: str) -> UserModel:
    """id 기반으로 사용자를 조회"""
    try:
        user = UserModel.get(hash_key=id)
        return user
    except UserModel.DoesNotExist:
        # 사용자가 존재하지 않는 경우, 사용자 정의 예외 발생
        raise EntityNotFoundException(
            f"User {id} does not exist", EntityNotFoundException.__qualname__
        )

#회원가입
def create_user(user_request: dict) -> UserModel:
    email = user_request.get("email")
    try:
        user = get_user_by_email(email)
        raise UserAlreadyExistException(
            f"{email} already exists!", UserAlreadyExistException.__qualname__
        )

    except EntityNotFoundException:
        # 사용자가 존재하지 않는 경우, 새로운 사용자 생성
        pass

    user = UserModel()  # 사용자 모델 인스턴스 생성
    update_model_from_args(user, user_request)  # 요청 데이터를 모델에 업데이트
    # 비밀번호를 암호화하여 사용자 모델에 저장
    user.id=uuid.uuid4().hex
    user.password = generate_password_hash(user_request.get("password")).decode("utf-8")

    user.save()  # 사용자 정보 저장
    return user


def update_user(user_info: str, user_update_model: dict) -> UserModel:
    user = UserModel.get(hash_key=user_info)
    update_model_from_args(user,user_update_model)

    user.updated_at = get_now()
    user.save()
    return


def sign_in(email: str, password: str) -> (str, UserModel):
    """로그인 함수입니다. 이메일과 비밀번호를 검증 후 JWT 토큰을 생성합니다."""
    user = get_user_by_email(email)  # 사용자 조회
    if not check_password_hash(user.password, password):
        # 비밀번호가 일치하지 않는 경우, 사용자 정의 예외 발생
        raise InvalidValueException(f'Not matched the password', InvalidValueException.__qualname__)

    access_token = create_access_token(identity=user.id)  # JWT 토큰 생성
    user.last_login_at = get_now()  # 마지막 로그인 시간 업데이트
    user.save()  # 변경 사항 저장

    return access_token  # 생성된 JWT 토큰 반환

def delete_user(id: str):
    # 두개의 테이블을 all or nothing 으로 처리해야 하기 때문에 트랜잭션 처리
    user = UserModel.get(id)
    user.delete()



