import datetime
import platform

import easygui
import psycopg2

from config import bcolors
from config import configs as cf
from modules import updatehash


# creating a private key 
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
        
        #display private key
        easygui.msgbox(f'''\nYour wallet key:\n{w_key}\n
        \nPLEASE KEEP PRIVATE!!!!\n''')

        conn.commit()
        

    except Exception as error:
        print(f'{bcolors.FAIL}{error}{bcolors.ENDC}')
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

