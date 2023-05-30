import io
from unittest import TestCase
from unittest.mock import patch
from deleteRecord import DeleteRecordPage
from mock_db import MockDB
from accessor import ExecutionStatus as es
import const
from datetime import datetime
from readRecord import ReadRecordPage, ReadRecordOption
from records import RecordOption, RecordPage

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
    @patch.object(RecordPage, "updateAccountAmount")
    @patch.object(DeleteRecordPage, "checkIDInteger", return_value=1)
    def test_deleteByID(self, _checkIDInteger, _updateAccountAmount, _stdout):
        with self.mock_db_config:
            DeleteRecordPage.deleteByID()
            DeleteRecordPage.tearDown_connection(es.NONE)
        self.assertEqual(_checkIDInteger.call_count, 1)
        self.assertEqual(_updateAccountAmount.call_count, 1)
    
    @patch("sys.stdout", new_callable=io.StringIO)
    @patch.object(RecordPage, "updateAccountAmount")
    @patch.object(DeleteRecordPage, "checkIDInteger", return_value=10)
    def test_deleteByID2(self, _checkIDInteger, _updateAccountAmount, _stdout):
        with self.mock_db_config:
            DeleteRecordPage.deleteByID()
            DeleteRecordPage.tearDown_connection(es.NONE)
        self.assertEqual(_checkIDInteger.call_count, 1)
        self.assertEqual(_updateAccountAmount.call_count, 0)
    
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