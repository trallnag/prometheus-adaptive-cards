.PHONY: all
all: lint format_style format_imports test docs requirements

.PHONY: lint
lint:
	poetry run flake8 --config .flake8 --statistics

.PHONY: format
format: format_style format_imports

.PHONY: format_style
format_style:
	poetry run black .

.PHONY: format_imports
format_imports:
	poetry run isort --profile black .

# ==============================================================================

.PHONY: test
test:
	poetry run pytest --cov=./ --cov-report=xml

.PHONY: test_not_slow
test_not_slow:
	poetry run pytest -m "not slow"

.PHONY: test_slow
test_slow:
	poetry run pytest -m "slow"






.PHONY: docs
docs:
	rm -rf docs/*; \
	mkdir -p docs; \
	poetry run pdoc --output-dir /tmp/docs --html prometheus_webhook_proxy; \
	mv /tmp/docs/prometheus_adaptive_cards/* docs/; 

.PHONY: requirements
requirements:
	poetry export --format "requirements.txt" --output "requirements.txt" --without-hashes
