import psycopg2
from postgis.psycopg import register


conn = psycopg2.connect(host='******', user='******', password='******', port='****', dbname='******')
register(conn)
curr = conn.cursor()
