# blockchain-imports
from hashlib import sha256
import datetime
import math
import time


# def value(self):
#         URL = "https://crypto.com/price/shiba-inu"
#         results = requests.get(URL)
#         src = results.content

#         html = BeautifulSoup(src, features="html.parser")
#         temp = html.find('span', "chakra-text")
#         value = temp.get_text()
#         return value

database = []
total_supply = len(database)

def updatehash(*args):
    hashing_text = ""; h = sha256()
    for arg in args:
        hashing_text += str(arg)
    h.update(hashing_text.encode("utf-8"))
    return h.hexdigest()

#katanakoin 

class katanakoin():

    def __init__(self):
        self.serial_number()
    
    def serial_number(self):
        return updatehash(datetime.datetime.now())


# create coins  

def generate_starting_supply():
    coins = int(input("Generate coins: "))
    for coin in range(coins):
        coin = katanakoin()
        database.append(coin)

def auto_generate_coins(amount_to_gen):
        try:
            coins = math.ceil(math.log2(amount_to_gen))
        except ValueError:
            coins = 5
        for coin in range(coins):
            coin = katanakoin()
            database.append(coin) 
        
# Transactions
class Transaction():

    def __init__(self):
        pass
        
        
    def send(key, amount, receiver):
        pass

    def receive(key, amount, sender):
        pass

    def buy(key, amount_to_buy = int(input("Buy: "))):
        if total_supply <= amount_to_buy:
            auto_generate_coins(amount_to_buy)
        else:
            #send to wallet
            pass



# Block
class Block():
    data = None
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
            self.data, 
            self.nonce
        )


    def __str__(self):
        
        return str("\nBlock #: {0}\nHash: {1}\nPrevious:".format(
                self.number, 
                self.hash()) + 
                " {0}\nSerial #: {1}\nNonce: {2}\nTimestamp: {3}\n" .format(
                self.previous_hash, 
                self.data.serial_number(), 
                self.nonce,
                datetime.datetime.now()
            ))


# Blockchain
class Blockchain():
    
    def __init__(self, chain=[]):
        self.chain = chain
        self.difficulty = len(self.chain)
        

    def add(self, block):
        self.chain.append(block)

    # def remove(self, block):
    #     self.chain.remove(block)

    def mine(self, block):
        # reward sent to miners wallet
        reward = (len(self.chain) * self.difficulty) - len(self.chain)
        try:
            block.previous_hash = self.chain[-1].hash()
        except IndexError:
            pass

        while True:
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.add(block)
                self.difficulty += 1
                if self.difficulty < 5:
                    self.difficulty == 5 
                break
            else:
                block.nonce += 1
                

    def isValid(self):
        for i in range(1, len(self.chain)):
            _previous = self.chain[i].previous_hash
            _current = self.chain[i-1].hash()
            if _previous != _current or _current[:self.difficulty] != "0"*self.difficulty:
                return False

        return True



