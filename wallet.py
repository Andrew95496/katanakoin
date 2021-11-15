import datetime
import math
from tkinter import *

import easygui
import psycopg2

from config import bcolors
from config import configs as cf
from modules import updatehash
from modules.coin_class import mint_coins


# this function creates a wallet for the user using their wallet_key
def create_wallet(key):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            host = cf.hostname,
            dbname = cf.database,
            user = cf.username,
            password = cf.pwd,
            port = cf.port_id)

        cur = conn.cursor()
        address = updatehash(key)
        create_script = f''' CREATE TABLE IF NOT EXISTS wallet{address} (
                                id int    PRIMARY KEY,
                                wallet_key    varchar(1000) NOT NULL UNIQUE,
                                address     varchar(1000) NOT NULL UNIQUE,
                                balance    int DEFAULT 0
                                )'''
        #transactions table
        create_trans = f''' CREATE TABLE IF NOT EXISTS transactions{address} (
                                sender_address   varchar(1000) NOT NULL ,
                                receiver_address     varchar(1000) NOT NULL ,
                                amount    int NOT NULL,
                                timestamp varchar(100) NOT NULL
                                )'''

        cur.execute(f"SELECT has_wallet FROM wallet_keys WHERE key = '{key}'")
        has_wallet = cur.fetchone()
        if has_wallet[0] == False:
            cur.execute(create_script)
            cur.execute(create_trans)
            cur.execute(f"UPDATE wallet_keys SET has_wallet = TRUE WHERE key = '{key}'")
            insert_script = f'insert into wallet{address}(id, wallet_key, address, balance) VALUES ( %s,%s,%s,%s)' 
            insert_values = (1 , key, address, 0 )
            cur.execute(insert_script, insert_values)
            print(f"{bcolors.OKGREEN}\nWallet Created!!!{bcolors.ENDC}")
            easygui.msgbox(f"Wallet for wallet{address} created!\nPublic address: {address}")
        else:
            print(f"{bcolors.WARNING}\nWallet already exist{bcolors.ENDC}")
            easygui.msgbox("Wallet already exist")
        conn.commit()
        
    except Exception as error:
        print(f'{bcolors.FAIL}{error}{bcolors.ENDC}')
        easygui.msgbox("Something went wrong!\nTry Again")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

###############################################################################################################################

# buy coins function

def buy_coins(key,address,amount):
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            host = cf.hostname,
            dbname = cf.database,
            user = cf.username,
            password = cf.pwd,
            port = cf.port_id)

        cur = conn.cursor()
        if amount <= 0:
            print(f"{bcolors.FAIL}AMOUNT ENTERED MUST BE GREATER THAN 0{bcolors.ENDC}")

        else:
            cur.execute(f"SELECT balance FROM wallet{address}")
            current_amount = cur.fetchone()
            cur.execute(f"SELECT * FROM pg_catalog.pg_tables WHERE tablename = 'wallet{address}'")
            wallet_exist = cur.fetchone()
            cur.execute(f"SELECT address FROM wallet{address} WHERE address = '{address}'")
            address_exist = cur.fetchone()
            cur.execute(f"SELECT address FROM wallet{address} WHERE wallet_key = '{key}'")
            key_exist = cur.fetchone()
            if address_exist and wallet_exist and key_exist:
                cur.execute("SELECT count(coin_number) FROM katanakoins WHERE owned_by = 'None'")
                count = cur.fetchone()
                if count[0] <= amount:
                    mint_coins(amount + math.ceil(math.log2(amount)))
                for _ in range(amount):
                    cur.execute("SELECT coin_number FROM katanakoins WHERE owned_by = 'None' order by coin_number desc limit 1")
                    coins = cur.fetchone()
                    inc = coins[0]
                    cur.execute(f"UPDATE katanakoins SET owned_by = '{address}' WHERE  coin_number = {inc} ")
                    inc -= 1
                cur.execute(f"UPDATE wallet{address} SET balance = '{current_amount[0] + amount}' ")
                insert_script = f'insert into transactions{address}(sender_address,receiver_address, amount, timestamp ) VALUES ( %s,%s,%s,%s)' 
                insert_values = ( 'money supply', address, amount, datetime.datetime.now() )
                cur.execute(insert_script, insert_values)
                print(f'\n{bcolors.BOLD}{amount}{bcolors.ENDC}{bcolors.OKGREEN} coin(s) bought!{bcolors.ENDC}\n')
                easygui.msgbox(f'{amount} coin(s) bought')
            else:
                print(f"\n{bcolors.FAIL}wallet and/or address does not exist{bcolors.ENDC}\n")
                easygui.msgbox("Wallet and/or address does not exist")
                


        conn.commit()
        
    except Exception as error:
        print(f'{bcolors.FAIL}{error}{bcolors.ENDC}')
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

