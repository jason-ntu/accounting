from structure import Action
class Budget:

    def show(self):
        print('0: 查看總預算')
        print('1: 修改總預算')

    def choose(self):
        pass

    def execute(self,option):
        if option == Action.READ:
            self.read()
        elif option == Action.UPDATE:
            self.update()
        pass

    def read(self):
        pass

    def update(self):
        pass

    def start(self):
        self.show()
        option = self.choose()
        self.execute(option)




