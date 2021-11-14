import psycopg2
import plotly.express as px


hostname = 'localhost'
database = 'katanakoin'
username = 'drewskikatana'
pwd = 'password'
port_id = 5432


def get_data():
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id)
        
        # cursor
        cur = conn.cursor()
        
        
        #queries
        
        conn.commit()
        
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()