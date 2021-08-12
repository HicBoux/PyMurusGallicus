VENV_NAME = venv
PYTHON = $(VENV_NAME)/bin/python3
PIP = $(VENV_NAME)/bin/pip3
PYTHON_VERSION = $(shell python3 --version 2>&1)
IS_PYTHON_VERSION_OK =  $((shell case "Python 3" in *PYTHON_VERSION* ) "TRUE";)

all: install test run

install:
ifdef IS_PYTHON_VERSION_OK
	python3 -m venv $(VENV_NAME)
	. $(VENV_NAME)/bin/activate; pip install -Ur requirements.txt
else
	$(error !!! ERROR : Are you sure that Python 3 is installed ? !!!)
endif

run: $(VENV_NAME)/bin/activate
	$(PYTHON) ./src/main.py

test:
	$(PYTHON) -m unittest discover 

clean:
	rm -rf __pycache__
	rm -rf $(VENV_NAME)
	find . -type f -name '*.pyc' -delete

.PHONY: all install run clean test