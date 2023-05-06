import const
import sqlalchemy
from sqlalchemy_utils import database_exists, create_database, drop_database


def create_db(url):
    if not database_exists(url):
        create_database(url)

def init_db(url):
    engine = sqlalchemy.create_engine(url)
    conn = engine.connect()
    metadata = sqlalchemy.MetaData()

    sqlalchemy.Table('Student', metadata,
                     sqlalchemy.Column(
                         'Id', sqlalchemy.Integer(), primary_key=True),
                     sqlalchemy.Column(
                         'Name', sqlalchemy.String(255), nullable=False),
                     sqlalchemy.Column(
                         'Major', sqlalchemy.String(255), default="Math"),
                     sqlalchemy.Column(
                         'Pass', sqlalchemy.Boolean(), default=True)
                     )

    metadata.create_all(engine)

    student = sqlalchemy.Table(
        'Student', metadata, mysql_autoload=True, autoload_with=engine)

    conn.execute(student.insert().values(
        Id=1, Name='Matthew', Major="English", Pass=True))

    values_list = [{'Id': '2', 'Name': 'Nisha', 'Major': "Science", 'Pass': False},
                   {'Id': '3', 'Name': 'Natasha', 'Major': "Math", 'Pass': True},
                   {'Id': '4', 'Name': 'Ben', 'Major': "English", 'Pass': False}]
    conn.execute(student.insert().values(values_list))

    output = conn.execute(student.select()).fetchall()
    print(output)

    conn.commit()

def drop_db(url):
    if database_exists(url):
        drop_database(url)


if __name__ == "__main__":
    create_db(const.DEV_DB_URL)
    init_db(const.DEV_DB_URL)
