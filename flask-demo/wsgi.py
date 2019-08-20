# usage
# pip install gunicorn
# gunicorn --bind 0.0.0.0:8080 wsgi:app

from app import app

if __name__ == "__main__":
    app.run()