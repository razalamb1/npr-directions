install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
lint:
	pylint $(git ls-files '*.py')

test:
	python -m pytest -vv --cov tests
