PYTHON ?= python

.PHONY: test unit_test perf_test coverage lint doc

# Tous les tests (unitaires + performance)
test:
	$(PYTHON) -m pytest

# Tous les tests sauf ceux de performance
unit_test:
	$(PYTHON) -m pytest -m "not perf"

# Uniquement les tests de performance (-s pour afficher les mesures)
perf_test:
	$(PYTHON) -m pytest -m perf -s

# Rapport de couverture (sans les tests de performance).
# Le "-" permet de générer le rapport même si des tests échouent.
coverage:
	-$(PYTHON) -m coverage run -m pytest -m "not perf"
	$(PYTHON) -m coverage report -m
	$(PYTHON) -m coverage html

# Qualité de code
lint:
	$(PYTHON) -m ruff check

# Documentation HTML dans le dossier docs/
doc:
	$(PYTHON) -m pdoc --html --force --output-dir docs triangulator
