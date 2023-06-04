from unittest.mock import patch
from mock_db import MockDB
from freezegun import freeze_time
from menu import MenuPage


class FixedIEE2ETest(MockDB):
    
    @freeze_time("2023-05-27")
    @patch('builtins.input', side_effect=[
        # 基本設定
        4,
        # 查看/新增/修改/刪除每月固定收支
        2,
        # 新增三筆固定收支
        1, 2, "每月4號固定支出", 1, 1, 100, 1, 4, "",
        1, 2, "每月27號固定支出", 4, 2, 15000, 10, 27, "房租",
        1, 1, "每月31號固定收入", 3, 3, 2000, 6, 31, "ETH",
        # 查看固定收支
        2,
        # 回到上一頁
        5,
        # 回到上一頁
        6,
        # 消費紀錄
        1,
        # 檢視消費紀錄
        2, 
        # 查看本月紀錄
        3,
        # 回到上一頁
        5,
        # 回到上一頁
        5,
        # 關閉程式
        6
        ])
    def test_01(self, _input):
        print("create fixedIE on 5/27")
        with self.mock_db_config:
            menu = MenuPage()
            menu.start()
    
    @freeze_time("2023-05-27")
    @patch('builtins.input', side_effect=[        
        # 消費紀錄
        1, 
        # 檢視消費紀錄
        2,
        # 查看指定時間紀錄
        4,
        # 起始日
        "2023-01-01",
        # 終止日
        "2023-12-31",
        # 回到上一頁
        5,
        # 回到上一頁
        5,
        # 關閉程式
        6
        ])
    def test_02(self, _input):
        print("open the app on 5/27")
        with self.mock_db_config:
            menu = MenuPage()
            menu.start()

    @freeze_time("2023-06-03")
    @patch('builtins.input', side_effect=[        
        # 消費紀錄
        1, 
        # 檢視消費紀錄
        2,
        # 查看指定時間紀錄
        4,
        # 起始日
        "2023-01-01",
        # 終止日
        "2023-12-31",
        # 回到上一頁
        5,
        # 回到上一頁
        5,
        # 關閉程式
        6
        ])
    def test_03(self, _input):
        print("open the app on 6/3")
        with self.mock_db_config:
            menu = MenuPage()
            menu.start()

    @freeze_time("2023-07-30")
    @patch('builtins.input', side_effect=[        
        # 消費紀錄
        1, 
        # 檢視消費紀錄
        2,
        # 查看指定時間紀錄
        4,
        # 起始日
        "2023-01-01",
        # 終止日
        "2023-12-31",
        # 回到上一頁
        5,
        # 回到上一頁
        5,
        # 關閉程式
        6
        ])
    def test_04(self, _input):
        print("open the app on 7/30")
        with self.mock_db_config:
            menu = MenuPage()
            menu.start()

    @freeze_time("2023-09-30")
    @patch('builtins.input', side_effect=[        
        # 消費紀錄
        1, 
        # 檢視消費紀錄
        2,
        # 查看指定時間紀錄
        4,
        # 起始日
        "2023-01-01",
        # 終止日
        "2023-12-31",
        # 回到上一頁
        5,
        # 回到上一頁
        5,
        # 關閉程式
        6
        ])
    def test_05(self, _input):
        print("open the app on 9/30")
        with self.mock_db_config:
            menu = MenuPage()
            menu.start()