import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class InvoicePage:
    #進入點
    def start(self):
        while True:
            self.queryLatest()

    def queryLatest(self):
        pass

    def pair(self):
        pass
    


if __name__ == '__main__': # pragma: no cover
    invoicePage = InvoicePage()
    invoicePage.start()