import os
import mysql.connector
from dotenv import load_dotenv
load_dotenv()
HOST=os.getenv("MYSQL_HOST","localhost"); PORT=int(os.getenv("MYSQL_PORT","3306")); USER=os.getenv("MYSQL_USER","root"); PASSWORD=os.getenv("MYSQL_PASSWORD",""); DATABASE=os.getenv("MYSQL_DATABASE","finguard_ai")

def get_server_connection(): return mysql.connector.connect(host=HOST,port=PORT,user=USER,password=PASSWORD)
def get_db_connection(): return mysql.connector.connect(host=HOST,port=PORT,user=USER,password=PASSWORD,database=DATABASE)
def create_database():
    c=get_server_connection(); cur=c.cursor(); cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DATABASE}`"); c.commit(); cur.close(); c.close()
if __name__=="__main__":
    create_database(); c=get_db_connection(); print("MySQL connected:",c.is_connected()); c.close()
