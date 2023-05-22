import io
from unittest import TestCase
from unittest.mock import patch
from deleteRecord import DeleteRecordPage
from mock_db import MockDB
from accessor import ExecutionStatus as es
import const
from datetime import datetime
from readRecord import ReadRecordPage, ReadRecordOption


class TestDeleteRecord(MockDB):
    
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_hints(self, _stdout):
        hints = [(DeleteRecordPage.hintGetID, "請輸入想刪除的紀錄ID:\n")]
        for hint in hints:
            hint[0]()
            self.assertMultiLineEqual(_stdout.getvalue(), hint[1])
            _stdout.truncate(0)
            _stdout.seek(0)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["2.5", "F", "1", "2"])
    def test_checkIDInteger(self, _input, _stdout):
        self.assertEqual(DeleteRecordPage.checkIDInteger(), 1)
        self.assertEqual(_input.call_count, 3)
        self.assertEqual(DeleteRecordPage.checkIDInteger(), 2)
        self.assertEqual(_input.call_count, 4)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 6)
        self.assertEqual(output_lines[0], "請輸入想刪除的紀錄ID:")
        self.assertEqual(output_lines[1],"輸入的ID須為整數")
        self.assertEqual(output_lines[2], "請輸入想刪除的紀錄ID:")
        self.assertEqual(output_lines[3],"輸入的ID須為整數")
        self.assertEqual(output_lines[4], "請輸入想刪除的紀錄ID:")
        self.assertEqual(output_lines[5], "請輸入想刪除的紀錄ID:")

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(DeleteRecordPage, "checkIDInteger", side_effect=[1, 10])
    def test_deleteByID(self, _checkIDInteger, _stdout):
        with self.mock_db_config:
            DeleteRecordPage.setUp_connection_and_table()
            DeleteRecordPage.deleteByID()
            DeleteRecordPage.deleteByID()
            DeleteRecordPage.tearDown_connection(es.NONE)
        self.assertEqual(_checkIDInteger.call_count, 2)
        output_lines = _stdout.getvalue().strip().split('\n')
        self.assertEqual(len(output_lines), 3)
        self.assertEqual(output_lines[0], "%s操作成功%s" % (const.ANSI_GREEN, const.ANSI_RESET))
        self.assertEqual(output_lines[1], "此紀錄ID不存在")
        self.assertEqual(output_lines[2], "%s操作失敗%s" % (const.ANSI_RED, const.ANSI_RESET))
    
    @patch.object(DeleteRecordPage, "deleteByID")
    @patch.object(ReadRecordPage, "execute")
    @patch.object(ReadRecordPage, "choose",
        side_effect=[ReadRecordOption.TODAY, ReadRecordOption.WEEK, ReadRecordOption.MONTH, ReadRecordOption.OTHER, ReadRecordOption.BACK],
    )
    @patch.object(ReadRecordPage, "show")
    def test_start(self, _show, _choose, _execute, _deleteByID):
        DeleteRecordPage.start()
        self.assertEqual(_show.call_count, 5)
        self.assertEqual(_choose.call_count, 5)
        self.assertEqual(_execute.call_count, 4)
        self.assertEqual(_deleteByID.call_count, 4)