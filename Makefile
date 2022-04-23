install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
lint:
	pylint --disable=R,C src/gmaps.py

test:
	python -m pytest -vv --cov tests
