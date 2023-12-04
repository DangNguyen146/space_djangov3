Run env
source enviroment_3_9_5/bin/activate

Goi thu vien
pip install django-cors-headers
pip install djoser
pip install pillow
pip install stripe
pip install qrcode

Chay
python3 manage.py makemigrations
python3 manage.py makemigrations
python3 manage.py migrate --fake

python3 manage.py createsuperuser
<!-- admin -->
<!-- admin -->
python3 manage.py runserver

create project
django-admin startproject space_django
python3 manage.py startapp cards


# Cách chạy cho máy mới



sudo apt update
sudo apt install python3-pip
sudo apt install -y postgresql postgresql-contrib

#Truy cap vap postgres
sudo -i -u postgres
psql
CREATE USER user WITH PASSWORD 'pass';
CREATE DATABASE spacedbv3 OWNER dangnguyen;
dangnguyen


DROP DATABASE spacedbv3;
SELECT
	pg_terminate_backend (pg_stat_activity.pid)
FROM
	pg_stat_activity
WHERE
	pg_stat_activity.datname = 'spacedbv3';


\q
exit
sudo su - user

pip install django
pip install djangorestframework
pip install django-rest-knox
pip install markdown       # Markdown support for the browsable API.
pip install django-filter  # Filtering support
pip install django-cors-headers
pip install djoser
pip install psycopg2-binary

sudo apt install libpq-dev python3-dev
pip install Pillow
pip install stripe

pip freeze > requirements




Login Regieter
https://studygyaan.com/django/django-rest-framework-tutorial-register-login-logout
https://www.youtube.com/watch?v=Cw_jSc1NGdo

https://www.youtube.com/watch?v=DCRNavrlS8s&list=PLlVHoHHccp2_kuKovosZTK_Ftu6XwgFyH
https://medium.com/django-rest/django-rest-framework-change-password-and-update-profile-1db0c144c0a3






https://app.creately.com/diagram/4qBlCNBx4tj/edit





 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'spacedbv3',
        'USER': 'dangnguyen',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',




"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --disable-web-security --disable-gpu --user-data-dir=~/chromeTemp



docker run  -d --name postgresql -p "5432:5432"  -e POSTGRESQL_USERNAME=dangnk -e POSTGRESQL_PASSWORD=dangnk -e POSTGRESQL_DATABASE=spacedbv3 bitnami/postgresql:latest 

psql -U dangnk -d spacedbv3
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

Cài đặt STATIC_ROOT sẽ trỏ đến thư mục nơi Django thu thập các tệp tĩnh. Đảm bảo rằng nó được đặt chính xác thành đường dẫn chứa tệp tĩnh của bạn.

python manage.py createsuperuser
<!-- admin -->
<!-- admin -->
python3 manage.py runserver




https://stackoverflow.com/questions/30027203/create-django-super-user-in-a-docker-container-without-inputting-password
Docker auto create user supper admin
