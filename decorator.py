import re
from datetime import datetime

def profiling(argument):
    def _profiling(function):
        def wrapper(*args, **kwargs):
            startpoint = datetime.now()
            res = function(*args, **kwargs)
            endpoint = datetime.now()
            with open(argument, "a") as f:
                f.write("Function started execution: {} \
                   , Function finished execution: {}\n".format(str(startpoint), str(endpoint)))
            return res
        return wrapper
    return _profiling


class Sentence:

    def __init__(self, s=None):
        if not s:
            self.tokens = []
            self._is_it_ok = None
            return

        self.tokens = re.split(r'(\W+)', s)
        self._is_it_ok = None

    @property
    def is_it_ok(self):
        return self._is_it_ok

    @is_it_ok.setter
    def is_it_ok(self, value):
        if value:
            self._is_it_ok = True
            print("it's ok!")
        else:
            self._is_it_ok = False
            print("it's not ok!")

    def add_token(self, token):
        self.tokens.append(token)

    @profiling("sample.txt")
    def __str__(self):
        return "".join(self.tokens)

    def __add__(self, other):
        return Sentence(self.__str() + " " + other.__str())

    def __getitem__(self, index):
        return self.tokens[index]

    def __eq__(self, other):
        return self.__str() == other.__str()

    def __len__(self):
        return len(self.tokens)



s1 = Sentence('Жили-были дед да баба.')
s2 = Sentence('London is a capital of Great Britain.')

print(s1)

s1.is_it_ok = True
s1.is_it_ok = False