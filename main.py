import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


options = Options()
options.add_argument('--headless')

s = Service('chromedriver.exe')
driver = webdriver.Chrome(service=s, options=options)

URL_TEMPLATE = "https://www.englishdom.com/skills/glossary/wordset/top-100-slov-urovnya-advanced/"
driver.get(URL_TEMPLATE)
time.sleep(5)
wordlist = driver.find_elements(By.XPATH, value="//p[@class='word']")

with open('wordlist.txt', 'a') as f:
    for i in wordlist:
        f.write(i.text)
        f.write('\n')

driver.close()