import psycopg2
from  modules import updatehash
from config import configs as cf
from config import bcolors
from modules.coin_class import mint_coins
import math

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
                                katanakoins    int DEFAULT 0
                                )'''

        cur.execute(f"SELECT has_wallet FROM wallet_keys WHERE key = '{key}'")
        has_wallet = cur.fetchone()
        if has_wallet[0] == False:
            cur.execute(create_script)
            cur.execute(f"UPDATE wallet_keys SET has_wallet = TRUE WHERE key = '{key}'")
            insert_script = f'insert into wallet{address}(id, wallet_key, address, katanakoins) VALUES ( %s,%s,%s,%s)' 
            insert_values = (1 , key, address, 0 )
            cur.execute(insert_script, insert_values)
            print(f"Wallet for wallet{address} created!\nPublic address: {address}")
        else:
            print(f"{bcolors.WARNING}Wallet already exist{bcolors.ENDC}")
        
        conn.commit()
        
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


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
            cur.execute(f"SELECT katanakoins FROM wallet{address}")
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
                    cur.execute("select coin_number from katanakoins WHERE owned_by = 'None' order by coin_number desc limit 1")
                    coins = cur.fetchone()
                    inc = coins[0]
                    cur.execute(f"UPDATE katanakoins SET owned_by = '{address}' WHERE  coin_number = {inc} ")
                    inc -= 1
                cur.execute(f"UPDATE wallet{address} SET katanakoins = '{current_amount[0] + amount}' ")
                print(f'\n{bcolors.BOLD}{amount}{bcolors.ENDC}{bcolors.OKGREEN} coin(s) bought!{bcolors.ENDC}\n')
            else:
                print(f"\n{bcolors.FAIL}wallet and/or address does not exist{bcolors.ENDC}\n")


        conn.commit()
        
    except Exception as error:
        print(f'{bcolors.FAIL}{error}{bcolors.ENDC}')
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def send(key,sender_address, receiver_address, amount):
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
        cur.execute(f"SELECT address FROM wallet{sender_address} WHERE wallet_key = '{key}'")
        key_exist = cur.fetchone()
        if sender_address == 'None' or receiver_address == 'None' or amount <= 0:
            print(f"{bcolors.FAIL}FIX YOUR ENTRIES{bcolors.ENDC}")
        elif key_exist:
            cur.execute(f"SELECT katanakoins FROM wallet{sender_address}")
            coins = cur.fetchone()
            if coins[0] == None or amount > coins[0]:
                print(f"{bcolors.FAIL}Insufficent Funds!!!{bcolors.ENDC}")
            else:
                for _ in range(amount):
                    cur.execute(f"select coin_number from katanakoins WHERE owned_by = '{sender_address}' order by coin_number desc limit 1")
                    incr = cur.fetchone()
                    cur.execute(f"UPDATE katanakoins SET owned_by = '{receiver_address}' WHERE  owned_by = '{sender_address}' and coin_number={incr[0]}")
                cur.execute(f"SELECT katanakoins FROM wallet{receiver_address}")
                current_amount = cur.fetchone()
                cur.execute(f"UPDATE wallet{receiver_address} SET katanakoins = '{current_amount[0] + amount}' ")
                cur.execute(f"SELECT katanakoins FROM wallet{sender_address}")
                current_amount = cur.fetchone()
                cur.execute(f"UPDATE wallet{sender_address} SET katanakoins = '{current_amount[0] - amount}' ")
                print(f"\n{bcolors.BOLD}{bcolors.HEADER}{receiver_address}{bcolors.ENDC}{bcolors.OKGREEN} has received payment{bcolors.ENDC}{bcolors.ENDC}\n{bcolors.OKCYAN}amount:{bcolors.ENDC} {bcolors.BOLD}{amount}{bcolors.ENDC}\n{bcolors.OKCYAN}sender:{bcolors.ENDC}{bcolors.ENDC} {bcolors.BOLD}{sender_address}{bcolors.ENDC}")
        else:
            print(f"\n{bcolors.FAIL}Try again...something went wrong{bcolors.ENDC}\n")            
        conn.commit()
        
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

