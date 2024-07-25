class List():
    def __init__(self):
        self._lis = []


    def append(self, value):
        self._lis.append(value)


    def remove(self, value):
        self._lis.remove(value)

    def __iter__(self):
        while True:
            for i in self._lis:
                yield i