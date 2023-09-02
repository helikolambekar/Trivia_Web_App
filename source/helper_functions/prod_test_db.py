import psycopg2, os
def db_exists():
    try:
        db_connection_url = os.environ['DATABASE_URL'].replace("://", "ql://", 1)
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(db_connection_url)
        print("Connection successful")
        cursor = conn.cursor()

        cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
        x = cursor.fetchall()

        if len(x) == 0:
            return False
        else:
            return True

    except (Exception, psycopg2.DatabaseError) as error:
        print("An Error has occurd!")
        print(error)