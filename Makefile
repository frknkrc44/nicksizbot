VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python

all: venv installRequirements run
run:
	[ $(shell $(PYTHON) -c 'from sys import version_info as ver;print(ver.major)') -eq 3 ] && $(PYTHON) main.py && exit 0
	echo "You must use Python 3 for this bot"
	exit 1
installRequirements:
	$(PYTHON) -m pip install -r requirements.txt
venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -e .
	touch $(VENV_NAME)/bin/activate