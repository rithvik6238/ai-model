# APi 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

import openai
import pyttsx3
import speech_recognition as sr
import time
import datetime

# Set your OpenAI API key
openai.api_key = "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"

# Initialize the text-to-speech engine
engine = pyttsx3.init()
now=datetime.datetime.now()

if now.hour<12 :
    print(" welcom back sir all system will be prepared in a few minutes for now feel free to grab a cup of coffee and have a good day")
    msg= " welcom back sir all system will be prepared in a few minutes for now feel free to grab a cup of coffee and have a good day" 
elif  now.hour<18:
    print("goodafternoon sir ")
    msg="goodafternoon sir "
elif now.hour<21:
    print("goodevening sir")
    msg="goodevening sir"
else :
    print("hello sir how can i help you at midnight")
    msg= "hello sir how can i help you at midnight"

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
        
        #print("Say 'jarvis' to start recording your question...")
        #speak_text("Say 'jarvis' to start recording your question...")
        print("listening")

        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower()=="shutdown":
                    break

                #if transcription.lower() == "yes":
                  #  print(" i am jarvis the virtual artificial intelligence and i am here to assist you with a variety of tasks as best i can twentyfour hours a day seven days a week importing all preferences from home interface systems are  now fully operational  ")
                   # speak_text( "now me to introduce myself i am jarvis the virtual artificial intelligence and i am here to assist you with a variety of tasks as best i can twentyfour hours a day seven days a week importing all preferences from home interface systems are  now fully operational ") 
                if transcription.lower()=="jarvis":
                    print( "yes sir how can i help you")
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
                    if text =="stop":
                        break
                    if text=="tell me about yourself":
                        print(text)
                        print(" i am jarvis the virtual artificial intelligence and i am here to assist you with a variety of tasks as best i can twentyfour hours a day seven days a week importing all preferences from home interface systems are  now fully operational  ")
                        speak_text( "now me to introduce myself i am jarvis the virtual artificial intelligence and i am here to assist you with a variety of tasks as best i can twentyfour hours a day seven days a week importing all preferences from home interface systems are  now fully operational ") 
                    elif text:
                        print(f"You said: {text}")

                        # Generate response using GPT-3
                        response = generate_response(text)
                        print(f"{response}")

                        # Read response using text-to-speech
                        speak_text(response)
            except Exception as e:
                print("An error occurred: {}".format(e))


if __name__ == "__main__":
    main()