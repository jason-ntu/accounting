import calendar
import sqlalchemy as sql
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from datetime import datetime
from accessor import Accessor, ExecutionStatus as es
from sqlalchemy import and_
from enum import IntEnum, auto
from tabulate import tabulate
from selenium.webdriver.chrome.options import Options

class InvoiceOption(IntEnum):
    BACK = auto()

class InvoiceText():
    BACK = ('%d: 回到上一頁' % InvoiceOption.BACK)
    TITLE = '========== 記帳簿［自動對獎］ =========='
    SUBTITLE = '［首頁］'
    QUESTION = '請選擇功能：'
    HINT = '輸入錯誤，請重新輸入！'
    NODATA = '本期兌獎資訊抓取失敗！'
    NOPAIR = '本期未中獎！'

class InvoicePage(Accessor):
    table_name = "Record"
    dicLatest = {}
    
    # 進入點
    def start(self):
        self.queryLatest()
        
        if self.dicLatest:
            self.goPair()
        else:
            print(InvoiceText.NODATA + "\n")

        self.show()
        self.choose()
        return

    #呈現選擇畫面
    def show(self):
        print(InvoiceText.TITLE)
        print(InvoiceText.BACK)
        print(InvoiceText.TITLE + "\n")

    #取得使用者選擇值
    def choose(self):
            while True:
                try:
                    option = InvoiceOption(int(input(InvoiceText.QUESTION)))
                    break
                except ValueError:
                    print(InvoiceText.HINT + "\n")
            return option

    # 上網抓發票資訊
    def queryLatest(self):
        aryAward3 = []
        browser = None

        # try:            
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        # print("stop0")
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # print("stop1")
        # print("self.dicLatest:", self.dicLatest)
        # print("browser: ", browser)

        url = 'https://invoice.etax.nat.gov.tw/'
        browser.get(url)

        #月份
        xpathPeriod = "//li[1]/a[@class='etw-on']"
        WebDriverWait(browser, 60).until(expected_conditions.presence_of_element_located((By.XPATH, xpathPeriod)))
        strPeriod = browser.find_element("xpath", xpathPeriod)
        self.dicLatest["period"] = strPeriod.text

        #特別獎
        xpathAward1 = "//div[@class='etw-web']/table[@class='etw-table-bgbox etw-tbig']/tbody/tr[1]/td[2]/p[@class='etw-tbiggest']/span[@class='font-weight-bold etw-color-red']"
        WebDriverWait(browser, 60).until(expected_conditions.presence_of_element_located((By.XPATH, xpathAward1)))
        strNumber1 = browser.find_element("xpath", xpathAward1)
        self.dicLatest["award1"] = strNumber1.text

        #特獎
        xpathAward2 = "//div[@class='etw-web']/table[@class='etw-table-bgbox etw-tbig']/tbody/tr[2]/td[2]/p[@class='etw-tbiggest']/span[@class='font-weight-bold etw-color-red']"
        WebDriverWait(browser, 60).until(expected_conditions.presence_of_element_located((By.XPATH, xpathAward2)))
        strNumber2 = browser.find_element("xpath", xpathAward2)
        self.dicLatest["award2"] = strNumber2.text

        #頭獎
        xpathAward3_1 = "/html/body/div[@class='etw-page']/div[@class='etw-wrapper']/div[@id='etw-container']/div[@class='container-xl']/div[@class='container-fluid etw-bgbox mb-4']/div[@class='etw-web']/table[@class='etw-table-bgbox etw-tbig']/tbody/tr[3]/td[2]/p[@class='etw-tbiggest mb-md-4'][1]"
        WebDriverWait(browser, 60).until(expected_conditions.presence_of_element_located((By.XPATH, xpathAward3_1)))
        strNumber3_1 = browser.find_element("xpath", xpathAward3_1)
        aryAward3.append(strNumber3_1.text.strip())

        xpathAward3_2 = "/html/body/div[@class='etw-page']/div[@class='etw-wrapper']/div[@id='etw-container']/div[@class='container-xl']/div[@class='container-fluid etw-bgbox mb-4']/div[@class='etw-web']/table[@class='etw-table-bgbox etw-tbig']/tbody/tr[3]/td[2]/p[@class='etw-tbiggest mb-md-4'][2]"
        WebDriverWait(browser, 60).until(expected_conditions.presence_of_element_located((By.XPATH, xpathAward3_2)))
        strNumber3_2 = browser.find_element("xpath", xpathAward3_2)
        aryAward3.append(strNumber3_2.text.strip())

        xpathAward3_3 = "/html/body/div[@class='etw-page']/div[@class='etw-wrapper']/div[@id='etw-container']/div[@class='container-xl']/div[@class='container-fluid etw-bgbox mb-4']/div[@class='etw-web']/table[@class='etw-table-bgbox etw-tbig']/tbody/tr[3]/td[2]/p[@class='etw-tbiggest mb-md-4'][3]"
        WebDriverWait(browser, 60).until(expected_conditions.presence_of_element_located((By.XPATH, xpathAward3_3)))
        strNumber3_3 = browser.find_element("xpath", xpathAward3_3)
        aryAward3.append(strNumber3_3.text.strip())

        self.dicLatest["award3"] = aryAward3
        browser.quit()
        
        # except:
        #     print(InvoiceText.NODATA)
        
        # finally:
        #     if browser is not None:
                # browser.quit()

    # 取得符合期別之紀錄
    def queryRecord(self, dateS, dateE):
        self.setUp_connection_and_table()
        query = sql.select(self.table).where(and_(self.table.c.purchaseDate >= dateS, self.table.c.purchaseDate <= dateE))
        results = self.conn.execute(query).fetchall()
        self.tearDown_connection(es.NONE)
        return results
    
    # 兌獎
    def goPair(self):
        period = self.dicLatest["period"]
        year = int(period[0:3]) + 1911
        month1 = int(period[4:6])
        month2 = int(period[7:9])
        dateSart = datetime(year, month1, 1)
        dateEnd = datetime(year, month2, calendar.monthrange(year, month2)[1])        

        records = self.queryRecord(dateSart, dateEnd)        
        if records:
            headerE = ["id", "IE", "category", "account", "amount", "location", "purchaseDate", "debitDate", "invoice", "note"]
            headerC = ["id", "收/支", "類別", "金額", "帳戶", "地點", "消費時間", "扣款時間", "發票號碼", "備註"]
            df = pd.DataFrame.from_records(records, columns = headerE)
            df["result"] = ''
            headerE.append("result")
            headerC.append("兌獎結果")
            df2 = pd.DataFrame(columns = headerE)

            for index, row in df.iterrows():
                ret = self.checkNumbers(row["invoice"])
                if ret != '':
                    row["result"] =  ret
                    df2.loc[len(df2)] = row

            if len(df2) > 0:
                print("\n" + self.dicLatest["period"])
                print(tabulate(df2, headers = headerC, tablefmt = 'pretty', showindex = False, stralign = 'left'))
                print("\n")
            else:
                print(InvoiceText.NOPAIR + "\n")
        else:
            print(InvoiceText.NOPAIR + "\n")

    # 兌獎邏輯
    def checkNumbers(self, myInvoice):
        ret = ''
        if myInvoice == self.dicLatest["award1"]: ret = '對中 1000 萬元！'   # 對中特別獎
        if myInvoice == self.dicLatest["award2"]: ret = '對中 200 萬元！'    # 對中特獎
        
        # 頭獎判斷
        for i in self.dicLatest["award3"]:
            if myInvoice == i:
                ret = '對中 20 萬元！'   # 對中頭獎
                break
            elif myInvoice[-7:] == i[-7:]:
                ret = '對中 4 萬元！'    # 末七碼相同
                break
            elif myInvoice[-6:] == i[-6:]:
                ret = '對中 1 萬元！'    # 末六碼相同
                break
            elif myInvoice[-5:] == i[-5:]:
                ret = '對中 4000 元！'   # 末五碼相同
                break
            elif myInvoice[-4:] == i[-4:]:
                ret = '對中 1000 元！'   # 末四碼相同
                break
            elif myInvoice[-3:] == i[-3:]:
                ret = '對中 200 元！'    # 末三碼相同
                break
        
        return ret
