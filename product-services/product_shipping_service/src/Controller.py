import mysql.connector
from mysql.connector import errorcode
import os

MYSQL_DB_HOST=os.environ['MYSQL_DB_HOST']
MYSQL_DB_USERNAME=os.environ['MYSQL_DB_USERNAME']
MYSQL_DB_PASSWORD=os.environ['MYSQL_DB_PASSWORD']

try:
    cnx = mysql.connector.connect(user=MYSQL_DB_USERNAME,password=MYSQL_DB_PASSWORD,host=MYSQL_DB_HOST, database='shipping', pool_name="pool", pool_size=32)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password", flush=True)
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist", flush=True)

def retrieve_shipping():
    pooled_cnx = mysql.connector.connect(pool_name="pool")
    cursor = pooled_cnx.cursor()
    query = ("SELECT * from shipping.shipping")
    cursor.execute(query)
    result=cursor.fetchall()
    cursor.close()
    pooled_cnx.close()
    
    return result