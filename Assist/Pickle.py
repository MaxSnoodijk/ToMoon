import pickle
from pathlib import Path

# Initial save class and load class same name!
# () after class NOT redundant
# Always work with __init__


class Initial_Physics():

    folder = Path('Load')
    file = folder / 'Physics.txt'

    def save(self):
        f = open(self.file, 'wb')
        pickle.dump(Physics, f)

    def __init__(self):
        self.G = 6.674 * 10 ** -11
        self.time = 10


Physics = Initial_Physics()
Physics.save()
