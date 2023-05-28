from unittest.mock import patch
from mock_db import MockDB
from freezegun import freeze_time
from fixedIE import FixedIEPage
from menu import MenuPage


class FixedIEIntegrationTest(MockDB):
    
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
    def test_same_day_as_register(self, _input):
        with self.mock_db_config:
            menu = MenuPage()
            menu.start()
            menu.start()