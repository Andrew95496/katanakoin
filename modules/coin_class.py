# module-imports
from hashlib import sha256
import datetime
import psycopg2
import datetime

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
def mint_coins(amount_to_mint):
    hostname = 'localhost'
    database = 'katanakoin'
    username = 'drewskikatana'
    pwd = 'password'
    port_id = 5432
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id)

        cur = conn.cursor()

        date = datetime.datetime.now()

        get_database_len = 'SELECT count(coin_number) FROM katanakoins;'

        cur.execute(get_database_len)
        num = cur.fetchone()
        conn.commit()
        id = 0
        inc = 0
        for _ in range(amount_to_mint):
            serial = katanakoin.serial_number(date)
            id =  num[0] + inc
            insert_script = 'insert into katanakoins (coin_number, serial_number, hash,owned_by, timestamp) VALUES (%s, %s, %s, %s,%s)' 
            insert_values = ( id, serial, katanakoin.serial_number(serial), 'None', date)
            cur.execute(insert_script, insert_values)
            conn.commit()
            inc += 1
        
        print(f"{amount_to_mint} coin(s) created!")


        conn.commit()
        

    except SyntaxError:
        print("Something went wrong")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()




