NAME = mazegen
VERSION = 1.0.0
VENV = venv
BIN = $(VENV)/bin
PYTHON = $(BIN)/python3
PIP = $(BIN)/pip
MAIN = a_maze_ing.py
WHL = $(NAME)-$(VERSION)-py3-none-any.whl

all: install

install: $(VENV)

$(VENV): requirements.txt pyproject.toml
	@python3 -c "import sys; exit(1) if sys.version_info < (3, 10) else exit(0)" || \
	(echo "Error: Python 3.10 or higher is required for A-Maze-ing."; exit 1)
	@python3 -m venv $(VENV)
	@$(PIP) install --upgrade pip
	@$(PIP) install build
	@$(PIP) install -e .
	@$(PYTHON) -m build
	@cp dist/$(WHL) .
	@touch $(VENV)

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
	@rm -f $(NAME)-$(VERSION)-py3-none-any.whl
	@rm -f $(NAME)-$(VERSION).tar.gz

re: fclean all

lint:
	@$(BIN)/flake8 a_maze_ing.py src/
	@$(BIN)/mypy a_maze_ing.py src/ --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	@$(BIN)/flake8 a_maze_ing.py src/
	@$(BIN)/mypy a_maze_ing.py src/ --strict

.PHONY: all install run debug clean fclean re lint lint-strict