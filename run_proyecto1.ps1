@echo off
call .venv\Scripts\activate.bat
set FLASK_APP=.venv/proyecto1/app.py
flask run --port=5000
pause
.venv/proyecto1/app.py
.venv/proyecto1/templates/base.html