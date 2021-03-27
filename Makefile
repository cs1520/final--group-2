.PHONY: start install clean

start: install
	. venv/bin/activate; GOOGLE_APPLICATION_CREDENTIALS=service-acct-keys.json FLASK_APP=main FLASK_ENV=development flask run

install: venv/touchfile

venv/touchfile: requirements.txt
	test -d venv || python3 -m venv venv
	. venv/bin/activate; pip3 install -Ur requirements.txt
	touch venv/touchfile

clean:
	rm -rf venv/ __pycache__/ lib/ include/
