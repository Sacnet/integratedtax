import MySQLdb

def connection():
    conn=MySQLdb.connect(host="localhost", user="root", passwd="", db="tgs")
    c=conn.cursor()
    return c, conn