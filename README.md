# GoWake



## Install

```bash
python3 -m venv ./env
source ./env/bin/activate
pip install -r requirements.txt
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```