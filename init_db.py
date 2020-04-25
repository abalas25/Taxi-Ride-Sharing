import psycopg2
from postgis.psycopg import register


conn = psycopg2.connect(host='localhost', user='postgres', password='Prototype1998', port='5432', dbname='TEST_GEO')
register(conn)
curr = conn.cursor()
