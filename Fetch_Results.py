import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
from termcolor import colored

TIME_TIMEOUT = 20 # Twenty-second timeout default
import getpass
import time

# Hardcode the registration, password and sem (Comment out the lines from 20-22)

# registration = 
# password = 
# sem = 

# Credentials for login and semester
registration = input('Enter your registration number: ');
password = getpass.getpass("Password:")
sem = int(input('Enter the semester: '))

# start a browser session
chromeOptions = webdriver.ChromeOptions()
prefs={"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096 }
chromeOptions.add_experimental_option('prefs', prefs)
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--window-size=1920,1080")
browser = webdriver.Chrome(chrome_options=chromeOptions)

# open link in browser
browser.get('https://academics.mnnit.ac.in/new/')

browser.find_element_by_xpath("//li[@onclick=\"openLoginModal();\"]").click()
# sleep function to let web components load in case of slow internet connnection
time.sleep(1)

# login
nameElem = WebDriverWait(browser, TIME_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//input[@id='id_regno']")))

nameElem.send_keys(registration)

passElem = browser.find_element_by_id('id_password')
passElem.send_keys(password)

browser.find_element_by_xpath("//input[@class=\"btn btn-default btn-login\"]").click()

# open result page
browser.find_element_by_xpath("//a[@href=\"/new/result\"]").click()

final_page = browser.page_source

browser.quit()

final_soup = BeautifulSoup(final_page,"html5lib")

details = final_soup.findAll(id = "info_student")
new_details = details[0].div.div
topi = new_details.findAll('span')

#Find out the semester in the scraped result 
given_sem =topi[8].text
given_sem = int(given_sem[11])

if given_sem!=sem:
	print(colored("Result not declared yet!!!","blue",attrs=['bold']))
	sys.exit(0)

#Print out the details and SPI
i=0
k=1
while i<len(topi)-1:
	print(topi[i].text.ljust(40),end='\t')
	if k%2==0:
		print('')
	k=k+1
	i=i+2


#Scrap out the final result
table = final_soup.findAll(id = "user_result")

mod_table = table[0].div.table

headings = mod_table.thead.tr.findAll('th')
headers=[]
for i in range(len(headings)):
	headers.append(headings[i].text)

print(end='\t')
for i in range(len(headers)):
	print(colored(headers[i],"blue",attrs=['bold']),end='\t\t\t')

print(colored('\n----------------------------------------------------------------------------------------------\n',"blue"))

Code=[]
Course=[]
Credit=[]
Grade=[]

final_result = mod_table.tbody.findAll('tr')

for i in range(len(final_result)):
	total = final_result[i].findAll('td')
	Code.append(total[0].text)
	Course.append(total[1].text)
	Credit.append(total[2].text)
	Grade.append(total[3].text)

for i in range(len(Code)):
	print(colored('\t'+Code[i],"green"),end='\t\t')
	print(colored(Course[i].ljust(40),"cyan"),end='')
	print(colored(Credit[i].ljust(26),"magenta"),end='')
	print(colored(Grade[i],"blue"),end='\n')