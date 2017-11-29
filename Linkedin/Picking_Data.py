from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from random import randint
from datetime import datetime
import MyConnection

class LinkedinDetail():
    listURL = []
    FLAG_SCRAWL = False

    # def getListURL(self ): 
        

    def main(self) :
        try : 
            sQuery = """   SELECT  DISTINCT "URL"  ,"Head_Line", "Schools ",
            "Sumary", "Skill", "Experiences"   from "Linkedin_Detail" where "Is_Picked" is  null """ 
            conn = MyConnection.getConnection()
            cursor = conn.cursor()
            cursor.execute(sQuery)
            result = cursor.fetchone()
            HeadLine = ""
            Schools = ""
            Sumary = ""
            Skill = ""
            Experiences = ""

            while result : 
                url = result[0]
                HeadLine = result[1]
                Schools = result[2] 
                # Sumary = result[3]
                Skill = result[4]
                Experiences = result[5]


            ## GET ALL DETAIL ! 
                 
                li_Schools = Schools.split("---BREAK---")
                li_Sumary = Sumary.split("---BREAK---")
                li_Skill = Skill.split("---BREAK---")
                li_Experiences = Experiences.split("---BREAK---")

            ## Solve HeadLine ! 
                HeadLine = str(HeadLine).upper()
                # Kiểm tra trong Headline có từ "AT" không  ? 
                li_Headline = HeadLine.split()
                if ("AT" in li_Headline): 
                    index = int(li_Headline.index("AT"))
                    HeadLine = ' '.join(li_Headline[0 : (index - 1)])
            
            ## Solve Company ! 
                for x in li_Schools : 
                    try : 
                        temp = x.split("\n")
                        school_Name = temp[0]
                        title = temp[2]
                        duration = temp[6]
                        field_Study = temp[4]
                        active = temp[7].replace('Activities and Societies:','')

                        sQuery = """ INSERT INTO public."Linkedin_School"(
                        "School_Name", "Secondary_Title", "Date_Attended", 
                        "Activitive", "Linkedin_URL", "Field_Study")
                        VALUES (?, ?, ?, ?, ?, ?) """ 
                        value = [school_Name , title , duration, active  , 
                        url ,  field_Study]

                        MyConnection.insertUpdateDB(sQuery, value)
                        print("INSERT SCHOOL DONE ! ")

                    except Exception as e : 
                        print("Pick Schools ERROR " , e )

            # Solving Experiences !
                for x in li_Experiences : 
                    try : 
                        temp = x.split("\n")
                        position = temp[0]
                        company_Name = temp[2]
                        date_Empl = temp[4]
                        empl_Duration = temp[6]

                        location = ""
                        desctiption = ""
                        if(7 < len(temp)): 
                            location = temp[8]
                            desctiption = ' '.join(temp[9 : (len(temp))])
                            print(desctiption)
                        

                        sQuery = """INSERT INTO public."Linkedin_Experiences"(
                            "Position", "Company_Name", "Date_Employee", "Employee_Duration", "Location", 
                            "Description", "URL")
                            VALUES (?, ?, ?, ?, ?, ?, ?) """
                        value = [position, company_Name, date_Empl, empl_Duration,
                        location, desctiption, url]
                        
                        MyConnection.insertUpdateDB(sQuery, value)
                        print("INSERT EXPERIENCES DONE ! ")
                    except Exception as e : 
                        print("Pick EXPERIENCES ERROR " , e )

            # Solving Skill !
                for x in li_Skill : 
                    try : 
                        temp = x.split("\n")
                        for i in temp: 
                            sQuery  = """INSERT INTO public."Linkedin_Skill"(
                            "Skill", "URL")
                            VALUES (?,?)""" 
                            value = [i.strip(), url]

                            MyConnection.insertUpdateDB(sQuery, value)
                            print("INSERT SKILL DONE ! ")
                    except Exception as e: 
                        print("INSERT SKILL ERROR ! ",e)

            ## UPDATE Is_Picked for thí URL ! 
                try : 
                    sQuery = """  UPDATE "Linkedin_Detail" SET "Is_Picked" = '1'  WHERE "URL" =  ?""" 
                    value = [url]
                    MyConnection.insertUpdateDB(sQuery, value)
                    print("Update DONE ! ")
                except Exception as e : 
                    print("UPDATE ERROR ! ", e)
                result = cursor.fetchone()
            conn.close()


        except Exception as e : 
            print("ERROR ! " , e)
 
if __name__=="__main__": 
    linkedin = LinkedinDetail()
    linkedin.main()

        
 
            