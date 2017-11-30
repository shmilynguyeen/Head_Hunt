from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from random import randint
from datetime import datetime
import MyConnection
 

class Skill_Header():
    
    # Xử lý bóc tách data Skill theo từng trường
    listURL = []
    FLAG_SCRAWL = False

    # def getListURL(self ): 
        

    def main(self) :
        try : 
            sQuery = """ SELECT DISTINCT [URL] , [Skill] , [Row_ID], [Schools ]
            FROM [DB_LINKEDIN].[dbo].[Linkedin_Detail]
            WHERE  Row_ID = '1523' """ 
            conn = MyConnection.getConnection()
            cursor = conn.cursor()
            cursor.execute(sQuery)
            result = cursor.fetchone()
           

            while result : 
                url = result[0]
                skill = result[1]
                profile_ID = result[2]
                education  = result[3]
                 ## GET ALL  Experiences DETAIL ! 
                
                li_Skill = skill.split('---BREAK---')
                li_Edu = education.split('---BREAK---')
            
            ## Solve Skill  ! 
                for  x in li_Skill : 
                    if(len(x) >2 and None != x and '' != x ): 
                        try  :
                            sQuery = """INSERT INTO [dbo].[Linkedin_Skill_Header]
                                    ([Profile_ID]
                                    ,[URL]
                                    ,[Skill_Name])
                                VALUES(?,?,?) """ 
                            value = [profile_ID , url, x]
                            MyConnection.insertUpdateDB(sQuery, value)
                            print("INSERT SKILL DONE ! ")
                        except Exception as e : 
                            print("INSERT SKILL ERROR ! " , e)
                 
            ## Solve Education  ! 
                for e in li_Edu : 
                    if(len(e) >2 and None != e and '' != e ):
                        try : 
                            temp = e.split('\n')
                            school_Name = temp[0]
                            Degree_Name = temp[2]
                            field_Of_Study = temp[4]
                            dates_Attended = temp[6]
                            description = ' '.join(temp[7 : len(temp)])

                            sQuery = """INSERT INTO [dbo].[Linkedin_Education_Header]
                                ([Profile_ID]
                                ,[URL]
                                ,[School_Name]
                                ,[Degree_Name]
                                ,[Field_Of_Study]
                                ,[Dates_Attended_Or_Expected_graduation]
                                ,[Education_Description])
                            VALUES (?,?,?,?,?,?,?) """    
                            value = [profile_ID, url, school_Name, Degree_Name,
                            field_Of_Study, dates_Attended, description] 
                            MyConnection.insertUpdateDB(sQuery, value)
                            
                            print("INSERT EDU DONE ! ")  
                        except Exception as e : 
                            print("INSERT EDU ERROR ! " , e )

                result = cursor.fetchone()
            conn.close()


        except Exception as e : 
            print("ERROR ! " , e)
 
if __name__=="__main__": 
    linkedin = Skill_Header()
    linkedin.main()

        
 
            