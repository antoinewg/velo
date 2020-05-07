venv:
	python3 -m venv venv
	source ./venv/bin/activate

install:
	pip3 install -r requirements.txt

freeze:
	pip3 freeze > requirements.txt

lint:
	black .

test:
	python3 -m pytest

serve:
	python manage.py runserver 127.0.0.1:8001