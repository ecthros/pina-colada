import psycopg2

conn = psycopg2.connect("dbname='network' user='aces' host='localhost' password='aces'")
cur = conn.cursor()
cur.execute("create table computers(id serial, ip varchar (50), mac varchar(50), ports varchar(50), last_online varchar(50));")
cur.execute("Create table networks(id serial, name varchar(50), status varchar(50), last_online varchar(50));")
conn.commit()
cur.close()
