import const
import sqlalchemy
from sqlalchemy_utils import database_exists, create_database, drop_database


def create_dev_db():
    engine = sqlalchemy.create_engine(const.DEV_DB_URL)
    if not database_exists(engine.url):
        create_database(engine.url)

def init_dev_deb():
    engine = sqlalchemy.create_engine(const.DEV_DB_URL)
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

def drop_dev_db():
    engine = sqlalchemy.create_engine(const.DEV_DB_URL)
    if database_exists(engine.url):
        drop_database(engine.url)

if __name__ == "__main__":
    create_dev_db()
    init_dev_deb()
