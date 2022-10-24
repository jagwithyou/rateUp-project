import psycopg2
import config

con = psycopg2.connect(
        database=config.database, 
        user=config.user,
        password=config.password,
        host=config.host, 
        port=config.port
    )
print("Database opened successfully")

cur = con.cursor()


cur.execute(''' CREATE TABLE users
        (ID SERIAL PRIMARY KEY,
        NAME     VARCHAR, 
        EMAIL    VARCHAR, 
        PASSWORD VARCHAR);''')
print("Table created successfully!")

con.commit()
con.close()