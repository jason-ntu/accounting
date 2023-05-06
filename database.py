import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

env = dotenv_values(".env")

ANSI_BLACK = "\033[30m"
ANSI_RED = "\033[31m"
ANSI_GREEN = "\033[32m"
ANSI_YELLOW = "\033[33m"
ANSI_BLUE = "\033[34m"
ANSI_MAGENTA = "\033[35m"
ANSI_CYAN = "\033[36m"
ANSI_WHITE = "\033[37m"
ANSI_RESET = "\033[0m"

config = {
    "host": env["MYSQL_HOST"],
    "user": env["MYSQL_USER"],
    "password": env["MYSQL_PASSWORD"],
    "port": env["MYSQL_PORT"],
}


class Database:
    @classmethod
    def setup(cls, db_name=None):
        try:
            if db_name == None:
                # Connect to the MySQL server
                cls.connection = mysql.connector.connect(**config)
            else:
                # Connect to the specified database
                cls.connection = mysql.connector.connect(**config, database=db_name)
            # Create a cursor object that returns query results as dictionaries
            cls.cursor = cls.connection.cursor(dictionary=True)
            print("%s...Connection created.%s" % (ANSI_BLACK, ANSI_RESET))
            return True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("User authorization error")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database doesn't exist")
            else:
                print(err)
            return False

    @classmethod
    def teardown(cls):
        if cls.connection.is_connected():
            # Close the cursor
            cls.cursor.close()
            # Disconnect from the MySQL server
            cls.connection.close()
            print("%s...Connection closed.%s" % (ANSI_BLACK, ANSI_RESET))

    @classmethod
    def create_db(cls, db_name):
        if not cls.setup():
            return False
        try:
            cls.cursor.execute(
                "CREATE DATABASE `%s` DEFAULT CHARACTER SET 'utf8';" % (db_name)
            )
            print("%s created." % db_name)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DB_CREATE_EXISTS:
                print("%s already exists. Please provide another name." % (db_name))
            else:
                print("Failed creating database: {}".format(err))
        cls.teardown()
        return True

    @classmethod
    def drop_db(cls, db_name):
        if not cls.setup():
            return False
        try:
            cls.cursor.execute("DROP DATABASE `%s`;" % (db_name))
            print("%s dropped." % db_name)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DB_DROP_EXISTS:
                print("%s does not exist." % (db_name))
            else:
                print("Failed dropping database: {}".format(err))
        cls.teardown()
        return True

    @classmethod
    def write_db(cls, db_name, query, params=None):
        if not cls.setup(db_name=db_name):
            return False
        try:
            cls.cursor.execute(query, params)
            cls.connection.commit()
            print("write succeeded.")
            result = True
        except mysql.connector.Error as err:
            print(err)
            cls.connection.rollback()
            result = False
        finally:
            cls.teardown()
            return result


if __name__ == "__main__":
    db_name = env["MYSQL_DEV_DB"]

    create_table = """CREATE TABLE `test_table` (
                  `id` varchar(10) NOT NULL PRIMARY KEY ,
                  `text` text NOT NULL,
                  `int` int NOT NULL
                )"""

    insert_table = """INSERT INTO `test_table` (`id`, `text`, `int`) VALUES
                            ('1', 'test_text', 1),
                            ('2', 'test_text_2',2)"""

    Database.create_db(db_name)
    Database.write_db(db_name, create_table)
    Database.write_db(db_name, insert_table)
    Database.drop_db(db_name)
