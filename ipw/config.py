from os import environ

class Config:
    # General
    SECRET_KEY = '\xb7)\xa8\x9d\xd3\xa1\xeaG[+\xe3\xfa\xe0\xb2\xe2j'
    # Database
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://allotech:allotech@localhost/ipw'
    SQLALCHEMY_TRACK_MODIFICATIONS = False