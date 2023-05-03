from enum import IntEnum, auto

class Record:
    direction: bool # 0: 'income' / 1: 'outcome'
    date: str # '2020-01-01'
    category: str # 'food'
    balanceType: str # 'Line pay'
    location: str # 'Taipei'
    amount: int # 100
    description: str # 'lunch'
    invoice: str # 'ABC12344567' (optional)
    timestamp: str # 2020-01-01 12:00:00 (系統自行判段)

class Balance:
    name: str # 'Line pay'
    amount: int # 10000
    category: bool # 0: not credit card / 1: credit card

class SettingsOption(IntEnum):
    BUDGET = auto()
    FIXEDIE = auto()
    CATEGORY = auto()
    BALANCE = auto()
    LOCATION = auto()

class Action(IntEnum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()