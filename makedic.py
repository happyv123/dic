import docx, random
import time
from docx.enum.text import WD_BREAK
from docx.shared import Pt
from progress.bar import IncrementalBar
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-logging')
options.add_argument('--disable-extensions')
options.add_argument('--log-level=3')
options.add_argument('--disable-in-process-stack-traces')
options.add_argument('--ignore-certificate-errors')

s = Service('chromedriver.exe')
driver = webdriver.Chrome(options=options, service=s)

URL_TEMPLATE = "https://dictionary.cambridge.org/ru/%D1%81%D0%BB%D0%BE%D0%B2%D0%B0%D1%80%D1%8C/%D0%B0%D0%BD%D0%B3%D0%BB%D0%BE-%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9/"

mydoc = docx.Document()
style = mydoc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)

used = []

with open('wordlist.txt', 'r') as f:
    wordlist = f.readlines()
    bar = IncrementalBar('Countdown', max=70)
    errorword = 0
    for i in range(1, 71):
        word = random.choice(wordlist)
        while word in used:
            word = random.choice(wordlist)

        used.append(word)
        word = word.replace("\n", "")
        driver.get(URL_TEMPLATE + word)
        try:
            word_def = driver.find_element(By.XPATH, value="//div[@class='def ddef_d db']")
            current_par = mydoc.add_paragraph()
            bold_word = current_par.add_run(str(i) + "." + word)
            bold_word.bold = True
            italic_def = current_par.add_run(' - ' + word_def.text).add_break(WD_BREAK.LINE)
            example = driver.find_element(By.XPATH, value="//div[@class='examp dexamp']")
            italic_example = current_par.add_run(example.text)
            italic_example.italic = True
        except Exception as e:
            errorword += 1
            print('Error. Word: ' + word)
        mydoc.save('dic.docx')
        bar.next()
        time.sleep(1)
bar.finish()
driver.close()

print("Words with errors: ", errorword)
print("Check the docx file for errors!!!")