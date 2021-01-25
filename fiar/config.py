from abc import ABC


class Config(ABC):
    SECRET_KEY = 'super secret key'

    APP_DB_DRIVER = 'postgresql'
    APP_DB_HOST = 'localhost'
    APP_DB_PORT = '5432'
    APP_DB_NAME = 'pia'
    APP_DB_USER = 'pia'
    APP_DB_PASSWORD = 'pia'

    # --- SQLAlchemy ---
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f'{self.APP_DB_DRIVER}://' \
               f'{self.APP_DB_USER}:{self.APP_DB_PASSWORD}' \
               f'@{self.APP_DB_HOST}:{self.APP_DB_PORT}' \
               f'/{self.APP_DB_NAME}'


class ProductionConfig(Config):
    ENV = 'production'


class DevelopmentConfig(Config):
    ENV = 'development'
