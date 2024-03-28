import pynamodb
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model as DDBModel
from util.time_utils import get_now
from util.logging_util import logger
from contants import DEFAULT_REGION


class UserModel(DDBModel):
    """
    User Data Model for DDB
    """

    class Meta:
        billing_mode = pynamodb.constants.PAY_PER_REQUEST_BILLING_MODE
        table_name = "min_user"
        region = DEFAULT_REGION

    #인덱스
    id = UnicodeAttribute(hash_key=True)

    # 인증 정보
    email = UnicodeAttribute(null=False)
    password = UnicodeAttribute(null=False)


    # 기본 정보
    name = UnicodeAttribute(null=False)
    mobile = UnicodeAttribute(null=False)
    profile_image = UnicodeAttribute(null=True)


    # 생성/수정 일자
    created_at = UTCDateTimeAttribute(default=lambda: get_now())
    updated_at = UTCDateTimeAttribute(default=lambda: get_now())

    # 로그인 관련
    #scope = UnicodeAttribute(null=True)
    last_login_at = UTCDateTimeAttribute(null=True)

    def __repr__(self):
        return "<%r %r %r %r %r>" % (
            self.Meta.table_name,
            self.email,
            self.name,
            self.mobile,
            self.created_at,
        )


#pynamodb 자동 생성
if not UserModel.exists():
    UserModel.create_table(
        wait=True, billing_mode=pynamodb.constants.PAY_PER_REQUEST_BILLING_MODE
    )
    logger.get_logger("pynamodb").info("UserModel created!")
else:
    logger.get_logger("pynamodb").info("UserModel is already exists!")
