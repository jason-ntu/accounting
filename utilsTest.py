from mock_db import MockDB
import utils

class TestUtils(MockDB):

    def test_db_write(self):
        with self.test_db:
            self.assertEqual(utils.create("""INSERT INTO `test_table` (`id`, `text`, `int`) VALUES
                            ('3', 'test_text_3', 3)"""), True)
            self.assertEqual(utils.create("""INSERT INTO `test_table` (`id`, `text`, `int`) VALUES
                            ('1', 'test_text_3', 3)"""), False)
            self.assertEqual(utils.create("""DELETE FROM `test_table` WHERE id='1' """), True)
            self.assertEqual(utils.create("""DELETE FROM `test_table` WHERE id='4' """), True)
