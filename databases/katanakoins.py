import psycopg2


hostname = 'localhost'
database = 'katanakoin'
username = 'postgres'
pwd = 'password'
port_id = 5432

conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = port_id
)

print("success")

conn.close()