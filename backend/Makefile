PYTHON = python3
ARGS = $(filter-out $@,$(MAKECMDGOALS))

.PHONY: help practice1

# Set PYTHONPATH to include the project's root directory
export PYTHONPATH := $(PYTHONPATH):$(PWD)

help:
	@echo "Usage:"
	@echo "  make help - Display this help message"
	@echo "  make install - Install requirements"
	@echo "  make collect - Collect data from the web and store it in the triplestore"
	@echo "  make query - Make queries to the triplestore and display the results"


install:
	$(PYTHON) -m pip install -r requirements.txt

clean:
	rm -rf data_retrevial/__pycache__ 

collect:
	$(PYTHON) data_retrieval/collect.py $(ARGS)

query:
	$(PYTHON) data_retrieval/query.py $(ARGS)
