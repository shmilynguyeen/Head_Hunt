from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from random import randint
import re
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import MyConnection

class LinkedinDetail():
    listURL = []
    FLAG_SCRAWL = False

    def getListURL(self ): 
        sQuery = """ SELECT DISTINCT "Linkedin_URL" from "Linkedin_URL" WHERE "Is_Crawl" is NULL   """ 
        conn = MyConnection.getConnection()
        cursor = conn.cursor()
        cursor.execute(sQuery)
        result = cursor.fetchone()
        while result : 
            self.listURL.append(result[0])
            result = cursor.fetchone()
        conn.close()

    def main(self) :
        try : 
            
            self.getListURL()
            browser = webdriver.Chrome()  
            # options = webdriver.ChromeOptions()
            # options.add_argument('headless')
            # browser = webdriver.Chrome(chrome_options=options)  

            # browser.get("https://www.google.com")
            # time.sleep(20)
            browser.get( "https://www.linkedin.com")
            # time.sleep(60)
            username = browser.find_element_by_xpath("//*[@class='login-email']")
            password = browser.find_element_by_xpath("//*[@class='login-password']")
            username.send_keys("scrapyvintagedecor@gmail.com")
            password.send_keys("duybaoo19")
            time.sleep(4)
            browser.find_element_by_xpath("//*[@class='login submit-button']").click()   
            time.sleep(randint(10,20))
        
            # GET DEATIL FOR EACH URL IN listURL ! 
            for URL in self.listURL  : 
                try :
                    browser.get(URL) 
                    browser.get("https://www.linkedin.com/in/vomanhtoan/")
                    print(URL)
                    time.sleep(randint(5,20))

                    # Show information profile ! 
                    try :
                        browser.find_element_by_xpath("//*[@class='contact-see-more-less link-without-visited-state']").click()
                    except Exception as e : 
                        print(e)
                    time.sleep(3)
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
                    phone= ""
                    email= ""
                    connected_Time = ""
                    experiences = ""

                    address = ""
                    website = ""
                    IM = ""
                    birthDay = ""
                    avatar = ""


                    browser.execute_script("window.scrollTo(0, 500);") #kéo thanh cuộn xuống .
                    time.sleep(5) 
                    try : 
                        avatar = browser.find_element_by_xpath("//*[@class=' presence-entity__image EntityPhoto-circle-8 ember-view']").get_attribute('style')
                        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', avatar)
                    except Exception as e: 
                        avatar = ""
                    browser.execute_script("window.scrollTo(0, 1000);") #kéo thanh cuộn xuống .
                    time.sleep(5)
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") #kéo thanh cuộn xuống .
                    time.sleep(5)
                    

                    try : 
                        address = browser.find_element_by_xpath("//*[@class='pv-contact-info__contact-type ci-address']").text
                    except Exception as e: 
                        address = ""
                    try : 
                        IM = browser.find_element_by_xpath("//*[@class='pv-contact-info__contact-type ci-ims']").text
                    except Exception as e : 
                        IM = ""
                    try : 
                        birthDay = browser.find_element_by_xpath("//*[@class='pv-contact-info__contact-type ci-birthday']").text
                    except Exception as e : 
                        birthDay = ""
                    try : 
                        website = browser.find_element_by_xpath("//*[@class='pv-contact-info__contact-type ci-websites']").text
                    except Exception as e : 
                        website = ""
                    try :
                        name = browser.find_element_by_xpath("//*[@class='pv-top-card-section__name Sans-26px-black-85%']").text
                    except Exception as e  : 
                        name = ""
                    try:
                        headLine = browser.find_element_by_xpath("//*[@class='pv-top-card-section__headline Sans-19px-black-85%']").text
                    except Exception as e  : 
                        headLine = ""
                    try:
                        company = browser.find_element_by_xpath("//*[@class='pv-top-card-section__company Sans-17px-black-70% mb1 inline-block']").text
                    except Exception as e  : 
                        company = ""
                
                    try : 
                        listSchool = browser.find_elements_by_xpath("//*[@class='pv-education-entity pv-profile-section__card-item ember-view']") 
                        for x in listSchool : 
                            school += x.text + "\n"
                    except Exception as e  :
                        school = ""
                    location = browser.find_element_by_xpath("//*[@class='pv-top-card-section__location Sans-17px-black-70% mb1 inline-block']").text
                    connections = browser.find_element_by_xpath("//*[@class='pv-top-card-section__headline Sans-19px-black-85%']").text
                    try:
                        summary = browser.find_element_by_xpath("//*[@class='pv-top-card-section__summary-text Sans-15px-black-55% mt5 pt5 ember-view']").text
                    except Exception as e  : 
                        summary = ""
                   

                    try:
                        listExperiences = browser.find_elements_by_xpath("//*[@class='pv-profile-section__card-item pv-position-entity ember-view']")
                        for x in listExperiences: 
                            experiences += x.text + "---BREAK---"
                    except Exception as e  : 
                        experiences = ""
                    education = ""
                    try : 
                        # pv-entity__summary-info
                        listEducation = browser.find_elements_by_xpath("//*[@class='pv-profile-section__sortable-card-item pv-education-entity pv-profile-section__card-item ember-view']")
                        for x in listEducation:
                            education += x.text + "---BREAK---"
                    except  Exception as e  : 
                        education = ""
                    skills = ""
                    #  Click show more skill
                    try : 
                        browser.find_element_by_xpath("//*[@class='pv-profile-section__card-action-bar pv-skills-section__additional-skills artdeco-container-card-action-bar']").click()
                    except Exception as e  :
                        print(e)
                    try:
                        listSkill = browser.find_elements_by_xpath("//*[@class='pv-skill-entity__skill-name truncate Sans-15px-black-85%-semibold inline-block ']")
                        for x in listSkill: 
                            skills += x.text + "---BREAK---"
                    except Exception as e  : 
                        skills = ""
                    langaues = ""
                    try: 
                        listLanguages = browser.find_elements_by_xpath("//*[@class='pv-profile-section accordion-panel pv-accomplishments-block languages ember-view']")
                    
                        for x in listLanguages : 
                            langaues += x.text + "---BREAK---"    
                    except Exception as e  : 
                        langaues = ""  
                    course = ""
                    try : 
                        listCourse = browser.find_elements_by_xpath("//*[@class='pv-profile-section accordion-panel pv-accomplishments-block courses ember-view']")
                        for x  in listCourse : 
                            course += x.text + "---BREAK---"  
                    except Exception as e : 
                        course = ""

                    project = ""
                    try : 
                        listProject = browser.find_elements_by_xpath("//*[@class='pv-profile-section accordion-panel pv-accomplishments-block projects ember-view']")
                        for x  in listCourse : 
                            project += x.text + "---BREAK---"  
                    except Exception as e  : 
                        project = ""

                    publication = ""
                    try : 
                        listPublication = browser.find_elements_by_xpath("//*[@class='pv-profile-section accordion-panel pv-accomplishments-block publications ember-view']")
                        for x  in listCourse : 
                            publication += x.text + "---BREAK---"  
                    except Exception as e  : 
                        publication = ""
                    try : 
                        phone = browser.find_element_by_xpath("//*[@class='pv-contact-info__list']").text
                    except Exception as e :
                        phone = ""            
                    try : 
                        email = browser.find_element_by_xpath("//*[@class='pv-contact-info__contact-link Sans-15px-black-55%']").text
                    except Exception as e : 
                        email = ""
                    try : 
                        connected_Time = browser.find_element_by_xpath("//*[@class='pv-contact-info__contact-item Sans-15px-black-55%']").text
                    except Exception as e : 
                        connected_Time = ""
                
                # ------------SAVE AS DB
                    try :
                        command = """INSERT INTO  "Linkedin_Detail" (  "Name", "Head_Line", "Company", "Schools ", "Location", "Phone", "Email", "Connected_Date", 
                        "Connection", "Sumary", "Skill", "Language", "Course", "Project", "Publication", "URL" , "Experiences",
                         "Web", "Address", "BirthDay", "IM" ,"Avatar_URL" )
                         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                        value = [name, headLine, company, education, location, phone, email , connected_Time,
                        connections, summary,  skills, langaues, course, project, publication, URL, experiences,
                        website, address, birthDay, IM , avatar ]
                        MyConnection.insertUpdateDB(command, value)
                        print("INSERT DONE !")
                    except Exception as e : 
                        print("INSERT ERROR ! " , e)
                    time.sleep(randint(5,20))
                    ## Update Crawl with linkedin URL !
                    try : 
                        command = """UPDATE "Linkedin_URL" SET "Is_Crawl" = '1' WHERE "Linkedin_URL" = %s """
                        value  = [URL]
                        MyConnection.insertUpdateDB(command, value)
                        print(" Update DONE ! ")
                    except Exception as e : 
                        print("UPDATE ERROR !  " , e)

                except Exception as e : 
                    print(e)
        except Exception as e : 
            print("ERROR ! " , e)
            browser.close()
 
if __name__=="__main__": 
    linkedin = LinkedinDetail()
    linkedin.main()

        
 
            