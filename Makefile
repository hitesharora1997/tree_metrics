# Variables
VENV_NAME = venv
PYTHON = $(VENV_NAME)/bin/python
PIP = $(VENV_NAME)/bin/pip
PYTEST = $(VENV_NAME)/bin/pytest

.PHONY: all setup install run test lint fix-lint clean docker help

# Default target
all: clean setup install lint test run

# Create virtual environment and install dependencies
setup:
	@echo "Setting up the virtual environment and installing dependencies."
	python3 -m venv $(VENV_NAME)
	$(PIP) install -r requirements.txt
	mkdir -p data outputs logs

# Install dependencies
install: $(VENV_NAME)
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt

# Run the application
DEFAULT_DATASET = data/example_dataset.las

run:
	@echo "Running the application..."
	PYTHONPATH=$(PWD) $(PYTHON) main.py $(if $(FILE),$(FILE),$(DEFAULT_DATASET)) $(OPTIONS)

# Run tests
test: install
	@echo "Running tests..."
	PYTHONPATH=$(PWD) $(PYTEST) tests

# Build Docker image
docker:
	@echo "Building Docker image..."
	docker build -t tree-metrics .

# Run with Docker
docker-run:
	@if [ -z "$(FILE)" ]; then \
		echo "Usage: make docker-run FILE=path/to/your/pointcloud.las [OPTIONS=\"--visualize --log-level DEBUG\"]"; \
		exit 1; \
	fi
	@echo "Running with Docker..."
	docker run -v $(PWD)/data:/app/data -v $(PWD)/outputs:/app/outputs tree-metrics $(FILE) $(OPTIONS)

# Clean up
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_NAME)
	find . -type f -name '.pyc' -delete
	find . -type d -name 'pycache' -exec rm -rf {} +
	find . -type d -name '.pytest_cache' -exec rm -rf {} +
	rm -rf logs/.log

# Display help information
help:
	@echo "Usage: make [TARGET]"
	@echo ""
	@echo "Targets:"
	@echo "  setup       - Create virtual environment and install dependencies"
	@echo "  install     - Install dependencies"
	@echo "  run         - Run the application (requires FILE=path/to/your/pointcloud.las)"
	@echo "  test        - Run tests"
	@echo "  docker      - Build Docker image"
	@echo "  docker-run  - Run application in Docker (requires FILE=path/to/your/pointcloud.las)"
	@echo "  clean       - Clean up"
	@echo "  help        - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make run FILE=data/example.las"
	@echo "  make run FILE=data/example.las OPTIONS="--visualize --log-level DEBUG""
	@echo "  make docker-run FILE=data/example.las"
	@echo "  make run FILE=data/example.las OPTIONS="--visualize-3d --color-by height""
