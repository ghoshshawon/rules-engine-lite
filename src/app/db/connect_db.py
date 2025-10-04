import mysql.connector

def connection(host="localhost", user="root", password="Admin", port=3307):
    print("Processing...")
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        print("Dtabase Connected Successfully")
    except Exception as e:
        print("error:",e)