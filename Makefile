
UNIT_TEST := accountTest.py budgetTest.py createRecordTest.py deleteRecordTest.py exportTest.py \
				fixedIETest.py fixedIErecordTest.py IEAttributeTest.py invoiceTest.py menuTest.py \
				readRecordTest.py recordsTest.py reportTest.py settingTest.py updateRecordTest.py
E2E_TEST := FixedIEE2ETest.py
ALL_TEST := $(UNIT_TEST) $(E2E_TEST)
MENU := menu.py
CACHE := .coverage htmlcov coverage_html_report

.PHONY: all clean

meun:
	@python3 $(MENU)

test:
	@python3 -m unittest $(UNIT_TEST)

e2e-test:
	@python3 -m unittest $(E2E_TEST)

coverage:
	@coverage run -m unittest $(ALL_TEST)
	@coverage report -m
	@coverage html

install:
	@pip3 install -r requirements.txt

database:
	@python3 database.py

clean:
	@$(RM) -r $(CACHE)

run:
	@python3 -m unittest invoiceTest.TestInvoicePage