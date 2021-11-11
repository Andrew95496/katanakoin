import psycopg2
from blockchain import katanakoin
import datetime



def generate_coins(amount_to_gen):
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

        create_script = ''' CREATE TABLE IF NOT EXISTS katanakoins (
                                coin_number int    PRIMARY KEY,
                                serial_number    varchar(1000) NOT NULL,
                                hash    varchar(1000) NOT NULL,
                                timestamp    varchar(100) NOT NULL
                                )   
                                '''

        cur.execute(create_script)
        get_database_len = 'SELECT count(coin_number) FROM katanakoins;'

        cur.execute(get_database_len)
        num = cur.fetchone()
        conn.commit()
        id = 0
        inc = 0
        for _ in range(amount_to_gen):
            serial = katanakoin.serial_number(date)
            id =  num[0] + inc
            insert_script = 'insert into katanakoins (coin_number, serial_number, hash, timestamp) VALUES (%s, %s, %s, %s)' 
            insert_values = ( id, serial, katanakoin.serial_number(serial), date)
            cur.execute(insert_script, insert_values)
            conn.commit()
            inc += 1
        
        print("Coins Generated!!")

        cur.execute('SELECT * FROM katanakoins;')
        for serial in cur.fetchall():
            print(f'\nCoin #: {serial[0]}\nSerial #: {serial[1]}\nHash: {serial[2]}\nTimestamp: {serial[3]}')


        conn.commit()
        

    except SyntaxError:
        print("Something went wrong")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

generate_coins(int(input("How many coins to generate: ")))