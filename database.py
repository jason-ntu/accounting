import mysql.connector
from mysql.connector import errorcode
import const
import sqlalchemy
from sqlalchemy_utils import database_exists, create_database, drop_database

config = {
    "user": const.MYSQL_USER,
    "host": const.MYSQL_HOST,
    "password": const.MYSQL_PASSWORD,
    "port": const.MYSQL_PORT,
}

class Database:

    def __init__(self, db_name):
        self.create_db(db_name)

    @classmethod
    def setup(cls, db_name=None):
        try:
            # Connect to the MySQL server or some database if specified
            cls.conn = mysql.connector.connect(**config, database=db_name)
            # Create a cursor object that returns query results as dictionaries
            cls.cursor = cls.conn.cursor(dictionary=True)
            print("%s...Connection created.%s" %
                  (const.ANSI_BLACK, const.ANSI_RESET))
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
        if cls.conn.is_connected():
            # Close the cursor
            cls.cursor.close()
            # Disconnect from the MySQL server
            cls.conn.close()
            print("%s...Connection closed.%s" %
                  (const.ANSI_BLACK, const.ANSI_RESET))

    @classmethod
    def create_db(cls, db_name):
        if not cls.setup():
            return False
        try:
            cls.cursor.execute(
                "CREATE DATABASE `%s` DEFAULT CHARACTER SET 'utf8';" % (db_name)
            )
            print("%s created." % db_name)
            result = True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DB_CREATE_EXISTS:
                print("%s already exists. Please manually drop it or provide another name." % (db_name))
            else:
                print("Failed creating database: {}".format(err))
            result = False
        cls.teardown()
        return result

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


if __name__ == "__main__":

    engine = sqlalchemy.create_engine("%s+%s://%s:%s@%s:%s/%s" % (const.MYSQL_DIALECT, const.MYSQL_DRIVER,
                                      const.MYSQL_USER, const.MYSQL_PASSWORD, const.MYSQL_HOST, const.MYSQL_PORT, const.MYSQL_DEV_DB))  
    if not database_exists(engine.url):
        create_database(engine.url)

    conn = engine.connect()
    metadata = sqlalchemy.MetaData()

    sqlalchemy.Table('Student', metadata,
                       sqlalchemy.Column('Id', sqlalchemy.Integer(), primary_key=True),
                       sqlalchemy.Column('Name', sqlalchemy.String(255), nullable=False),
                       sqlalchemy.Column('Major', sqlalchemy.String(255), default="Math"),
                       sqlalchemy.Column('Pass', sqlalchemy.Boolean(), default=True)
                       )

    metadata.create_all(engine)

    student = sqlalchemy.Table('Student', metadata, mysql_autoload=True,autoload_with=engine)

    conn.execute(student.insert().values(Id=1, Name='Matthew', Major="English", Pass=True))

    values_list = [{'Id':'2', 'Name':'Nisha', 'Major':"Science", 'Pass':False},
                {'Id':'3', 'Name':'Natasha', 'Major':"Math", 'Pass':True},
                {'Id':'4', 'Name':'Ben', 'Major':"English", 'Pass':False}]
    conn.execute(student.insert().values(values_list))

    output = conn.execute(student.select()).fetchall()
    print(output)

    conn.commit()

    drop_database(engine.url)
