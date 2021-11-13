import psycopg2
from modules import katanakoin
from config import configs as cf
import datetime



def generate_coins(amount_to_gen):
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

        date = datetime.datetime.now()

        create_script = ''' CREATE TABLE IF NOT EXISTS katanakoins (
                                coin_number int    PRIMARY KEY,
                                serial_number    varchar(1000) NOT NULL,
                                hash    varchar(1000) NOT NULL,
                                owned_by   varchar(1000) NOT NULL,
                                timestamp    varchar(100) NOT NULL
                                )   
                                '''

        cur.execute(create_script)

        cur.execute('SELECT count(coin_number) FROM katanakoins')
        num = cur.fetchone()
        id = 0
        inc = 0
        for _ in range(amount_to_gen):
            serial = katanakoin.serial_number(date)
            id =  num[0] + inc
            insert_script = 'insert into katanakoins (coin_number, serial_number, hash,owned_by, timestamp) VALUES (%s, %s, %s, %s, %s)' 
            insert_values = ( id, serial, katanakoin.serial_number(serial),"None", date)
            cur.execute(insert_script, insert_values)
            inc += 1
        
        print("Coins Generated!!")

        cur.execute('SELECT * FROM katanakoins')
        for serial in cur.fetchall():
            print(f'\nCoin #: {serial[0]}\nSerial #: {serial[1]}\nHash: {serial[2]}\nOwner: {serial[3]}\nTimestamp: {serial[4]}')


        conn.commit()
        

    except Exception:
        print("Something went wrong")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

generate_coins(1000)