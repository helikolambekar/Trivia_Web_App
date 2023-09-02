import psycopg2 , os
import sys

user_email = ''

if __name__ == "__main__":
    if len(sys.argv) > 0:
        user_email =sys.argv[1]
       
if user_email != "":
    try:     
        db_connection_url = os.environ['DATABASE_URL'].replace("://", "ql://", 1)
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(db_connection_url)
        cursor = conn.cursor()
      
        cursor.execute('UPDATE "Player" SET admin = TRUE WHERE email = %s' , (user_email,))

        conn.commit()
        cursor.close()
        print("ADMIN enabled from: " + str(user_email))
    except (Exception, psycopg2.DatabaseError) as error:
        print("An Error has occurd!")
        print(error)
   
else:
    print("please input an email when running this file")