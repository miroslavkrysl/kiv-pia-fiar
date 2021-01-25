from abc import ABC


class Config(ABC):
    SECRET_KEY = 'super secret key'
    DB_DRIVER = 'postgresql'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_NAME = 'pia'
    DB_USER = 'pia'
    DB_PASSWORD = 'pia'

    @property
    def DB_URI(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


class ProductionConfig(Config):
    ENV = 'production'


class DevelopmentConfig(Config):
    ENV = 'development'
