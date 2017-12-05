from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from random import randint
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from random import randint
import MyConnection
class  Bing_Linkedin_Spider():
    
    
###Purpose of Class :  Get Profile Linkedin URL from Bing using ThaiLand  CompanyName get from Hoover !!! 
 
    Spider_ID = 0
    timeStart = datetime.now()
    current_URL = ""

    


    def setSpider_ID (self , ID): 
        self.Spider_ID = ID

    def updateSpiderStatus(self, flag   ): 
        # Disable !
        if(int(flag) == 0 ):
            squery = """UPDATE [Spider_Status] SET [Status] = 0 , [Last_Page_Crawl] =? 
            , [Last_Stop]= ? , [Last_Start] = ? , [URL] = ?  WHERE [Row_ID] = ? """
            value =[ "", datetime.now() , self.timeStart, self.current_URL ,self.Spider_ID ]
            MyConnection.insertUpdateDB(squery, value )
        # Enable ! 
        else : 
            squery = """UPDATE [Spider_Status] SET [Status] = 1, [URL] = ?  WHERE [Row_ID] = ? """
            value = [self.current_URL , self.Spider_ID]
            MyConnection.insertUpdateDB(squery, value)
            self.timeStart = datetime.now()   
    
    def main(self , country , start , end , ID):
        try: 

            ## GET ALL COMPANY NAME TO  SEARCH  !
            listKey = {}
            connection = MyConnection.getConnection()
            cursor = connection.cursor()
            
            ## GET COMMPANY NAME  USED TO SEARCH WITH BING!! 
            SQLCommand =  """SELECT DISTINCT [D-U-N-S] , [Company_Name_Clean] FROM [Company] WHERE
             [Company_Name_Clean] is not null  AND [Is_Crawl] is NULL and [Row_ID] >= ? and [Row_ID]  < ?  """
            value = [start, end]
            cursor.execute(SQLCommand, value )
            results = cursor.fetchone()
            while results:
                DUNS_ID =  int(results[0]) # this is DUNS Number this comapany
                listKey[DUNS_ID] = results[1] # Name of Company
                results = cursor.fetchone()
            connection.close()
            
            ## Config for browser do not open web browser ! 
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            browser = webdriver.Chrome(chrome_options=options)  
            
            browser.get( "https://www.bing.com/")
            time.sleep(4)

            for duns in listKey.keys():
                
                time.sleep(randint(8,25))

                print("Company Search : " , listKey[duns])
                keys = " \"VietNam \" " +  " site: linkedin.com/in " + "\"" +   listKey[duns] + " \"" 
                KeySearch = browser.find_element_by_xpath("//*[@class='b_searchbox']")
                KeySearch.clear()
                KeySearch.send_keys(keys) # Truyền tên cty vào để search
                time.sleep(randint(2,6))
                # KeySearch.send_keys(u'\ue007') # Enter search ! 
                btnSearch = browser.find_element_by_xpath("//*[@id='sb_form_go']").click()
                sleep = int(randint(3,15))
                time.sleep(sleep)
                
                try: 
                    allRow = browser.find_elements_by_xpath("//*[@class='b_algo']")
                    count_2 = 0
                    if(0< len(allRow)):
                        while True : 
                            timeSpleep = randint(8, 30) #  Random delay time from  3 - 20s
                            print("TIME DELAY : ", timeSpleep)
                            time.sleep(timeSpleep)
                            if(50 == count_2): 
                                time.sleep(40)
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
                                    command = """INSERT INTO  [Linkedin_URL]
                                    ([Linkedin_Name]
                                    ,[Linkedin_URL]
                                    ,[DUNS_NUMBER]
                                    ,[Linkedin_Type]
                                    ,[Country])
                                VALUES (?,?,?,?,? )"""
                                    value = [companyName, urls , duns, "Profile" , country]
                                    MyConnection.insertUpdateDB(command, value)
                                    print("INSERT DONE ! " )
                                    count_2 +=1
                                except Exception as e:
                                    print ("INSERT CRAWL ERROR : " , e)
                            browser.find_element_by_xpath("//*[@class='sb_pagN']").click() # NExt page! 
                            time.sleep(3)     
                except Exception as e : 
                    print("ERROR  WHEN CRAWLING ! " , e)  
                
                # xác nhận đã search với keyword đó rồi :  
                try:
                    command = """UPDATE [Company]  SET [Is_Crawl] = 1 WHERE  [D-U-N-S] = ? """
                    value =[duns]
                    MyConnection.insertUpdateDB(command, value)
                    print("UPDATE Crawl DONE ! ")
                    time.sleep(2)
                except Exception as e : 
                    print( "UPDATE Crawl Error : " , e)   
        except Exception as e : 
            print("ERROR IS : ",e)

## Test ! 
if __name__ == "__main__":
    linkedin_1 = Bing_Linkedin_Spider()

    

# linkedin_1.main("VietNam" , 0,10000,11)
# linkedin_1.main("VietNam" , 10000,20000,11)
# linkedin_1.main("VietNam" , 20000,30000,11)
# linkedin_1.main("VietNam" , 30000,40000,11)
linkedin_1.main("VietNam" , 40000,50000,11)

# linkedin_1.main("VietNam" , 50000,60000,11)
# linkedin_1.main("VietNam" , 60000,70000,11)
# linkedin_1.main("VietNam" , 70000,80000,11)
# linkedin_1.main("VietNam" , 80000,90000,11)

