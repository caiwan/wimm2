# coding=utf-8

import os

SRC_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Generate it with manage.py gensalt. You should get something like this:
SECRET_KEY = b'$2b$12$4KQgT9MsGuHCQ2i3aA05Cu'
FLASH_MESSAGES = True

# DB Connection
# Sqlite
DATABASE = "sqlite"
DATABASE_NAME = "cai-notes"
DATABASE_PATH = "./app.db"

# -- OR --
# Postgresql
# DATABASE = "postgresql"
# DATABASE_NAME = "wimmapp"
# DATABASE_AUTH = {
#     "user": "wimuser",
#     "password": "wimmpassword",
#     "host": "127.0.0.1",
#     "port": 5432
# }

# -- OR --
# for testing
# DATABASE = "sqlite"
# DATABASE_NAME = "cai-notes"
# DATABASE_PATH = ":memory"

# Application in-dev. settings
TESTING = False
DEBUG = True

# LOGIN_DISABLED = True

# Set secret keys for CSRF protection
CSRF_SESSION_KEY = "qWmODTwKC95EpJHp5zmW7Ui9DkraYLUa"
CSRF_ENABLED = True

