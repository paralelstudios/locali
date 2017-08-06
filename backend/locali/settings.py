# -*- coding: utf-8 -*-
"""
    locali.settings
    ~~~~~~~~~~~~~~~~
    Global backend package settings
"""

import os
from datetime import timedelta
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'local')
DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# DB and SQLAlchemy settings
DB_NAME = os.environ.get('POSTGRES_USER', 'locali')
DB_USER = os.environ.get('POSTGRES_USER', 'locali')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'locali')
DB_HOST = os.environ.get('POSTGRES_PORT_5432_TCP_ADDR', 'localhost')
DB_PORT = int(os.environ.get('POSTGRES_PORT_5432_TCP_PORT', 5432))
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_LOG_QUERIES = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

# API settings
SECRET_KEY = os.environ.get('LOCALI_API_SECRET_KEY', 'secret-key-so-secret')
BCRYPT_LOG_ROUNDS = 12
JWT_AUTH_USERNAME_KEY = "email"
JWT_EXPIRATION_DELTA = timedelta(1)
JWT_AUTH_URL_RULE = "/api/auth"

# AWS credentials
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')

# resource URIs
LOCALI_PHOTO_UPLOAD_BUCKET = os.environ.get('LOCALI_PHOTO_UPLOAD_BUCKET', 'locali-resources-local')
