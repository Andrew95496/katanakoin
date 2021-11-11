import blockchain.katana_blockchain as kb
import time
import math
import numpy as np
import matplotlib.pyplot as plt

# def test_coin_gen():
#     database = []
#     start = time.time()
#     katanakoins = kb.Blockchain()
#     check = kb.Transaction()
#     coins = int(input("Generate coins: "))
#     for coin in range(coins):
#         coin = kb.katanakoin()
#         database.append(coin)
#     check.buy()
#     num = 0
#     for data in kb.database:
#         num += 1
#         katanakoins.mine(kb.Block(data, num))

#     for block in katanakoins.chain:  
#         print(block)
#     end = time.time()
#     print(end-start)


