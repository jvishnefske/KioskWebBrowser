.PHONY: test coverage lint clean install

PYTHON ?= python3

install:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install pytest pytest-cov flake8

test:
	$(PYTHON) -m pytest tests/ -v

coverage:
	$(PYTHON) -m pytest tests/ --cov=. --cov-report=html --cov-report=xml --cov-report=term-missing

lint:
	$(PYTHON) -m flake8 *.py --max-line-length=120 --ignore=E501,W503,E301,E265,E402,F401,F841,W291,W292 || true

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

all: lint test coverage
