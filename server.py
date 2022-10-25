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


# cur.execute(''' CREATE TABLE users
#         (ID SERIAL PRIMARY KEY,
#         NAME     VARCHAR, 
#         EMAIL    VARCHAR, 
#         PASSWORD VARCHAR);''')

# cur.execute(''' CREATE TABLE games
#         (ID SERIAL PRIMARY KEY,
#         NAME     VARCHAR, 
#         DESCRIPTION    VARCHAR, 
#         FILENAME VARCHAR);''')
# print("Table created successfully!")

# cur.execute(''' CREATE TABLE game_rating
#         (ID SERIAL PRIMARY KEY,
#         RATING   INTEGER, 
#         MESSAGE    VARCHAR, 
#         RATEDBY INTEGER,
#         GAMEID INTEGER);''')
# print("Table created successfully!")

cur.execute(''' CREATE TABLE user
        (ID SERIAL PRIMARY KEY,
        NAME   VARCHAR, 
        EMAIL    VARCHAR, 
        PASSWORD INTEGER);''')
print("Table created successfully!")

con.commit()
con.close()