###############################################################################################################################

# send coins function

def send_coins(key,sender_address, receiver_address, amount):
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            host = cf.hostname,
            dbname = cf.database,
            user = cf.username,
            password = cf.pwd,
            port = cf.port_id)
        cur = conn.cursor()
        
        #queries
        
        #GET key
        cur.execute(f"SELECT wallet_key FROM wallet{sender_address} WHERE wallet_key = '{key}'")
        key_exist = cur.fetchone()

        #GET sender address
        cur.execute(f"SELECT address FROM wallet{sender_address} WHERE address = '{sender_address}'")
        sender_exist = cur.fetchone()

        #GET receiver address
        cur.execute(f"SELECT address FROM wallet{receiver_address} WHERE address = '{receiver_address}'")
        receiver_exist = cur.fetchone()
        
        # Compare data query to input
        if sender_address == 'None' or receiver_address == 'None' or amount <= 0:
            print(f"{bcolors.FAIL}FIX YOUR ENTRIES{bcolors.ENDC}")
            easygui.msgbox('FIX YOUR ENTRIES')
        elif key_exist[0] == key and sender_exist[0] == sender_address and receiver_exist[0] == receiver_address:
            cur.execute(f"SELECT BALANCE FROM wallet{sender_address}")
            coins = cur.fetchone()
            if coins[0] == None or amount > coins[0]:
                print(f"{bcolors.FAIL}Insufficient Funds!!!{bcolors.ENDC}")
                easygui.msgbox('Insufficient Funds!!!')
            else:
                for _ in range(amount):
                    cur.execute(f"SELECT coin_number FROM katanakoins WHERE owned_by = '{sender_address}' ORDER BY coin_number desc limit 1")
                    incr = cur.fetchone()
                    cur.execute(f"UPDATE katanakoins SET owned_by = '{receiver_address}' WHERE  owned_by = '{sender_address}' and coin_number={incr[0]}")
                cur.execute(f"SELECT balance FROM wallet{receiver_address}")
                current_amount = cur.fetchone()

                # UPDATE coins in wallet 
                cur.execute(f"UPDATE wallet{receiver_address} SET balance = '{current_amount[0] + amount}' ")
                cur.execute(f"SELECT balance FROM wallet{sender_address}")
                current_amount = cur.fetchone()
                cur.execute(f"UPDATE wallet{sender_address} SET balance = '{current_amount[0] - amount}' ")

                # UPDATE sender transaction
                insert_script = f"insert into transactions{sender_address}(sender_address,receiver_address, amount, timestamp) VALUES ( '{sender_address}', '{receiver_address}', {amount}, '{datetime.datetime.now()}')" 
                cur.execute(insert_script)

                #GET timestamp from sender
                cur.execute(f"SELECT timestamp FROM transactions{sender_address} ORDER BY timestamp DESC LIMIT 1")
                date = cur.fetchone()

                # UPDATE receiver transaction
                insert_script = f"insert into transactions{receiver_address}(sender_address,receiver_address, amount, timestamp) VALUES ( '{sender_address}', '{receiver_address}', {amount}, '{date[0]}' )"
                cur.execute(insert_script)
                print(f'{bcolors.HEADER}{receiver_address}{bcolors.ENDC}{bcolors.OKGREEN} has received payment{bcolors.ENDC}{bcolors.ENDC}\n{bcolors.OKCYAN}amount:{bcolors.ENDC} {bcolors.BOLD}{amount}{bcolors.ENDC}\n{bcolors.OKCYAN}sender:{bcolors.ENDC}{bcolors.ENDC} {bcolors.BOLD}{sender_address}{bcolors.ENDC}')
                easygui.msgbox(f'{receiver_address} has received payment\namount: {amount}\nsender: {sender_address}')
        else:
            print(f"\n{bcolors.FAIL}Try again...something went wrong{bcolors.ENDC}\n")
            easygui.msgbox('Try again...something went wrong')            
        conn.commit()
        
    except Exception as error:
        print(f'{bcolors.FAIL}{error}{bcolors.ENDC}')
        easygui.msgbox('Try again...something went wrong')  
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

