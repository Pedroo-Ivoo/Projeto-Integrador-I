import sqlite3

connection = sqlite3.connect("database.db")

with open('schema.sql') as f:
    connection.executescript(f.read())
    

cur = connection.cursor()
    
cur.execute("INSERT INTO regioes (nome) VALUES (?)", ('Norte',))
cur.execute("INSERT INTO regioes (nome) VALUES (?)", ('Sul',))
cur.execute("INSERT INTO regioes (nome) VALUES (?)", ('Leste',))
cur.execute("INSERT INTO regioes (nome) VALUES (?)", ('Oeste',))


connection.commit()
connection.close()