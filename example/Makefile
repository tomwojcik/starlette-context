.PHONY: init up
SHELL := /bin/bash
.DEFAULT_GOAL := up

init:
	if [ -d "venv" ]; then rm -r venv; fi
	python3 -m venv venv
	source ./venv/bin/activate; \
	python -m pip install -U pip; \
	python -m pip install -r requirements.txt -e ..

up:
	if [ ! -d "venv" ]; then $(MAKE) init; fi
	uvicorn app:app --reload --port 5000
