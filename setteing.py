def showSettingsPage():
    option = input()
    if option == '總預算':
        enterBudget()
    elif option == '每月固定收支':
        enterFixedIE()
    elif option == '類別':
        enterCategory()
    elif option == '餘額':
        enterBalance()
    elif option == '地點':
        enterLocation()
    pass

# > 查看/修改總預算
# > 新增每月固定收支
# > 查看/新增/修改/刪除類別
# > 查看/新增/修改/刪除餘額
# > 查看/新增/修改/刪除地點

# 查看/修改總預算
def enterBudget():
    action = input()
    if action == '查看':
        readBudget()
    else:
        updateBudget()
    pass

def readBudget():
    pass

def updateBudget():
    pass

# 新增每月固定收支
def enterFixedIE():
    pass

def createFixedIE():
    pass

# 查看/新增/修改/刪除類別
def enterCategory():
    pass

def createCategory():
    pass

def readCategory():
    pass

def updateCategory():
    pass

def deleteCategory():
    pass

# 查看/新增/修改/刪除餘額
def enterBalance():
    pass

def createBalance(name, amount, category):
    pass

def readBalance(name):
    pass

def updateBalance(name, newBalance):
    pass

def deleteBalance(name):
    pass


# 查看/新增/修改/刪除地點
def enterLocation():
    pass

def createLocation():
    pass

def readLocation():
    pass

def updateLocation():
    pass

def deleteLocation():
    pass