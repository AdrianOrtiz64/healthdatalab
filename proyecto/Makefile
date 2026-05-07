# Makefile del proyecto-ejemplo Fase 2.
#
# Mismo stack que los labs (docker-compose + jupyter/scipy-notebook). Este
# Makefile es un complemento que orquesta el pipeline end-to-end. Mostrar
# que un proyecto real puede sumar herramientas al stack base del curso.
#
# Uso típico (Linux/Mac/WSL/Git Bash):
#   make setup      # construye e instala dependencias dentro del contenedor
#   make all        # pipeline completo: ingest -> curate -> tests -> render
#   make jupyter    # levanta Jupyter en http://localhost:8888
#
# En Windows nativo (PowerShell), correr los targets vía docker compose:
#   docker compose run --rm jupyter make all

PYTHON ?= python
COMPOSE := docker compose
RUN := $(COMPOSE) run --rm jupyter

.PHONY: setup ingest curate test render all jupyter clean

setup:
	$(COMPOSE) build
	$(RUN) pip install --quiet -r requirements.txt

ingest:
	$(RUN) $(PYTHON) -m src.ingest

curate: ingest
	$(RUN) $(PYTHON) -m src.curate

test:
	$(RUN) $(PYTHON) -m pytest tests/ -v

render: curate
	$(RUN) jupyter nbconvert \
		--to html \
		--execute notebooks/dashboard.ipynb \
		--output dashboard.html

all: setup curate test render
	@echo ""
	@echo "Pipeline completo. Abrir notebooks/dashboard.html"

jupyter:
	$(COMPOSE) up

clean:
	rm -f db/*.db
	rm -rf data/processed/
	rm -f notebooks/dashboard.html
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
