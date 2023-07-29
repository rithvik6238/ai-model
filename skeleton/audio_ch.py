import pyttsx3
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Initialize the text-to-speech engine
chrome_options=Options()
chrome_options.add_argument('--log-levels=3')
chrome_options.headless=True
s=Service("database\chromedriver.exe")
driver = webdriver.Chrome(service=s)
driver.maximize_window()
website="https://ttsmp3.com/text-to-speech/British%20English/"
driver.get(website)
ButtonSelection = Select(driver.find_element(by=By.XPATH,value='/html/body/div[4]/div[2]/form/select'))
ButtonSelection.select_by_visible_text('British English / Brian')

def Speak(Text):
    lengthoftext = len(str(Text))

    if lengthoftext==0:
        pass
    else:
        print("")
        print(f"jarvis : {Text}")
        print("")
        Data = str(Text)
        xpathofsec = '/html/body/div[4]/div[2]/form/textarea'
        driver.find_element(By.XPATH,value=xpathofsec).send_keys(Data)
        driver.find_element(By.XPATH,value='//*[@id="vorlesenbutton"]').click()
        driver.find_element(By.XPATH,value="/html/body/div[4]/div[2]/form/textarea").clear()

        if lengthoftext>=30:
            sleep(4)
        elif lengthoftext>=40:
            sleep(6)
        elif lengthoftext>=55:
            sleep(8)
        elif lengthoftext>=70:
            sleep(10)
        elif lengthoftext>=100:
            sleep(13)
        elif lengthoftext>=120:
            sleep(14)
        else:
            sleep(2)

Speak("hello sir")