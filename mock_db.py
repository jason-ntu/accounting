from unittest import TestCase
import mysql.connector
import sqlalchemy as db
from mock import patch
import utils
from dotenv import dotenv_values

env = dotenv_values(".env")

MYSQL_DIALECT = env["MYSQL_DIALECT"]
MYSQL_DRIVER = env["MYSQL_DRIVER"]
MYSQL_HOST = env["MYSQL_HOST"]
MYSQL_USER = env["MYSQL_USER"]
MYSQL_PASSWORD = env["MYSQL_PASSWORD"]
MYSQL_TEST_DB = env["MYSQL_TEST_DB"]
MYSQL_PORT = env["MYSQL_PORT"]

INITIAL_BUDGET = env["INITIAL_BUDGET"]

# class MockDB(TestCase):

#     @classmethod
#     def setUpClass(cls):
#         url = "%s+%s://%s:%s@%s:%s/%s" % (MYSQL_DIALECT, MYSQL_DRIVER, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_TEST_DB)
#         engine = db.create_engine(url)
#         connection = engine.connect()
#         metadata = db.MetaData()


class MockDB(TestCase):
    @classmethod
    def setUpClass(cls):
        cnx = mysql.connector.connect(
            host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, port=MYSQL_PORT
        )
        cursor = cnx.cursor(dictionary=True)

        # drop database if it already exists
        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_TEST_DB))
            cursor.close()
            print("DB dropped")
        except mysql.connector.Error as err:
            if err.errno != 1008:
                print(err)

        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(MYSQL_TEST_DB)
            )
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
        cnx.database = MYSQL_TEST_DB

        createsTables = [
            """CREATE TABLE `test_table` (
                  `id` varchar(10) NOT NULL PRIMARY KEY ,
                  `text` text NOT NULL,
                  `int` int NOT NULL
                )""",
            """CREATE TABLE `budget_table` (
                  `id` varchar(10) NOT NULL PRIMARY KEY ,
                  `amount` FLOAT NOT NULL
                )""",
            """CREATE TABLE `payment_table` (
                  `id` varchar(10) NOT NULL PRIMARY KEY ,
                  `name` varchar(40) NOT NULL,
                  `balance` FLOAT NOT NULL,
                  `category` ENUM('CASH', 'DEBIT_CARD', 'CREDIT_CARD', 'ELECTRONIC', 'OTHER') NOT NULL
                )""",
        ]

        for createsTable in createsTables:
            try:
                cursor.execute(createsTable)
                cnx.commit()
            except mysql.connector.Error as err:
                print(err)
                cnx.rollback()

        insertsTables = [
            """INSERT INTO `test_table` (`id`, `text`, `int`) VALUES
                            ('1', 'test_text', 1),
                            ('2', 'test_text_2',2)""",
            """INSERT INTO `budget_table` (`id`, `amount`) VALUES
                            ('1', '%f')"""
            % float(INITIAL_BUDGET),
            """INSERT INTO `budget_table` (`id`, `amount`) VALUES
                            ('1', '%f')"""
            % float(INITIAL_BUDGET),
        ]

        for insertsTable in insertsTables:
            try:
                cursor.execute(insertsTable)
                cnx.commit()
            except mysql.connector.Error as err:
                print(err)
                cnx.rollback()
        cursor.close()
        cnx.close()

        testconfig = {
            "host": MYSQL_HOST,
            "user": MYSQL_USER,
            "password": MYSQL_PASSWORD,
            "database": MYSQL_TEST_DB,
        }
        cls.mock_db_config = patch.dict(utils.config, testconfig)

    @classmethod
    def tearDownClass(cls):
        cnx = mysql.connector.connect(
            host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD
        )
        cursor = cnx.cursor(dictionary=True)

        # drop test database
        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_TEST_DB))
            cnx.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print(
                "Database {} does not exists. Dropping db failed".format(MYSQL_TEST_DB)
            )
            cnx.rollback()
        cnx.close()
