from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import pypyodbc
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from random import randint
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from random import randint
class  Bing_Linkedin_Spider():
    
    
###Purpose of Class :  Get Profile Linkedin URL from Bing using ThaiLand  CompanyName get from Hoover !!! 
 
    Spider_ID = 0
    timeStart = datetime.now()
    current_URL = ""

    def setCurrentURL (self , url ): 
        self.current_URL = url

   # Get Connection String
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


    def setSpider_ID (self , ID): 
        self.Spider_ID = ID

    def updateSpiderStatus(self, flag   ): 
        # Disable !
        if(int(flag) == 0 ):
            squery = """UPDATE [Spider_Status] SET [Status] = 0 , [Last_Page_Crawl] =? 
            , [Last_Stop]= ? , [Last_Start] = ? , [URL] = ?  WHERE [Row_ID] = ? """
            value =[ "", datetime.now() , self.timeStart, self.current_URL ,self.Spider_ID ]
            self.insertUpdateDB(squery, value )
        # Enable ! 
        else : 
            squery = """UPDATE [Spider_Status] SET [Status] = 1, [URL] = ?  WHERE [Row_ID] = ? """
            value = [self.current_URL , self.Spider_ID]
            self.insertUpdateDB(squery, value)
            self.timeStart = datetime.now()   
    
    def main(self , country , start , end , ID):
        try: 
            self.setSpider_ID(ID)
            self.updateSpiderStatus(1)
            # GET ALL KEY SEARCH 
            listKey = {}
            connection = self.getConnection()
            cursor = connection.cursor()
            
            # get commpany Name from Table ThaiLand_Company_ID using to search with Bing!! 
            SQLCommand = (""" SELECT  DISTINCT DUNS , Company_Name_Clean  FROM Hoover_Company_URL 
        WHERE Country ='ThaiLand' AND Is_Clean IS NOT NULL and Is_Crawl is NULL AND Row_ID >= ? AND Row_ID < ? """)
            value = [start, end]
            cursor.execute(SQLCommand , value)
            results = cursor.fetchone()
            while results:
                DUNS_ID =  int(results[0]) # this is Registration Tax of this comapany
                listKey[DUNS_ID] = results[1] # Name of Company
                # print(DUNS_ID, "-----", results[1])
                results = cursor.fetchone()
            connection.close()
            
            browser = webdriver.Chrome() 
            time.sleep(2)

            for duns in listKey.keys():
                self.setCurrentURL("https://www.bing.com/") 
                browser.get( "https://www.bing.com/")
                time.sleep(7)

                keys = ""
                print(listKey[duns])
                keys = " \"Current " +  listKey[duns].strip() +    " \""
                keys +=  "site: ( linkedin.com/in || linkedin.com/pub)" +   "\"Thailand"  + "\""
                KeySearch = browser.find_element_by_xpath("//*[@class='b_searchbox']")
                KeySearch.clear()
                KeySearch.send_keys(keys) # Truyền tên cty vào để search
                time.sleep(randint(1,4))
                # KeySearch.send_keys(u'\ue007') # Enter search ! 
                btnSearch = browser.find_element_by_xpath("//*[@id='sb_form_go']").click()
                sleep = int(randint(3,15))
                time.sleep(sleep)
                
                try: 
                    allRow = browser.find_elements_by_xpath("//*[@class='b_algo']")
                    count_2 = 0
                    if(0< len(allRow)):
                        while True : 
                            timeSpleep = randint(3, 10) #  Random delay time from  3 - 20s
                            print("TIME DELAY : ", timeSpleep)
                            time.sleep(timeSpleep)
                            if(50 == count_2): 
                                time.sleep(20)
                                count_2 = 0
                            allRow = browser.find_elements_by_xpath("//*[@class='b_algo']")
                            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") #kéo thanh cuộn xuống .
                            for x in allRow: 
                                txt = x.text
                                temp = txt.split()
                                findString = txt.find("LinkedIn")
                                urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', x.text)
                                companyName = txt[0: int(findString)]
                                urls = ''.join(urls)
                                print(urls)
                                print("--------------------------------------------------")

                                # Save to DB ! 
                                try:
                                    command = """INSERT INTO [dbo].[Linkedin_getURL]
                                                ([linkedin_name]
                                                ,[linkedin_url]
                                                ,[Country] ,[Linkedin_Type] ,  [Spider_ID] , [DUNS_NUMBER])
                                            VALUES (?,?,?,?,?,? )"""
                                    value = [companyName, urls ,  country ,"Profile" ,self.Spider_ID , duns]
                                    self.insertUpdateDB(command, value)
                                    print("INSERT DONE ! " , "-- Spider : " , self.Spider_ID)
                                    count_2 +=1
                                except Exception as e:
                                    print ("INSERT CRAWL ERROR : " , e)
                            browser.find_element_by_xpath("//*[@class='sb_pagN']").click() # NExt page! 
                            time.sleep(3)     
                except Exception as e : 
                    print("ERROR  WHEN CRAWLING ! " , e)  
                
                # xác nhận đã search với keyword đó rồi :  
                try:
                    command = """UPDATE Hoover_Company_URL  SET Is_Crawl = '1' WHERE  [DUNS]= ?"""
                    value =[duns]
                    self.insertUpdateDB(command, value)
                    print("UPDATE Crawl DONE ! ")
                    time.sleep(2)
                except Exception as e : 
                    print( "UPDATE Crawl Error : " , e)   
        except Exception as e : 
            print("ERROR IS : ",e)
            self.updateSpiderStatus(0)

## Test ! 
if __name__ == "__main__":
    linkedin_1 = Bing_Linkedin_Spider()

    

# Server VPS 
    # linkedin_1.main("ThaiLand" , 0,10000,11)
    # linkedin_1.main("ThaiLand" , 10000,20000,12)
    # linkedin_1.main("ThaiLand" , 20000,30000,13)
    # linkedin_1.main("ThaiLand" , 30000,40000,14) # Fin with 40.000

# Server BA 
    linkedin_1.main("ThaiLand" , 40000,50000,11)
    # linkedin_1.main("ThaiLand" , 50000,60000,12)
    # linkedin_1.main("ThaiLand" , 60000,70000,13)
    # linkedin_1.main("ThaiLand" , 70000,80000,14) # Fin with 40.000