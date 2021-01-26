SECRET_KEY = 'super secret key'

APP_DB_DRIVER = 'mysql+pymysql'
APP_DB_HOST = 'localhost'
APP_DB_PORT = '3306'
APP_DB_NAME = 'pia'
APP_DB_USER = 'pia'
APP_DB_PASSWORD = 'pia'

APP_DB_URI = f'{APP_DB_DRIVER}://' \
           f'{APP_DB_USER}:{APP_DB_PASSWORD}' \
           f'@{APP_DB_HOST}:{APP_DB_PORT}' \
           f'/{APP_DB_NAME}'

# --- Mail ---

# MAIL_SERVER : default ‘localhost’
# MAIL_PORT : default 25
# MAIL_USE_TLS : default False
# MAIL_USE_SSL : default False
# MAIL_DEBUG : default app.debug
# MAIL_USERNAME : default None
# MAIL_PASSWORD : default None
# MAIL_DEFAULT_SENDER : default None
# MAIL_MAX_EMAILS : default None
# MAIL_SUPPRESS_SEND : default app.testing
# MAIL_ASCII_ATTACHMENTS : default False
