from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from Job import Job as jobModel;
from pymongo import MongoClient
import asyncio
from Job import JobDetail as jobModelDetail;

client = MongoClient("mongodb://192.168.1.118:27017")
print("Connection Successful")
mydb = client["healthcare"] 
db = mydb["jobs"]

options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')
options.add_argument('ignore-ssl-errors')
options.add_argument('disable-gpu')
options.add_argument("no-sandbox")
driver = webdriver.Chrome("C:\\driver\\chromedriver.exe", options=options)
driver.maximize_window()


def correlationCriteria(job:jobModel):
    criteria1 = db.find({"description": job.description})
    #criteria2 = db.find({"companyName": job.companyName})
    #criteria3 = db.find({"jobName": job.jobName})
    if len(list(criteria1)) == 0:
        return True
    else :
        return False



async def insertRecord(job:jobModel):
    job.details = job.details.__dict__
    db.insert_one(job.__dict__)


async def InsertDataToDb(jobs: list):
  
    for job in jobs:
        if correlationCriteria(job):
            await insertRecord(job)
arr = ["Nurse" , "Licensed Practical Nurse", "Registered Nurses" , "Certified Nurse" , "Occupational therapy" , "Medical technology", "Health information management" , "Cardiovascular perfusion technology", "Speech-language pathology"]



def runSync(val):
    try: 
        jobs = []
        counter =  0

        URL = "https://www.indeed.com/jobs?q=" + val 
        driver.get(URL)
        print("OK")

        while True :
            try:
                try:
                    privicy = driver.find_element(By.CLASS_NAME , "gnav-CookiePrivacyNoticeBanner")
                    privicy.find_element(By.CLASS_NAME , "gnav-CookiePrivacyNoticeButton").click()
                    time.sleep(2)
                except:
                    print("No Privicy")
                ve = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "mosaic-provider-jobcards")))
                time.sleep(3)
                CardsData = driver.find_element(By.ID, value="mosaic-provider-jobcards")
                UlCards =  CardsData.find_elements(By.CLASS_NAME , value="cardOutline")
                ve = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "cardOutline")))

                print("Lenght : " +  str(len(UlCards)))
                print(len(UlCards))
                time.sleep(3)
                for i in range(0 , len(UlCards)):
                    job = jobModel()
                    d = []
                    jobDetail = jobModelDetail()
                    time.sleep(5)
                    UlCards[i].click()
                    time.sleep(8)
                    try:
                        component = driver.find_element(By.CLASS_NAME , "jobsearch-JobComponent-embeddedHeader")
                        try:
                            companyImage = component.find_element(By.CLASS_NAME , "jobsearch-JobInfoHeader-logo")
                           # job.setCompanyImage(companyImage.get_attribute("src"))
                        except:
                            print("image Not Found ")
                        try:
                            jobName = component.find_element(By.CLASS_NAME , value="icl-u-xs-mb--xs").text
                           # job.setJobName(jobName)
                        except:
                            print("job name not found")
                        try:
                            jobName = component.find_element(By.CLASS_NAME , value="icl-u-xs-mb--xs").text
                           # job.setJobName(jobName)
                        except:
                            print("job name not found")
                        try:
                            a = component.find_element(By.CLASS_NAME , value="jobsearch-JobInfoHeader-subtitle")
                            b = a.find_elements(By.TAG_NAME , value="div")[-1]
                            print(b.tag_name)
                            jobLocation = b.find_element(By.TAG_NAME , value="div").text
                            jobDetail.setLocation(jobLocation)
                        except:
                            print("job location not found")
                        try:
                            a = component.find_element(By.ID , value="salaryInfoAndJobType")
                            #job.setPayrate(a.find_element(By.TAG_NAME , value= "span").text)
                        except:
                            print("job rate not found")
                        try:
                            companyNameTag = component.find_elements(By.CLASS_NAME , "jobsearch-InlineCompanyRating")[0].find_elements(By.CLASS_NAME , value="jobsearch-InlineCompanyRating-companyHeader")[-1]
                            companyName = companyNameTag.find_elements(By.TAG_NAME , "a")[0].text
                            print(companyName)
                           # job.setCompanyName(companyName)
                        except:
                            print("company not found")
                    except:
                        print("jobsearch-JobComponent-embeddedHeader not found")

                    try: 
                        dic  ={}
                        cardDetailBody = driver.find_element(By.ID , value="jobDetailsSection")
                        sections  = cardDetailBody.find_elements(By.CLASS_NAME , value="jobsearch-JobDescriptionSection-sectionItem")
                        for sect in sections:
                            dic[sect.text.splitlines()[0]] =  sect.text.splitlines()[-1]
                        
                        if "Specialties" in  dic:
                            jobDetail.specialitiesPush(dic["Specialties"])
                        #jobDetail.detail = dic
                    except:
                        print("Detail not found")
                    try:
                        cardMainBody = driver.find_element(By.CLASS_NAME , "jobsearch-JobComponent-embeddedBody")
                        try:
                            jobType = cardMainBody.find_elements(By.CLASS_NAME , "jobsearch-JobDescriptionSection-sectionItem")[-1].find_elements(By.TAG_NAME , "div")[-1].text
                            job.setJobType(jobType)
                        except:
                            print("Job type not found")
                        try:
                            discriptionUl =cardMainBody.find_element(By.ID , "jobDescriptionText").find_elements(By.TAG_NAME , "ul")
                            for dis in discriptionUl:
                                job.setDescription(dis.text)
                        except:
                            print("card body not found")
                    except:
                        print("job search body not found")
                    job.setJobDetail(jobDetail)
                    print(job.__dict__)
                    jobs.append(job)
                time.sleep(3)
                counter = counter + 1
                if counter >= 200:
                    asyncio.run(InsertDataToDb(jobs))
                    time.sleep(5)
                    driver.quit()
                    break
                try:
                    newPage = driver.find_element(By.CLASS_NAME , "css-jbuxu0").find_elements(By.CLASS_NAME , "css-tvvxwd")[-1].find_element(By.TAG_NAME , "a").get_attribute("href")    
                    URL = newPage
                    driver.get(URL)
                    time.sleep(8)
                    try:
                        driver.find_element(By.CLASS_NAME , "icl-Modal-guts").find_element(By.CLASS_NAME , "icl-CloseButton").click()
                        time.sleep(10)
                    except:
                        print("close failed")
                except:
                    time.sleep(4)
                    asyncio.run(InsertDataToDb(jobs))
                    time.sleep(5)
                    driver.quit()
                    break
            except Exception as ex:
                    print(str(ex))
                    asyncio.run(InsertDataToDb(jobs))
                    time.sleep(5)
                    driver.quit()
                    break
    except Exception as ex:
        print("Conection Lost" + str(ex))
        driver.quit()

 

asyncio.run(runSync(arr[0]))






