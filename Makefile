TEST_FILE_NAME := settingTest.py budgetTest.py paymentTest.py fixedIETest.py menuTest.py reportTest.py incomeTest.py categoryTest.py
RUN_FILE_NAME := setting.py
CACHE := .coverage htmlcov coverage_html_report

.PHONY: all clean

run:
	@python3 $(RUN_FILE_NAME)

test:
	@python3 -m unittest $(TEST_FILE_NAME)

testElia:
	@python3 -m unittest viewRecordTest.py

coverage:
	@coverage run -m unittest $(TEST_FILE_NAME)
	@coverage report -m
	@coverage html

install:
	@pip3 install -r requirements.txt

requirements:
	@pip3 freeze > requirements.txt

database:
	@python3 database.py

record:
	@python3 records.py

clean:
	@$(RM) -r $(CACHE)
