@echo on
cd /
cd venvs/handybus/scripts
call activate.bat
cd /
cd github/handybus/mvp
python manage.py runserver
pause