import openai
import pyttsx3
import speech_recognition as sr
import time
from time import sleep
import datetime
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from googletrans import Translator
import os
import openai
from dotenv import load_dotenv
openai.api_key = "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"
load_dotenv()
completion = openai.Completion()

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))


# Initialize the text-to-speech engine
engine = pyttsx3.init()
now = datetime.datetime.now()

# Initialize the text-to-speech engine
chrome_options = Options()
chrome_options.add_argument('--log-levels=3')
chrome_options.headless = True
s = Service("database\chromedriver.exe")
driver = webdriver.Chrome(service=s)
driver.maximize_window()
website = "https://ttsmp3.com/text-to-speech/British%20English/"
driver.get(website)
ButtonSelection = Select(driver.find_element(by=By.XPATH , value='/html/body/div[4]/div[2]/form/select'))
ButtonSelection.select_by_visible_text('British English / Brian')

    #function to make response audio to jarvis audio
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


if now.hour < 12:
    print(
        " welcom back sir all system will be prepared in a few minutes for now feel free to grab a cup of coffee and have a good day")
    playsound(r'D:\AI\database\Audio voice\morning greet.mp3')
    sleep(1)
elif now.hour < 18:
    print("goodafternoon sir ")
    playsound(r'D:\AI\database\Audio voice\afternoon.mp3')
    sleep(1)
elif now.hour < 21:
    print("goodevening sir")
    playsound(r'D:\AI\database\Audio voice\evening.mp3')
    sleep(1)
else:
    print("hello sir how can i help you at midnight")
    playsound(r'D:\AI\database\Audio voice\midnight greeting.mp3')
    sleep(1)


def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print('Skipping unknown error')
def Malayalam_audio_to_eng(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        li= recognizer.recognize_google(audio,language="ml")
        line= str(li)
        translate = Translator()
        result = translate.translate(line)
        data = result.text
        print(f"You : {data}.")
        return data
    except:
        print('Skipping unknown error')


def generate_response(question,chat_log= None):

    filelog = open(r"D:\AI\brain\chat\chat_log.txt" ,"r")
    chat_log_temp = filelog.read()
    filelog.close()
    if chat_log is None:
        chat_log= chat_log_temp
    prompt = f'{chat_log}You : {question}\nJarvis : '
    response = completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=3400,
            top_p=0.3,
            frequency_penalty=0.5,
            presence_penalty=0)
    answer = response.choices[0].text.strip()
    chat_log_temp_update = chat_log_temp + f"\nYou : {question} \nJarvis : {answer}"
    filelog = open(r"D:\AI\brain\chat\chat_log.txt", "w")
    filelog.write(chat_log_temp_update)
    filelog.close()
    return answer



'''def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]'''

#offline audio
'''def speak_text(text):
    engine.say(text)
    engine.runAndWait()'''


print("Say 'jarvis' to start recording your question...")
playsound(r'D:\AI\database\Audio voice\rcd ques.mp3')


def main():
    while True:

        print("listening")


        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "shutdown":
                    break

                if transcription.lower() == "jarvis":
                    print("yes sir how can i help you")
                    playsound(r'D:\AI\database\Audio voice\help audio.mp3')
                    sleep(1)
                    print("select your prefered language sir english or malayalam")
                    playsound(r'D:\AI\database\Audio voice\lang req.mp3')
                    sleep(1)
                    while True:
                        print("listening")
                        with sr.Microphone() as source:
                            recognizer = sr.Recognizer()
                            audio = recognizer.listen(source)

                            try:
                                transcription = recognizer.recognize_google(audio)
                                if transcription.lower()=="shutdown":
                                    break
                                if transcription.lower() =="english":
                                    while True:
                                        filename = "input.wav"
                                        print("ask  question...")
                                        with sr.Microphone() as source:
                                            recognizer = sr.Recognizer()
                                            source.pause_threshold = 1
                                            audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                                            with open(filename, "wb") as f:
                                                f.write(audio.get_wav_data())
                                        # Transcribe audio to text
                                        text = transcribe_audio_to_text(filename)
                                        if text == "stop":
                                            break
                                        if text == "tell me about yourself":
                                            print(text)
                                            print(
                                                " i am jarvis the virtual artificial intelligence and i am here to assist you with a variety of tasks as best i can twentyfour hours a day seven days a week importing all preferences from home interface systems are  now fully operational  ")
                                            playsound(r'D:\AI\database\Audio voice\intro jarvis.mp3')
                                        elif text:
                                            print(f"You said: {text}")

                                            # Generate response using GPT-3
                                            response = generate_response(text)
                                            print(f"{response}")

                                            # Read response using text-to-speech
                                            Speak(response)
                                if transcription.lower()=="malayalam":
                                    try:
                                        while True:
                                            filename = "input.wav"
                                            print("ask  question...")

                                            with sr.Microphone() as source:
                                                recognizer = sr.Recognizer()
                                                source.pause_threshold = 1
                                                audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                                                with open(filename, "wb") as f:
                                                    f.write(audio.get_wav_data())

                                            # Transcribe audio to text
                                            text = Malayalam_audio_to_eng(filename)
                                            if text == "stop":
                                                break
                                            if text == "tell me about yourself":
                                                print(text)
                                                print(
                                                    " i am jarvis the virtual artificial intelligence and i am here to assist you with a variety of tasks as best i can twentyfour hours a day seven days a week importing all preferences from home interface systems are  now fully operational  ")
                                                playsound(r'D:\AI\database\Audio voice\intro jarvis.mp3')
                                            elif text:
                                                print(f"You said: {text}")

                                                # Generate response using GPT-3
                                                response = generate_response(text)
                                                print(f"{response}")

                                                # Read response using text-to-speech
                                                Speak(response)
                                    except Exception as e:
                                        print("An error occurred: {}".format(e))





                            except Exception as e:
                                print("An error occurred: {}".format(e))
            except Exception as e:
                print("An error occurred: {}".format(e))


if __name__ == "__main__":
    main()