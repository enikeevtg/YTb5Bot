# UTILS
PY = python3
PIP = pip3

# FILENAMES
VENV = .venv
APP = app
MAIN_SCRIPT = $(APP)/bot.py
ANYWHERE_MAIN_SCRIPT = $(APP)/bot_pythonanywhere.py
REQUIREMENTS = requirements.txt
APP_PACK = app.tar


# MAIN TARGET
run:
	$(PY) $(MAIN_SCRIPT)

# DEPLOYMENT
pack:
	rm -rf $(APP_PACK)
	tar -cf $(APP_PACK) $(APP) $(REQUIREMENTS)

unpack: $(APP_PACK)
	tar -xvf $(APP_PACK)

install: venv unpack
	$(PIP) install -r $(REQUIREMENTS)
	rm $(APP_PACK)

# SERVICE
venv:
	$(PY) -m venv $(VENV)

freeze_deps:
	$(PIP) freeze > $(REQUIREMENTS)

install_deps: $(REQUIREMENTS)
	$(PIP) install -r $^

clean:
clean:
	rm -rf __pycache__
	rm -rf $(APP)/__pycache__
	rm -rf $(APP)/admin/__pycache__
	rm -rf $(APP)/db_handler/__pycache__
	rm -rf $(APP)/handlers/__pycache__
	rm -rf $(APP)/keyboards/__pycache__
	rm -rf $(APP)/utils/__pycache__
