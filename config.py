import logging

from contants import SingletonInstance, get_config_from_param_store


# JWT
class JWTConfig(SingletonInstance):
    def __init__(self):
        # TODO: linkus와 통합 시, 하드 코딩된 키를 제거하고 캠프 통합 키를 사용하게 수정
        self.SECRET_KEY = get_config_from_param_store("/52g/bootcamp/min/jwt-secret-key")


# SQL Alchemy
# class SQLAlchemyConfig(SingletonInstance):
#     def __init__(self):
#         self.DB_HOST = get_config_from_param_store(f'/52g/template-flask/dev/db-host')
#         self.DB_USERNAME = get_config_from_param_store(f'/52g/template-flask/dev/db-username')
#         self.DB_PASSWORD = get_config_from_param_store(f'/52g/template-flask/dev/db-password')


# Flask Base Configuration
class BaseConfig(object):
    # Flask
    ENV = "development"
    DEBUG = False
    BUNDLE_ERRORS = True
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = JWTConfig.instance().SECRET_KEY
    # Restx
    RESTX_VALIDATE = True
    RESTX_MASK_SWAGGER = False
    # JWT
    JWT_ACCESS_TOKEN_EXPIRES = False
    LOG_LEVEL = logging.DEBUG
    # SQLAlchemy
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Flask Local Configuration
class LocalConfig(BaseConfig):
    DEBUG = True

    # PostgreSQL
    # @property
    # def SQLALCHEMY_DATABASE_URI(self):
    #     return f'postgresql://52g-dev:test123@localhost:5432/template-flask'


# Flask Dev Configuration
class DevConfig(BaseConfig):
    BASE_URL = "https://template.52g.studio"

    # PostgreSQL
    # @property
    # def SQLALCHEMY_DATABASE_URI(self):
    #     db_host = SQLAlchemyConfig.instance().DB_HOST
    #     db_username = SQLAlchemyConfig.instance().DB_USERNAME
    #     db_password = SQLAlchemyConfig.instance().DB_PASSWORD
    #     return f'postgresql://{db_username}:{db_password}@{db_host}:5432/template-flask'


config_by_name = dict(local="config.LocalConfig", dev="config.DevConfig")
