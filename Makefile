FILE_NAME := ./settings/settingsTest.py
CACHE := ./__pycache__ .coverage htmlcov coverage_html_report

.PHONY: all clean

all: test coverage

test:
	@coverage run -m unittest $(FILE_NAME)

coverage: .coverage
	@coverage report -m
	@coverage html

clean:
	@$(RM) -r $(CACHE)