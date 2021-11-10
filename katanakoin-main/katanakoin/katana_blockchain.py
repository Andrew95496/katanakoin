# blockchain-imports

from hashlib import sha256
import datetime

def updatehash(*args):
    hashing_text = ""; h = sha256()
    for arg in args:
        hashing_text += str(arg)
    h.update(hashing_text.encode("utf-8"))
    return h.hexdigest()

class katanakoin():
    def __init__(self):
        self.serial_number()
    

    def serial_number(self):
        return updatehash(datetime.datetime.now())




class Block():
    data = katanakoin()
    hash = None
    nonce = 0
    previous_hash = "0" * 64

    def __init__(self, data, number=0):
        self.data = data
        self.number = number

    def hash(self):
        return updatehash(
            self.previous_hash, 
            self.number, 
            self.data.serial_number(), 
            self.nonce
        )

    def __str__(self):
        return str("Block#: {0}\nHash: {1}\nPrevious:".format(
                self.number, 
                self.hash()) + 
            " {0}\nData: {1}\nNonce: {2}\n" .format(
                self.previous_hash, 
                self.data.serial_number(), 
                self.nonce
            ))


class Blockchain():
    difficulty = 4

    def __init__(self, chain=[]):
        self.chain = chain

    def add(self, block):
        self.chain.append(block)

    def remove(self, block):
        self.chain.remove(block)

    def mine(self, block):
        try:
            block.previous_hash = self.chain[-1].hash()
        except IndexError:
            pass

        while True:
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.add(block); break
            else:
                block.nonce += 1

    def isValid(self):
        for i in range(1, len(self.chain)):
            _previous = self.chain[i].previous_hash
            _current = self.chain[i-1].hash()
            if _previous != _current or _current[:self.difficulty] != "0"*self.difficulty:
                return False

        return True


def main():
    katanakoins = Blockchain()
    database = [katanakoin(), katanakoin()]

    for data in database:
        num += 1
        katanakoins.mine(Block(data, num))

    for block in katanakoins.chain:
        print(block)
        print(f"Serial_number: {data.serial_number()}\n")    

if __name__ == "__main__":
    main()
