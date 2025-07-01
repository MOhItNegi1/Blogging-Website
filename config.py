import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:12345@localhost/blog_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'supersecretkey'
