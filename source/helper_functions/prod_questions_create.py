import os,psycopg2, pandas as pd
try:
    db_connection_url = os.environ['DATABASE_URL'].replace("://", "ql://", 1)
    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(db_connection_url)
    print("Connection successful")
    cursor = conn.cursor()
       
    os.chdir('../')
    df = pd.read_csv("Quiz_Questions.csv", encoding="ISO-8859-1")
    print("SUCESSFULLY OPENED CSV FILE!")
    for index, row in df.iterrows():
        print(index)
        query = 'INSERT INTO "Question" (category, question, answer, option_1, option_2, option_3) VALUES (%s, %s, %s, %s, %s, %s);'
        data = (row['Category'], row['Question'], row['Answer'], row['Option_1'], row['Option_2'], row['Option_3'])
        cursor.execute(query, data)
        conn.commit()
    conn.close()

except (Exception, psycopg2.DatabaseError) as error:
    print(error) 