TEST_FILE_NAME := utilsTest.py settingTest.py budgetTest.py paymentTest.py
RUN_FILE_NAME := setting.py
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

requirements:
	@pip3 freeze > requirements.txt

clean:
	@$(RM) -r $(CACHE)
