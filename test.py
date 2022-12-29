from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

from Job import Job as jobModel;
from pymongo import MongoClient
import asyncio
#from webdriver_manager.chrome import ChromeDriverManager
from msedge.selenium_tools import Edge, EdgeOptions
from Job import JobDetail as jobModelDetail;
from webdriver_manager.microsoft import EdgeChromiumDriverManager

options = EdgeOptions()

options.add_argument('ignore-certificate-errors')
options.add_argument('ignore-ssl-errors')
options.use_chromium = True
options.add_argument('disable-gpu')
options.add_argument("no-sandbox")
options.add_argument("disable-dev-shm-usage")

# chrome_driver_path = Service(options=options)
driver = Edge(executable_path= EdgeChromiumDriverManager().install(), options=options)


driver.get("https://fsm.stafferlink.com/")