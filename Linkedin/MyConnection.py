import pypyodbc
def getConnection(): 
    # conn = psycopg2.connect("dbname='DB_LINKEDIN' user='dbadmin' host='103.1.238.237' password='dbadmin@123'")
    conn = pypyodbc.connect('Driver={SQL Server};'

                                        'Server=103.1.238.237;'

                                        'Database=DB_LINKEDIN;'

                                        'uid=bao.nguyen;pwd=Bao@1234') 
    return conn

## INSERT , UPDATE TO DB !!!
def insertUpdateDB( squery, value ): 
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(squery, value)
    conn.commit()
    conn.close()
