from os import environ
from dotenv import load_dotenv, find_dotenv

class Config:
    if find_dotenv() == '':
        # could not find a dotenv file, use development defaults
        # NOTE: These are dev defaults, these creds/keys are not used in prod
        
        # General
        SECRET_KEY = b'C\xd3\x90\x98qe\xd6\x03E\xf1\x9c,\xe1\xa6\xb1\xf4'
        FLASK_ENV = 'development'
        # Database
        SQLALCHEMY_DATABASE_URI = 'postgresql://allotech:allotech@localhost/teambuilder'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    else:
        load_dotenv()
        SECRET_KEY = environ.get("SECRET_KEY")
        # Database
        SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
        SQLALCHEMY_TRACK_MODIFICATIONS = False
