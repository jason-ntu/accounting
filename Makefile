# TEST_FILE_NAME := settingsTest.py budgetTest.py
TEST_FILE_NAME := database/utilsTest.py
RUN_FILE_NAME := settings.py
CACHE := .coverage htmlcov coverage_html_report

.PHONY: all clean

run:
	@python3 $(RUN_FILE_NAME)

test:
	@python3 -m unittest $(TEST_FILE_NAME)

coverage: 
	@coverage run -m unittest $(TEST_FILE_NAME)
	@coverage report -m
	@coverage html

clean:
	@$(RM) -r $(CACHE)
