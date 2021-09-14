import pickle
from pathlib import Path

configuration = 'n'


class Initial_Physics():

    folder = Path('Load')
    file = folder / 'Physics.txt'

    def load(self):
        f = open(self.file, 'rb')
        return pickle.load(f)

    def save(self):
        f = open(self.file, 'wb')
        pickle.dump(Physics, f)

    def __init__(self):

        if configuration == 'n':

            self.G = 6.674 * 10 ** -11
            self.time = 0

        else:

            instances = self.load()
            for instance in instances.__dict__.keys():
                setattr(self, instance, getattr(instances, instance))


Physics = Initial_Physics()

print(Physics.time)


