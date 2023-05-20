import io
from unittest.mock import patch
from records import RecordPage, RecordOption
from mock_db import MockDB
from accessor import ExecutionStatus as es
import const

class TestPaymentPage(MockDB):

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_show(self, _stdout):
        RecordPage.show()
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(output_lines[0], "%d: 新增消費紀錄" % RecordOption.CREATE)
        self.assertEqual(output_lines[1], "%d: 檢視消費紀錄" % RecordOption.READ)
        self.assertEqual(output_lines[2], "%d: 修改消費紀錄" % RecordOption.UPDATE)
        self.assertEqual(output_lines[3], "%d: 刪除消費紀錄" % RecordOption.DELETE)
        self.assertEqual(output_lines[4], "%d: 回到上一頁" % RecordOption.BACK)
    
    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['0', '6', 'T', '1', '2', '3', '4', '5'])
    def test_choose(self, _input,  _stdout):
        self.assertEqual(RecordPage.choose(), RecordOption.CREATE)
        self.assertEqual(_input.call_count, 4)
        self.assertEqual(_stdout.getvalue(), "請輸入 1 到 5 之間的數字:\n"*3)
        self.assertEqual(RecordPage.choose(), RecordOption.READ)
        self.assertEqual(_input.call_count, 5)
        self.assertEqual(RecordPage.choose(), RecordOption.UPDATE)
        self.assertEqual(_input.call_count, 6)
        self.assertEqual(RecordPage.choose(), RecordOption.DELETE)
        self.assertEqual(_input.call_count, 7)
        self.assertEqual(RecordPage.choose(), RecordOption.BACK)
        self.assertEqual(_input.call_count, 8)
    
    @patch.object(RecordPage, 'execute')
    @patch.object(RecordPage, 'choose', side_effect=[RecordOption.CREATE, RecordOption.READ, RecordOption.UPDATE, RecordOption.DELETE, RecordOption.BACK])
    @patch.object(RecordPage, 'show')
    def test_start(self, _show, _choose, _execute):
        RecordPage.start()
        self.assertEqual(_show.call_count, 5)
        self.assertEqual(_choose.call_count, 5)
        self.assertEqual(_execute.call_count, 4)
    
    # @patch("sys.stdout", new_callable=io.StringIO)
    # @patch.object(RecordPage, 'delete', return_value=True)
    # @patch.object(RecordPage, 'update', return_value=False)
    # @patch.object(RecordPage, 'read')
    # @patch.object(RecordPage, 'create', return_value=True)
    # def test_execute(self, _create, _read, _update, _delete, _stdout):
    #     with self.mock_db_config:
    #         RecordPage.execute(RecordOption.CREATE)
    #         self.assertEqual(_create.call_count, 1)
    #         RecordPage.execute(RecordOption.READ)
    #         self.assertEqual(_read.call_count, 1)
    #         RecordPage.execute(RecordOption.UPDATE)
    #         self.assertEqual(_update.call_count, 1)
    #         RecordPage.execute(RecordOption.DELETE)
    #         self.assertEqual(_delete.call_count, 1)
    #     output_lines = _stdout.getvalue().strip().split('\n')
    #     self.assertEqual(output_lines[0], "%s操作成功%s" %
    #                      (const.ANSI_GREEN, const.ANSI_RESET))
    #     self.assertEqual(output_lines[1], "%s操作失敗%s" %
    #                      (const.ANSI_RED, const.ANSI_RESET))
    #     self.assertEqual(output_lines[2], "%s操作成功%s" %
    #                      (const.ANSI_GREEN, const.ANSI_RESET))
    
