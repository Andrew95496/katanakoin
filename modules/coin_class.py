# module-imports
from hashlib import sha256
import datetime
import psycopg2
import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# HASH creater
def updatehash(*args):
    hashing_text = ""; h = sha256()
    for arg in args:
        hashing_text += str(arg)
    h.update(hashing_text.encode("utf-8"))
    return h.hexdigest()

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

        
        
        get_database_len = 'SELECT count(coin_number) FROM katanakoins;'
        date = datetime.datetime.now()
        cur.execute(get_database_len)
        num = cur.fetchone()
        conn.commit()
        id = 0
        inc = 0
        for _ in range(amount_to_mint):
            serial = updatehash(date)
            id =  num[0] + inc
            insert_script = 'insert into katanakoins (coin_number, serial_number, hash,owned_by, timestamp) VALUES (%s, %s, %s, %s,%s)' 
            insert_values = ( id, serial, updatehash(serial), 'None', date)
            cur.execute(insert_script, insert_values)
            conn.commit()
            inc += 1
        conn.commit()
        

    except Exception as error:
        print(f'{bcolors.FAIL}{error}{bcolors.ENDC}')
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()