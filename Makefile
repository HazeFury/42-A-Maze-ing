NAME = mazegen
VERSION = 1.0.0
VENV = venv
BIN = $(VENV)/bin
PYTHON = $(BIN)/python3
PIP = $(BIN)/pip
MAIN = a_maze_ing.py
WHL = $(NAME)-$(VERSION)-py3-none-any.whl
TAR = $(NAME)-$(VERSION).tar.gz

SRC_DIR = src/
APP_DIR = app/

all: install

install: $(VENV)
	@$(PIP) install --upgrade pip
	@$(PIP) install -e ".[dev]"

$(VENV):
	@python3 -c "import sys; exit(1) if sys.version_info < (3, 10) else exit(0)" || \
	(echo "Error: Python 3.10 or higher is required."; exit 1)
	@python3 -m venv $(VENV)

build: install
	@$(PIP) install build
	@$(PYTHON) -m build
	@cp dist/$(WHL) .

run:
	@$(PYTHON) $(MAIN) config.txt

debug:
	@$(PYTHON) -m pdb $(MAIN) config.txt

clean:
	@echo "Remove temporary files or caches"
	@rm -rf .mypy_cache .pytest_cache build/ dist/ src/$(NAME).egg-info
	@find . -type d -name "__pycache__" -exec rm -rf {} +

fclean: clean
	@echo "Remove virtual environment and distribution files"
	@rm -rf $(VENV)
	@rm -f $(WHL)
	@rm -f $(TAR)

re: fclean all

lint:
	@$(PYTHON) -m flake8 $(MAIN) $(SRC_DIR) $(APP_DIR)
	@$(PYTHON) -m mypy $(MAIN) $(SRC_DIR) $(APP_DIR) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	@$(PYTHON) -m flake8 $(MAIN) $(SRC_DIR) $(APP_DIR)
	@$(PYTHON) -m mypy $(MAIN) $(SRC_DIR) $(APP_DIR) --strict

test:
	@echo "Lancement de toute la suite de tests..."
	@$(PYTHON) -m pytest tests/ -v

test-file:
	@if [ -z "$(FILE)" ]; then \
		echo "Erreur: Tu dois spécifier un fichier."; \
		echo "Usage: make test-file FILE=tests/test_ton_fichier.py"; \
	else \
		echo "Lancement des tests pour $(FILE)..."; \
		$(PYTHON) -m pytest $(FILE) -v; \
	fi


.PHONY: all install run build debug clean fclean re lint lint-strict test test-file