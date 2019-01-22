# coding=utf-8

import logging
import os

SRC_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

SECRET_KEY = '47e585de7f22984d5ee291c2f31412384bfc32d0'
FLASH_MESSAGES = True

DATABASE = "sqlite"
# DATABASE = "postgresql"
DATABASE_NAME = "wimm"
#DATABASE_AUTH = {"user":'wimmapp', "password":'wimmapppassword123456'}
DATABASE_PATH = "./app.db"

# Application in-dev. settings
TESTING = False
DEBUG = True

LOGIN_DISABLED = True

# Set secret keys for CSRF protection
CSRF_SESSION_KEY = '8a7474974efcf76896aa84eea9cbe016bbc08828'
CSRF_ENABLED = True
