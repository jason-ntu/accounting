TEST_FILE_NAME := IEAttributeTest.py budgetTest.py fixedIETest.py accountTest.py  reportTest.py\
				  settingTest.py menuTest.py exportTest.py fixedIErecordTest.py  \
				 createRecordTest.py readRecordTest.py recordsTest.py updateRecordTest.py deleteRecordTest.py invoiceTest.py


RUN_FILE_NAME := menu.py
CACHE := .coverage htmlcov coverage_html_report
TARGET := invoiceTest.TestInvoicePage

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

single-test:
	@python3 -m unittest $(TARGET)

clean:
	@$(RM) -r $(CACHE)