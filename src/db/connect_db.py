import mysql.connector

def connection(host="localhost", user="root", password="Admin", port=3307,database="rules_engine_db"):
    print("Processing...")
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database=database
        )
        cursor = mydb.cursor()
        print("Dtabase Connected Successfully")
        return mydb,cursor 
    except Exception as e:
        print("Dtabase Connection error:",e)