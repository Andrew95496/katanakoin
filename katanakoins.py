import psycopg2
from modules import katanakoin
from config import configs as cf
from config import bcolors
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

        cur.execute('SELECT count(coin_number) FROM katanakoins')
        date = datetime.datetime.now()
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
        
        print("\nCoins Generated!!")

        cur.execute(f'SELECT * FROM katanakoins ORDER BY  coin_number DESC LIMIT {amount_to_gen}')
        for serial in cur.fetchall():
            print(f'''\n{bcolors.OKBLUE}Coin #:{bcolors.ENDC} {bcolors.WARNING}{serial[0]}{bcolors.ENDC}
            \n{bcolors.OKBLUE}Serial #:{bcolors.ENDC} {bcolors.BOLD}{serial[1]}{bcolors.ENDC}
            \n{bcolors.OKBLUE}Hash:{bcolors.ENDC} {bcolors.BOLD}{serial[2]}{bcolors.ENDC}
            \n{bcolors.OKBLUE}Owner:{bcolors.ENDC} {bcolors.WARNING}{serial[3]}{bcolors.ENDC}
            \n{bcolors.OKBLUE}Timestamp:{bcolors.ENDC} {bcolors.WARNING}{serial[4]}{bcolors.ENDC}''')
            print('\n##########################################################################################################\n')


        conn.commit()
        

    except Exception as error:
        print(f'{bcolors.FAIL}{error}{bcolors.ENDC}')
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

generate_coins(100)

