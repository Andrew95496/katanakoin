import psycopg2
from modules import updatehash
from config import configs as cf
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

        create_script = ''' CREATE TABLE IF NOT EXISTS wallet_keys (
                                id int    PRIMARY KEY,
                                key    varchar(1000) NOT NULL UNIQUE,
                                has_wallet    BOOLEAN DEFAULT FALSE
                                )  
                                '''
        cur.execute(create_script)

        w_key = updatehash(date, plat,uname)


        get_database_len = 'SELECT count(id) FROM wallet_keys;'
        cur.execute(get_database_len)
        num = cur.fetchone()
        insert_script = 'insert into wallet_keys (id, key) VALUES ( %s,%s)' 
        insert_values = (num[0] , w_key, )
        cur.execute(insert_script, insert_values)
        

        print(w_key)
        conn.commit()
        

    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()