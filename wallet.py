import psycopg2
from  modules import updatehash
from config import configs as cf
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
        create_script = f''' CREATE TABLE IF NOT EXISTS wallet{key} (
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
            insert_script = 'insert into wallet' + key + ' (id, wallet_key, address, katanakoins) VALUES ( %s,%s,%s,%s)' 
            insert_values = (1 , key, address, 0 )
            cur.execute(insert_script, insert_values)
            print(f"Wallet for '{key}' created!")
        else:
            print("Wallet already exist")
        
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
        cur.execute(f"SELECT * FROM pg_catalog.pg_tables WHERE tablename = wallet{key}")
        wallet_exist = cur.fetchone()
        cur.execute(f"SELECT address FROM wallet{key} WHERE address = '{address}'")
        address_exist = cur.fetchone()
        if address_exist and wallet_exist:
            cur.execute("SELECT count(coin_number) FROM katanakoins WHERE owned_by = 'None'")
            count = cur.fetchone()
            if count[0] <= amount:
                mint_coins(amount)
            for _ in range(amount):
                cur.execute("select coin_number from katanakoins WHERE owned_by = 'None' order by coin_number desc limit 1")
                coins = cur.fetchone()
                inc = coins[0]
                cur.execute(f"UPDATE katanakoins SET owned_by = '{address}' WHERE  coin_number = {inc} ")
                inc -= 1
            print(f'{amount} coins bought!')
        else:
            print("wallet and/or address does not exist")

        conn.commit()
        
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def send(sender_address, receiver_address, amount):
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
        if sender_address == 'None' or receiver_address == 'None':
            print(f'sender of {sender_address} cannot be sent to {receiver_address}')
        else:
            for _ in range(amount):
                    cur.execute(f"select coin_number from katanakoins WHERE owned_by = '{sender_address}' order by coin_number desc limit 1")
                    coins = cur.fetchone()
                    if coins == None:
                        print("Insufficent Funds!!!")
                    else:
                        inc = coins[0]
                        cur.execute(f"UPDATE katanakoins SET owned_by = '{receiver_address}' WHERE  owned_by = '{sender_address}' and coin_number={inc}")
                        print("Money Added")
                        
        conn.commit()
        
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

send('Andrew', 'Jade', 1000)