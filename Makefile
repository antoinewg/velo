venv:
	python3 -m venv venv
	source ./venv/bin/activate

install:
	pip3 install -r requirements.txt

freeze:
	pip3 freeze > requirements.txt

lint:
	@echo "Running linter.."
	@black .

test:
	@python3 -m pytest

serve:
	@streamlit run src/app.py