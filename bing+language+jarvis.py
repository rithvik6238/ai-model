import os
import re
import nltk
import openai
import asyncio
import pyttsx3
import datetime
import time
from time import sleep
from playsound import playsound
from googletrans import Translator
from EdgeGPT import Chatbot, ConversationStyle
import speech_recognition as sr
from youtube import youtube



from nltk.tokenize import word_tokenize

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
def speak_text(text):
    engine.say(text)
    engine.runAndWait()




if now.hour < 12:
    print(
        " welcom back sir all system will be prepared in a few minutes for now feel free to grab a cup of coffee and have a good day")
    speak_text(" welcom back sir all system will be prepared in a few minutes for now feel free to grab a cup of coffee and have a good day")


elif now.hour < 18:
    print("goodafternoon sir ")
    speak_text("goodafternoon sir ")
elif now.hour < 21:
    print("goodevening sir")
    speak_text("goodafternoon sir ")

else:
    print("hello sir how can i help you at midnight")
    speak_text("hello sir how can i help you at midnight")




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

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]


'''def generate_response(question,chat_log= None):

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
            max_tokens=60,
            top_p=0.3,
            frequency_penalty=0.5,
            presence_penalty=0)
    answer = response.choices[0].text.strip()
    chat_log_temp_update = chat_log_temp + f"\nYou : {question} \nJarvis : {answer}"
    filelog = open(r"D:\AI\brain\chat\chat_log.txt", "w")
    filelog.write(chat_log_temp_update)
    filelog.close()
    return answer'''


async def get_response(input_text):
    # Check if input has the word "jarvis"
    if "jarvis" in input_text.lower():
        # Remove the word "jarvis" from input
        input_text = input_text.lower().replace("jarvis", "").strip()

    # Call the get_bot_response() function with the remaining input text
    bot_response = await get_bot_response(input_text)

    # Check if bot response starts with "hello" or "hai" and contains the word "Microsoft"
    if re.match(r"^(hello|hai|hi|hey)", bot_response.lower()) and "microsoft" in bot_response.lower():
        # Remove the word "Microsoft" from the bot response
        bot_response = bot_response.lower().replace("microsoft", "").strip()

    # Replace the word "bing" with "jarvis" in the bot response
    bot_response = bot_response.replace("Bing", "Jarvis")
    bot_response = bot_response.replace("bing", "Jarvis")

    return bot_response


def classify_input(input):
    words = word_tokenize(input)
    pos_tags = nltk.pos_tag(words)
    intent = None
    for word, tag in pos_tags:
        if tag.startswith('VB'):
            intent = 'chat'
        elif tag == 'CD' or tag == 'NN' or tag == 'NNS':
            intent = 'math'
        elif tag == 'JJ' or tag == 'JJR' or tag == 'JJS':
            intent = 'general'
    return intent

def is_knowledge_question(prompt):
    # Use nltk to determine if prompt is a knowledge-based question
    tokens = nltk.word_tokenize(prompt)
    tagged = nltk.pos_tag(tokens)
    for word, pos in tagged:
        if pos.startswith('W') or pos.startswith('N') and word.lower() in ['who', 'what', 'when', 'where', 'which', 'how','price', 'current','rate', 'news','current','time','Amritapuri website','Amrita Vishwa Vidyapeetham','Amrita''amrita']:
            return True
    return False

def is_logical_question(prompt):
    # Use nltk to determine if prompt is a logic-based question
    tokens = nltk.word_tokenize(prompt)
    tagged = nltk.pos_tag(tokens)
    for word, pos in tagged:
        if pos.startswith('N') and word.lower() in ['maths', 'math', 'mathematics', 'logic', 'programming', 'code',
                                                    'writing', 'language', 'program','create','make','give','define',]:
            return True
    return False
