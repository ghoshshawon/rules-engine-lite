import mysql.connector

def get_databases(host="localhost", user="root", password="Admin", port=3307):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
    except Exception as e:
        print("error:",e)