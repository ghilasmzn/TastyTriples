PYTHON = python3
MAIN_DIR = api
ARGS = $(filter-out $@,$(MAKECMDGOALS))

.PHONY: help practice1

# Set PYTHONPATH to include the project's root directory
export PYTHONPATH := $(PYTHONPATH):$(PWD)

# Install the dependencies
.PHONY: install
install:
	pip3 install -r requirements.txt

help:
	@echo "Available targets:"

# Clean up generated files
.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -exec rm -rf {} +
