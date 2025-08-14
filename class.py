class MyIter:
    def __init__(self, number):
        self.number = number

    def __iter__(self):
        self.i = 1
        return self

    def __next__(self):
        if self.i<=self.number:
            x = self.i
            self.i += 1
            return x
        else:
            raise StopIteration

o1=MyIter(10)

for i in o1:
    print(i)
