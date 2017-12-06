from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from random import randint
from datetime import datetime
import MyConnection
 

class Experiences_Header():
    
    # Xử lý bóc tách data Experiences theo từng trường
    listURL = []
    FLAG_SCRAWL = False

    # def getListURL(self ): 
        

    def main(self) :
        try : 
            # sQuery = """ SELECT DISTINCT [URL] , [Experiences] , [Location], [Avatar_URL], [Row_ID]
            # FROM [DB_LINKEDIN].[dbo].[Linkedin_Detail]
            # WHERE  Row_ID = '1507' """ 

            sQuery = """SELECT DISTINCT [URL] , [Experiences] , [Location], [Avatar_URL], [Row_ID]
            FROM [DB_LINKEDIN].[dbo].[Linkedin_Detail]
            WHERE    len (Experiences) > 5 and Row_ID < 1630  AND [Is_Tag] IS NULL """
            conn = MyConnection.getConnection()
            cursor = conn.cursor()
            cursor.execute(sQuery)
            result = cursor.fetchone()
           

            while result : 
                temp_Experiences  = result[1]
                location = result[2]
                url = result[0]
                avatar = result[3]
                profile_ID = result[4]
                 ## GET ALL  Experiences DETAIL ! 
                li_Experiences = temp_Experiences.split('---BREAK---')

            ## Solve HeadLine ! 
                for e in li_Experiences : 
                    temp_Element = e.split('\n')

                    try : 
                        position = temp_Element[0]
                        company_Name = temp_Element[2]
                        date_Employee = temp_Element[4]
                        employee_Duration = temp_Element[6]
                        location = temp_Element[8]
                        description_Exp = ' '.join(temp_Element[9 : (len(temp_Element))])

                        sQuery =  """ INSERT INTO [dbo].[LinkedIn_Experience_Header]
                                ( [URL]
                                ,[Position]
                                ,[Company_Name]
                                ,[Dates_Employed]
                                ,[Employment_Duration]
                                ,[Location]
                                ,[Experience_Description]
                                , [Profile_Id])
                            VALUES (?,?,?,?,?,?,?,?) """ 
                        value = [url ,position , company_Name , date_Employee , employee_Duration ,
                        location , description_Exp , profile_ID]
                        MyConnection.insertUpdateDB(sQuery  , value)
                        print("INSERT DONE ! ")
                    except Exception as e :  
                        print("NOT SAME PATTERN ! " , e)
                # UPDATE   ! 
                try :  
                    sQuery = """ UPDATE [Linkedin_Detail]  SET Is_Tag = 1 WHERE  [Row_ID] = ? """ 
                    value = [profile_ID] 
                    MyConnection.insertUpdateDB(sQuery , value)
                    print("UPDATE DONE ")
                except Exception as e : 
                    print("UPDATE ERROR ! "  , e )
                result = cursor.fetchone()
            conn.close()


        except Exception as e : 
            print("ERROR ! " , e)
 
if __name__=="__main__": 
    linkedin = Experiences_Header()
    linkedin.main()

        
 
            