import MySQLdb

def connection():
    conn = MySQLdb.connect(host = "localhost",
                           user = "root",
                           passwd = "password",
                           db = "light_control")

    c = conn.cursor()
    return c, conn
