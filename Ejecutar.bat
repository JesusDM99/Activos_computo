@echo off

start /B cmd /c python manage.py runserver

start "" http://127.0.0.1:8000/