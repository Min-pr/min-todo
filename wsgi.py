import traceback  # 에러 발생 시, 스택 추적 정보를 출력하기 위한 모듈
from http import HTTPStatus  # HTTP 상태 코드를 제공하는 모듈

from api import create_app  # API 애플리케이션을 생성하는 함수가 정의된 모듈
from util.logging_util import logger  # 로깅을 위한 유틸리티 모듈

app = create_app()  # Flask 애플리케이션 인스턴스를 생성

@app.errorhandler(Exception)  # Flask 애플리케이션에서 발생하는 모든 예외를 처리
def handle_root_exception(error):
    # 발생한 예외에 대한 스택 추적 로그를 기록
    logger.error(f"flask errorhandler occurred:{traceback.print_exc()}")
    try:
        # 에러 객체에서 사용자 정의 메시지를 가져옴
        message = error.message
    except AttributeError:
        # 에러 객체에 message 속성이 없는 경우, 에러 객체를 문자열로 변환하여 메시지로 사용
        message = str(error)

    try:
        # 에러 객체에서 HTTP 상태 코드를 가져옴
        code = error.code
        # 상태 코드가 정상 범위를 벗어나는 경우, 내부 서버 오류 코드로 설정
        if 100 > code or code >= 600:
            code = HTTPStatus.INTERNAL_SERVER_ERROR
    except AttributeError:
        # 에러 객체에 code 속성이 없는 경우, 내부 서버 오류 코드로 설정
        code = HTTPStatus.INTERNAL_SERVER_ERROR
    except TypeError:
        # code 속성이 잘못된 타입인 경우, 내부 서버 오류 코드로 설정
        code = HTTPStatus.INTERNAL_SERVER_ERROR

    try:
        # 추가적인 에러 코드 정보를 가져옴
        error_code = error.error_code
    except AttributeError as e:
        # 에러 코드 정보가 없는 경우, 경고 로그를 기록하고 기본 에러 코드를 설정
        logger.warning(f"No error_code in AttributeError:{e}")
        if 400 <= code < 500:
            error_code = "Flask request error"
        else:
            error_code = "Flask internal error"

    # 최종 에러 로그를 기록하고, 클라이언트에게 에러 정보를 담은 응답을 반환
    logger.error(f"message:{message}, errorCode:{error_code}, error:{error}, code:{code}")
    return {
        "message": message,
        "errorCode": error_code,
        "error": error.__class__.__name__,
    }, code


if __name__ == "__main__":
    # 애플리케이션을 로컬 서버에서 실행. 모듈이 재로딩될 때 use_reloader=False로 설정하여 중복 실행을 방지
    app.run(host="0.0.0.0", debug=True, port=8080)
