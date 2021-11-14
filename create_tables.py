import psycopg2
from config import configs as cf
from modules.coin_class import katanakoin

def create_tables():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            host = cf.hostname,
            dbname = cf.database,
            user = cf.username,
            password = cf.pwd,
            port = cf.port_id)
        
        # cursor
        cur = conn.cursor()
        
        #create katanakoins table
        create_coins = ''' CREATE TABLE IF NOT EXISTS katanakoins (
                                coin_number int    PRIMARY KEY,
                                serial_number    varchar(1000) NOT NULL,
                                hash    varchar(1000) NOT NULL,
                                owned_by   varchar(1000) NOT NULL,
                                timestamp    varchar(100) NOT NULL
                                )   
                                '''
        cur.execute(create_coins)
        #create walley keys table
        create_keys = ''' CREATE TABLE IF NOT EXISTS wallet_keys (
                                id int    PRIMARY KEY,
                                key    varchar(1000) NOT NULL UNIQUE,
                                has_wallet    BOOLEAN DEFAULT FALSE
                                )  
                                '''
        cur.execute(create_keys)
        
        #queries
        
        conn.commit()
        
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

create_tables()