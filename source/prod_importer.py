import psycopg2
import pandas as pd


try:
    db_connection_url = "postgres://wnwyemwseiinvp:41da118b3b56e4b4d58f6dd502e7cb9da6dd557c3b65f8450de9b378d749eb23@ec2-3-219-103-45.compute-1.amazonaws.com:5432/d13qt3p08qavg5"
    
    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(db_connection_url)
    print("Connection successful")
    cursor = conn.cursor()
    # print (cur.fetchall())
    df = pd.read_csv("Quiz_Questions.csv", encoding="ISO-8859-1")
    for index, row in df.iterrows():
        print(index)
        query = "INSERT INTO question (id, category, question, answer, option_1, option_2, option_3) VALUES (%s,%s, %s, %s, %s, %s, %s);"
        data = (
        index, row['Category'], row['Question'], row['Answer'], row['Option_1'], row['Option_2'], row['Option_3'])
        cursor.execute(query, data)
        conn.commit()
    conn.close()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
