class Person:
    def __init__(self):
        self.a=12
        self._b=2
        self.__c=3

    def test(self):
        print(self.__c)

p1=Person()
p1.test()
p1.__c=14