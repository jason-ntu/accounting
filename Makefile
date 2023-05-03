FILE_NAME := settingsTest.py
CACHE := ./__pycache__ .coverage htmlcov coverage_html_report

.PHONY: clean

test:
	@coverage run -m unittest $(FILE_NAME)

coverage: .coverage
	@coverage report -m
	@coverage html

clean:
	@$(RM) -r $(CACHE)