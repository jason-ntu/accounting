FILES_NAME := settings/*.py
CACHE := .coverage htmlcov coverage_html_report

.PHONY: all clean

all: test coverage

test:
	@coverage run -m unittest $(FILES_NAME)

coverage: .coverage
	@coverage report -m
	@coverage html

clean:
	@$(RM) -r $(CACHE)
