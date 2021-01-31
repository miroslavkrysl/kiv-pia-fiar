SECRET_KEY = 'super secret key'

# --- Database ---

DB_PROVIDER = 'mysql+pymysql'
DB_HOST = 'localhost'
DB_USER = 'pia'
DB_PORT = 3306
DB_PASSWORD = 'pia'
DB_NAME = 'pia'

DB_URI = f'{DB_PROVIDER}://' \
         f'{DB_USER}:{DB_PASSWORD}' \
         f'@{DB_HOST}:{str(DB_PORT)}' \
         f'/{DB_NAME}'

# --- Security ---

# must be at least 32
APP_UID_LENGTH = 64

# --- Game ---

APP_GAME_BOARD_MAX_SIZE = 4096
APP_GAME_BOARD_DEFAULT_SIZE = 15
