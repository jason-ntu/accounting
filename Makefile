TEST_FILE_NAME := budgetTest.py  deleteRecordTest.py fixedIETest.py locationTest.py \
				 accountTest.py readRecordTest.py reportTest.py settingTest.py recordsTest.py \
				 createRecordTest.py updateRecordTest.py categoryTest.py
#  exportTest.py fixedIErecordTest.py invoiceTest.py menuTest.py

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