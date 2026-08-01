.PHONY: test check-data verify-artifacts check experiment

MVP_DIR := prd/01-scenario-library-mvp
PYTHON := python3

test:
	cd $(MVP_DIR) && $(PYTHON) -m unittest discover -s tests -v

check-data:
	cd $(MVP_DIR) && $(PYTHON) scripts/build_dataset.py --check

verify-artifacts:
	cd $(MVP_DIR) && $(PYTHON) -m src.experiment --verify-only --data-dir data --artifact-dir artifacts

check: test check-data verify-artifacts

experiment:
	cd $(MVP_DIR) && $(PYTHON) -m src.experiment --data-dir data --artifact-dir artifacts --price-per-1k 0.0005
