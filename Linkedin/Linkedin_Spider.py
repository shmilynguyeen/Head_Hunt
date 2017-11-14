from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pypyodbc
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import logging
import Connection
class LinkedinSpider():
    try: 
        # Cấu hình file Logging
        
        #------------------- GET URL 
        listURL = {}
      
        ID = ""
        FLAG_SCRAWL =False
        # connection = Connection.getConnection()
        # cursor = connection.cursor()
        # # SQLCommand = ("SELECT distinct  linkedin_url , Company_ID FROM  Linkedin_getURL WHERE is_scrawl = 0 or (is_scrawl is null) and ( Company_ID is not null or LEN(Company_ID) >0 )")
        # SQLCommand = """ """
        # cursor.execute(SQLCommand)
        # results = cursor.fetchone()
        # print(SQLCommand)
        
        # while results:
        #     URL = results[0] # URL of company
        #     listURL[URL] = results[1] #DUNS of company
        #     print( results[0], results[1])
        #     print("----------------------------")
        #     results = cursor.fetchone()
        # connection.close()
        # time.sleep(10)
       
        # ----------------CONNECT TO LINKEDIN

        browser = webdriver.Chrome()     
        browser.get( "https://www.linkedin.com")

        username = browser.find_element_by_xpath("//*[@class='login-email']")
        password = browser.find_element_by_xpath("//*[@class='login-password']")
        username.send_keys("scrapyvintagedecor@gmail.com")
        password.send_keys("duybaoo19")

        browser.find_element_by_xpath("//*[@class='login submit-button']").click()   
        print("-----Logging-----")
        time.sleep(1)
        print("-------------------------------START SEARCH--------------------")
      
        # GET DEATIL FOR EACH URL IN listURL
        listURL["Test"] = ["https://www.linkedin.com/in/baotrinh"]
        index = 0
        for URL in listURL.keys() : 
            print("URL : " , URL)
            try :
                # URL = str(listURL[URL])
                browser.get("https://www.linkedin.com/in/baotrinh") 
                print(URL)
                ID = listURL[URL]
                time.sleep(2)
                   
                
                # KHAI BAO BIEN
                name = ""
                headLine = ""
                company = ""
                location = ""
                connections = ""
                summary = ""
                name = ""
                headLine = ""
                company = ""
                school = ""

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") #kéo thanh cuộn xuống .
                time.sleep(3) 
                try:
                    name = browser.find_element_by_xpath("//*[@class='pv-top-card-section__name Sans-26px-black-85%']").text
                except NoSuchElementException : 
                    name = ""
                try:
                    headLine = browser.find_element_by_xpath("//*[@class='pv-top-card-section__headline Sans-19px-black-85%']").text
                except NoSuchElementException : 
                    headLine = ""
                try:
                    company = browser.find_element_by_xpath("//*[@class='pv-top-card-section__company Sans-17px-black-70% mb1 inline-block']").text
                except NoSuchElementException : 
                    company = ""
               
                try : 
                    listSchool = browser.find_elements_by_xpath("//*[@class='pv-education-entity pv-profile-section__card-item ember-view']") 
                    for x in listSchool : 
                        school += x.text + "\n"
                except NoSuchElementException :
                    school = ""
                location = browser.find_element_by_xpath("//*[@class='pv-top-card-section__location Sans-17px-black-70% mb1 inline-block']").text
                connections = browser.find_element_by_xpath("//*[@class='pv-top-card-section__headline Sans-19px-black-85%']").text
                try:
                    summary = browser.find_element_by_xpath("//*[@class='pv-top-card-section__summary-text Sans-15px-black-55% mt5 pt5 ember-view']").text
                except NoSuchElementException : 
                    summary = ""
                experiences = ""
                try:
                    listExperiences = browser.find_elements_by_xpath("//*[@class='pv-profile-section__card-item pv-position-entity ember-view']")
                    for x in listExperiences: 
                        experiences += x.text + "\n"
                except NoSuchElementException : 
                    experiences = ""
                education = ""
                try : 
                    listEducation = browser.find_elements_by_xpath("//*[@class='pv-education-entity pv-profile-section__card-item ember-view']")
                    for x in listEducation:
                        education += x.text + "\n"
                except NoSuchElementException : 
                    education = ""
                skills = ""
                try:
                    listSkill = browser.find_elements_by_xpath("//li[@class='pv-skill-entity--featured pb5 pv-skill-entity relative pv-skill-entity--include-highlights ember-view']")
                
                    for x in listSkill: 
                        skills += x.text + "\n"
                except NoSuchElementException : 
                    skills = ""
                langaues = ""
                try: 
                    listLanguages = browser.find_elements_by_xpath("//*[@class='pv-profile-section accordion-panel pv-accomplishments-block languages ember-view']")
                
                    for x in listLanguages : 
                        langaues += x.text + "\n"    
                except NoSuchElementException : 
                    langaues = ""  
                course = ""
                try : 
                    listCourse = browser.find_elements_by_xpath("//*[@class='pv-profile-section accordion-panel pv-accomplishments-block courses ember-view']")
                    for x  in listCourse : 
                        course += x.text + "\n"  
                except NoSuchElementException : 
                    course = ""

                project = ""
                try : 
                    listProject = browser.find_elements_by_xpath("//*[@class='pv-profile-section accordion-panel pv-accomplishments-block projects ember-view']")
                    for x  in listCourse : 
                        project += x.text + "\n"  
                except NoSuchElementException : 
                    project = ""

                publication = ""
                try : 
                    listPublication = browser.find_elements_by_xpath("//*[@class='pv-profile-section accordion-panel pv-accomplishments-block publications ember-view']")
                    for x  in listCourse : 
                        publication += x.text + "\n"  
                except NoSuchElementException : 
                    publication = ""
            
                
            
            # ------------SAVE AS DB
                print("----------HERE---------")
                conn = pypyodbc.connect('Driver={SQL Server};'

                                      'Server=27.0.12.57;'

                                      'Database=VINTELLO_STAGING;'

                                      'uid=spider_user;pwd=Spider@123')
                cursor = conn.cursor()
                command = """INSERT INTO [dbo].[Linkedin_getDetail]
                ([name]
                ,[head_line]
                ,[company]
                ,[schools]
                ,[location]
                ,[connection]
                ,[sumary]
                ,[education]
                ,[skill]
                ,[languages]
                ,[course]
                ,[project]
                ,[publication] , url_detail , [Company_ID])
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
                value = [name, headLine, company, school, location,
                connections, summary, education, skills, langaues, course, project, publication, URL ,  ID]
                print(command)
                cursor.execute(command, value)
                conn.commit()
                conn.close()
                FLAG_SCRAWL = True
                print("INSERT DONE !")

            # SET FLAG SCRAWL 
             
                conn = pypyodbc.connect('Driver={SQL Server};'

                                     'Server=103.15.50.24;'

                                      'Database=VINTELLO_STAGING;'

                                      'uid=spider_user;pwd=Spider@123')
                if True == FLAG_SCRAWL :  
                    cursor = conn.cursor()
                    command = "UPDATE Linkedin_getURL SET is_scrawl = 1 WHERE linkedin_url =N'" + URL +   "'"
                    cursor.execute(command )
                    conn.commit()
                    conn.close()
                    flagScrawl = True
                    print(" Scrawled  DONE ! ")

            except Exception as e : 
                print(e)
                 # Add to logfile
                d = {'url': URL}
                logger = logging.getLogger('tcpserver')
                logger.warning('Problem: %s', e, extra=d)

        index += 1 
    except ValueError as e : 
        print(e)
        
 
            