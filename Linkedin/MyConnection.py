import pypyodbc
def getConnection(): 
    conn = pypyodbc.connect('Driver={SQL Server};'

                                        'Server=SHMILYNGUYEN;'

                                        'Database=Vintello;'

                                        'uid=sa;pwd=1234')
    return conn

## INSERT , UPDATE TO DB !!!
def insertUpdateDB( squery, value ): 
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(squery, value)
    conn.commit()
    conn.close()