async def get_bot_response(user_input):
    bot = Chatbot(cookiePath='D:\AI\database\cookies.json')
    response = await bot.ask(prompt=user_input, conversation_style=ConversationStyle.precise)
    for message in response["item"]["messages"]:
        if message["author"] == "bot":
            bot_response = message["text"]

    bot_response = re.sub('\[\^\d+\^\]', '', bot_response)
    # Select only the bot response from the response dictionary
    for message in response["item"]["messages"]:
        if message["author"] == "bot":
            bot_response = message["text"]
    # Remove [^#^] citations in response
    bot_response = re.sub('\[\^\d+\^\]', '', bot_response)

    return bot_response
'''def youtube():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say 'music name' ")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print(f"You said: {command}")
        if command == command:
            music_name = command
            pywhatkit.playonyt(music_name)
        else:
            print("Command not recognized. Please try again.")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))'''



#offline audio



print("Say 'jarvis' to start recording your question...")
speak_text("Say 'jarvis' to start recording your question...")


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
                    speak_text("yes sir how can i help you")

                    print("select your prefered language sir english or malayalam")
                    speak_text("select your prefered language sir english or malayalam")

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
                                    print("your prefered language is english")
                                    speak_text("your prefered language is english")
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
                                        if text == "play the music":
                                            print("sir which music you want to be play")
                                            speak_text("sir which music you want to be play")
                                            youtube()
                                        elif text:
                                            print(f"You said: {text}")
                                            intent = classify_input(text)
                                            knolege = is_knowledge_question(text)
                                            logical = is_logical_question(text)
                                            if intent == 'math' and knolege == True:
                                                bingre = asyncio.run(get_response(text))
                                                print(bingre)
                                                speak_text(bingre)
                                            elif intent == 'chat' and knolege == True:
                                                bingre = asyncio.run(get_response(text))
                                                print(bingre)
                                                speak_text(bingre)

                                            elif intent == 'chat' or logical == True:
                                                response = generate_response(text)
                                                print(f"{response}")

                                                # Read response using text-to-speech
                                                speak_text(response)


                                            else:
                                                # Generate response using GPT-3
                                                response = generate_response(text)
                                                print(f"{response}")

                                                # Read response using text-to-speech
                                                speak_text(response)
                                if transcription.lower()=="malayalam":
                                    print("your prefered language is malayalam")
                                    speak_text("your prefered language is malayalam")
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
                                            if text == "Stopped":
                                                break
                                            if text == "tell me about yourself":
                                                print(text)
                                                print(
                                                    " i am jarvis the virtual artificial intelligence and i am here to assist you with a variety of tasks as best i can twentyfour hours a day seven days a week importing all preferences from home interface systems are  now fully operational  ")
                                                playsound(r'D:\AI\database\Audio voice\intro jarvis.mp3')
                                            if text == "play the music":
                                                print("sir which music you want to be play")
                                                speak_text("sir which music you want to be play")
                                                youtube()
                                            elif text:
                                                print(f"You said: {text}")
                                                intent = classify_input(text)
                                                knolege = is_knowledge_question(text)
                                                logical = is_logical_question(text)
                                                if intent == 'math' and knolege == True:
                                                    bingre = asyncio.run(get_response(text))
                                                    print(bingre)
                                                    speak_text(bingre)
                                                elif intent == 'chat' and knolege == True:
                                                    bingre = asyncio.run(get_response(text))
                                                    print(bingre)
                                                    speak_text(bingre)

                                                elif intent == 'chat' or logical == True:
                                                    response = generate_response(text)
                                                    print(f"{response}")

                                                    # Read response using text-to-speech
                                                    speak_text(response)


                                                else:
                                                    # Generate response using GPT-3
                                                    response = generate_response(text)
                                                    print(f"{response}")

                                                    # Read response using text-to-speech
                                                    speak_text(response)

                                    except Exception as e:
                                        print("An error occurred: {}".format(e))





                            except Exception as e:
                                print("An error occurred: {}".format(e))
            except Exception as e:
                print("An error occurred: {}".format(e))


if __name__ == "__main__":
    main()