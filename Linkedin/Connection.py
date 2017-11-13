import pypyodbc
def getConnection(self ): 
    conn = pypyodbc.connect('Driver={SQL Server};'

                                        'Server=27.0.12.57;'

                                        'Database=VINTELLO_STAGING;'

                                        'uid=spider_user;pwd=Spider@123')
    return conn

## INSERT , UPDATE TO DB !!!
def insertUpdateDB(self , squery, value ): 
    conn = self.getConnection()
    cursor = conn.cursor()
    cursor.execute(squery, value)
    conn.commit()
    conn.close()
