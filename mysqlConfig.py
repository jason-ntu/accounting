from dotenv import dotenv_values

env = dotenv_values(".env")

DIALECT = "mysql"
DRIVER = "mysqldb"
HOST = env["MYSQL_HOST"]
USER = env["MYSQL_USER"]
PASSWORD = env["MYSQL_PASSWORD"]
PORT = "3306"
DEV_DB = "dev_accounting_book"
TEST_DB = "test_accounting_book"

dev = {
    'host': HOST,
    'user': USER,
    'password': PASSWORD,
    'port': PORT,
    'database': DEV_DB,
    'url': "%s+%s://%s:%s@%s:%s/%s?charset=utf8mb4" % (DIALECT, DRIVER,
                                       USER, PASSWORD, HOST, PORT, DEV_DB)
}

test = {
    'host': HOST,
    'user': USER,
    'password': PASSWORD,
    'port': PORT,
    'database': TEST_DB,
    'url': "%s+%s://%s:%s@%s:%s/%s?charset=utf8mb4" % (DIALECT, DRIVER,
                                       USER, PASSWORD, HOST, PORT, DEV_DB)
}
