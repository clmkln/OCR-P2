update:
	@echo "Updating virtual environment"
	python3 -m pip install virtualenv
	python3 -m venv env
	env/bin/python3 -m pip install -r requirements.txt