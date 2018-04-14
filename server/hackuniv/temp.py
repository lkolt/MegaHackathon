import psycopg2

conn = psycopg2.connect(host="10.0.1.99", database="hackathondb", user="postgres", password="", port="5432")
cur = conn.cursor()
cur.execute('SELECT * FROM Port_desc')
row = cur.fetchone()
while row is not None:
    print(row)
    row = cur.fetchone()

cur.close()