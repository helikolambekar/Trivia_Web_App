import psycopg2
db_connection_url=""
print('Connecting to the PostgreSQL database...')
conn = psycopg2.connect(db_connection_url)
print("Connection successful")
cursor = conn.cursor()

# cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
# x = cursor.fetchall()
# print(x)
cursor.execute('SELECT * FROM "Question"')
x = cursor.fetchall()

for y in x:
   print(y)

user_id=7
cursor.execute(''' SELECT category, MAX(score) FROM "LeaderboardScore" where userid = '%s' group by category ''', [user_id] )
z = cursor.fetchall()
for y in z:
    print(y)