import psycopg2, os

try:  
    # connect to the PostgreSQL server
    db_connection_url = os.environ['DATABASE_URL'].replace("://", "ql://", 1)

    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(db_connection_url)
    print("Connection successful")
    
    cursor = conn.cursor()

    print("DELETEING QUESTIONS")
    cursor.execute('TRUNCATE TABLE "Question" RESTART IDENTITY')
    conn.commit()
    cursor.close()
    print("QUESTIONS DELETED!")
except (Exception, psycopg2.DatabaseError) as error:
    print("An Error has occurd!")
    print(error)