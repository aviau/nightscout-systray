venv:
	virtualenv -p python3 venv
	venv/bin/pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf venv

.PHONY: run
run: venv
	bash -c '\
	    venv/bin/python nightscout-systray.py \
	'
