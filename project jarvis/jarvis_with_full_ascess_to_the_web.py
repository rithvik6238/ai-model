# APi 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
import asyncio
import re
from EdgeGPT import Chatbot, ConversationStyle
import pyttsx3
import speech_recognition as sr
import time
import datetime
from youtube import youtube
import openai
import datetime
import nltk
from nltk.tokenize import word_tokenize

# Set your OpenAI API key
openai.api_key = "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"

# Initialize the text-to-speech engine
engine = pyttsx3.init()
now = datetime.datetime.now()

if now.hour < 12:
    print(
        " welcom back sir all system will be prepared in a few minutes for now feel free to grab a cup of coffee and have a good day")
    msg = " welcom back sir all system will be prepared in a few minutes for now feel free to grab a cup of coffee and have a good day"
elif now.hour < 18:
    print("goodafternoon sir ")
    msg = "goodafternoon sir "
elif now.hour < 21:
    print("goodevening sir")
    msg = "goodevening sir"
else:
    print("hello sir how can i help you at midnight")
    msg = "hello sir how can i help you at midnight"

engine.say(msg)
engine.runAndWait()


def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print('Skipping unknown error')

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
        if pos.startswith('W') or pos.startswith('N') and word.lower() in ['who', 'what', 'when', 'where', 'which', 'how','price', 'current','rate', 'news','current','time']:
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




def speak_text(text):
    engine.say(text)
    engine.runAndWait()


print("Say 'jarvis' to start recording your question...")
speak_text("Say 'jarvis' to start recording your question...")


def main():
    while True:
        # Wait for user to say "jarvis"

        # print("Say 'jarvis' to start recording your question...")
        # speak_text("Say 'jarvis' to start recording your question...")
        print("listening")

        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "shutdown":
                    break

                # if transcription.lower() == "yes":
                #  print(" i am jarvis the virtual artificial intelligence and i am here to assist you with a variety of tasks as best i can twentyfour hours a day seven days a week importing all preferences from home interface systems are  now fully operational  ")
                # speak_text( "now me to introduce myself i am jarvis the virtual artificial intelligence and i am here to assist you with a variety of tasks as best i can twentyfour hours a day seven days a week importing all preferences from home interface systems are  now fully operational ")
                if transcription.lower() == "jarvis":
                    print("yes sir how can i help you")
                    speak_text("yes sir how can i help you")

                while transcription.lower() == "jarvis":

                    # Record audio
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
                        speak_text(
                            "now me to introduce myself i am jarvis the virtual artificial intelligence and i am here to assist you with a variety of tasks as best i can twentyfour hours a day seven days a week importing all preferences from home interface systems are  now fully operational ")
                    if text == "play the music":
                        print("sir name of music which you want to play")
                        speak_text("sir name of music which you want to play")
                        youtube()
                    elif text:
                        print(f"You said: {text}")
                        intent = classify_input(text)
                        knolege = is_knowledge_question(text)
                        logical = is_logical_question(text)
                        if intent=='math'and knolege == True:
                            bingre = asyncio.run(get_response(text))
                            print(bingre)
                            speak_text(bingre)
                        elif intent=='chat'and knolege==True:
                            bingre = asyncio.run(get_response(text))
                            print(bingre)
                            speak_text(bingre)

                        elif intent=='chat'or logical==True:
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


if __name__ == "__main__":
    main()