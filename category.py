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
    def create():
        pass

    def read():
        pass
    
    def update():
        pass

    def delete():
        pass

    @classmethod
    def start(cls):
        pass
