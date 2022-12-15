from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

from Job import Job as jobModel;

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
chrome_driver_path = Service(
    "C:\\Users\\Bluezorro\\Downloads\\chromedriver_win32\\chromedriver.exe")
driver = webdriver.Chrome(service=chrome_driver_path, options=options)




def writeExcel(Jobs: list):
    array = [['Job Name', 'Company Name', 'Job Type' , "Company Image" , "Discription"]]
    for job in jobs:
        array.append([job.jobName,
        job.companyName,
        job.jobType,
        job.companyImage,
        job.discription])
    df = pd.DataFrame(array)
    df.to_excel(excel_writer = "data.xlsx")

jobs = []
counter =  0

URL = "https://pk.indeed.com/jobs?q=&fromage=1&l=Karachi"
driver.get(URL)

while True :
    try:
        CardsData = driver.find_element(By.ID, value="mosaic-provider-jobcards")
        UlCards =  CardsData.find_elements(By.CLASS_NAME , value="cardOutline")
        print("Lenght : " +  str(len(UlCards)))
        print(len(UlCards))
        time.sleep(1)
        for i in range(0 , len(UlCards)):
            job = jobModel()
            
            UlCards[i].click()
            time.sleep(2)
            try:
                component = driver.find_element(By.CLASS_NAME , "jobsearch-JobComponent-embeddedHeader")
                try:
                    companyImage = component.find_element(By.CLASS_NAME , "jobsearch-JobInfoHeader-logo")
                    job.setCompanyImage(companyImage.get_attribute("src"))
                except:
                    print("image Not Found ")
                try:
                    jobName = component.find_element(By.CLASS_NAME , value="icl-u-xs-mb--xs").text
                    job.setJobName(jobName)
                except:
                    print("job name not found")
                try:
                    companyNameTag = component.find_elements(By.CLASS_NAME , "jobsearch-InlineCompanyRating")[0].find_elements(By.CLASS_NAME , value="jobsearch-InlineCompanyRating-companyHeader")[-1]
                    companyName = companyNameTag.find_elements(By.TAG_NAME , "a")[0].text
                    print(companyName)
                    job.setCompanyName(companyName)
                except:
                    print("company not found")
            except:
                print("jobsearch-JobComponent-embeddedHeader not found")
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
                        job.setDiscription(dis.text)
                except:
                    print("card body not found")
            except:
                print("job search body not found")
            jobs.append(job)
        time.sleep(3)
        if counter == 100:
            writeExcel(jobs)
            break
        counter +=1
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
            writeExcel(jobs)
            break
    except:
            writeExcel(jobs)
            break


       
    


