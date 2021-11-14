import psycopg2
from modules import updatehash
from config import configs as cf
from config import bcolors
import platform
import datetime

def wallet_key_gen():
    conn = None
    cur = None
    try:
        date = datetime.datetime.now()
        plat = platform.platform()
        uname = platform.uname()
        conn = psycopg2.connect(
            host = cf.hostname,
            dbname = cf.database,
            user = cf.username,
            password = cf.pwd,
            port = cf.port_id)

        cur = conn.cursor()

        w_key = updatehash(date, plat,uname)
        get_database_len = 'SELECT count(id) FROM wallet_keys;'
        cur.execute(get_database_len)
        num = cur.fetchone()
        insert_script = 'insert into wallet_keys (id, key) VALUES ( %s,%s)' 
        insert_values = (num[0] , w_key, )
        cur.execute(insert_script, insert_values)
        

        print(f'{bcolors.OKBLUE}\nYour wallet key:{bcolors.ENDC}{bcolors.BOLD} {w_key}{bcolors.ENDC}{bcolors.ENDC}\n{bcolors.BOLD}{bcolors.HEADER}{bcolors.UNDERLINE}PLEASE KEEP PRIVATE!!!!{bcolors.ENDC}\n')
        conn.commit()
        

    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

wallet_key_gen()