Hello it's Beta version of Django and face-recognition. This program works on two cameras that are at the entrance and exit to the building, to register the faces of employees.
it belongs to work only in the operating system Linux Debian (Ubuntu).
It's installation guide of it:

1. clone project
2. add interpreter (python>=3.8)
3. activate venv
4. pip install -r requirements.txt
5. create "Face_django" database in MySQL
6. Add migrations:
   1. python manage.py makemigrations
   2. python manage.py migrate
7. Create superuser for login system:
   1. python manage.py createsuperuser
8. Collect the static files:
   1. python manage.py collectstatic
9. open access to root without a password, for this you need
   1. sudo visudo
   2. ![](../../Изображения/readme 1.png)
10. Write a systemd service for turning on cameras, for permanent work:
    1. sudo vim /etc/systemd/system/camera.service
    2. ![](../../Изображения/readme 2.png)
11. Enable bash scripts in "face_recognizer" directory:
    1. sudo chmod +x start.sh
    2. sudo chmod +x stop.sh
12. Start the server:
    1. python manage.py runserver
