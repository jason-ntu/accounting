from unittest import TestCase
import mysql.connector
from mysql.connector import errorcode
from mock import patch
import utils
from dotenv import dotenv_values
import time

env = dotenv_values(".env")

MYSQL_USER = env['MYSQL_USER']
MYSQL_PASSWORD = env['MYSQL_PASSWORD']
MYSQL_DB = env['MYSQL_DB']
MYSQL_HOST = env['MYSQL_HOST']
MYSQL_PORT = env['MYSQL_PORT']
INITIAL_BUDGET = env['INITIAL_BUDGET']

class MockDB(TestCase):

    @classmethod
    def setUpClass(cls):
        cnx = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port = MYSQL_PORT
        )
        cursor = cnx.cursor(dictionary=True)

        # drop database if it already exists
        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
            cursor.close()
            print("DB dropped")
        except mysql.connector.Error as err:
            print("{}{}".format(MYSQL_DB, err))

        cursor = cnx.cursor(dictionary=True)
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(MYSQL_DB))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
        cnx.database = MYSQL_DB
        
        createTestTable = """CREATE TABLE `test_table` (
                  `id` varchar(30) NOT NULL PRIMARY KEY ,
                  `text` text NOT NULL,
                  `int` int NOT NULL
                )"""
        
        createBudgetTable = """CREATE TABLE `budget_table` (
                  `id` varchar(30) NOT NULL PRIMARY KEY ,
                  `int` int NOT NULL
                )"""
        
        createsTables = [createTestTable, createBudgetTable]
        for createsTable in createsTables:
            try:
                cursor.execute(createsTable)
                cnx.commit()
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("The table already exists.")
                else:
                    print(err.msg)

        insertTestTable = """INSERT INTO `test_table` (`id`, `text`, `int`) VALUES
                            ('1', 'test_text', 1),
                            ('2', 'test_text_2',2)"""
        insertBudgetTable = """INSERT INTO `budget_table` (`id`, `int`) VALUES
                            ('1', %s)""" % INITIAL_BUDGET
        insertsTables = [insertTestTable, insertBudgetTable]
        for insertsTable in insertsTables:
            try:
                cursor.execute(insertsTable)
                cnx.commit()
            except mysql.connector.Error as err:
                print(err)
        cursor.close()
        cnx.close()

        testconfig ={
            'host': MYSQL_HOST,
            'user': MYSQL_USER,
            'password': MYSQL_PASSWORD,
            'database': MYSQL_DB
        }
        cls.mock_db_config = patch.dict(utils.config, testconfig)

    @classmethod
    def tearDownClass(cls):
        cnx = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        cursor = cnx.cursor(dictionary=True)

        # drop test database
        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
            cnx.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Database {} does not exists. Dropping db failed".format(MYSQL_DB))
        cnx.close()
