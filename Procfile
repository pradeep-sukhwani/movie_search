web:python manage.py runserver
web: gunicorn movie.wsgi --log-file -
heroku ps:scale web=1
heroku config:set DISABLE_COLLECTSTATIC=0
