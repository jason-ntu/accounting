from enum import IntEnum, auto
import sqlalchemy as sql
from accessor import Accessor, ExecutionStatus as es
import const

class CategoryOption(IntEnum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()
    BACK = auto()


class CategoryPage(Accessor):
    def show():
        pass

    def choose():
        pass

    def execute():
        pass

    def create():
        pass

    def hint_create_name():
        pass

    def read():
        pass

    def update():
        pass

    def hint_update_name():
        pass

    def hint_update_new_name():
        pass

    def hint_delete():
        pass

    def delete():
        pass

    @classmethod
    def start(cls):
        pass

if __name__ == "__main__":  # pragma: no cover
    CategoryPage.start()