import os
import speech_recognition as sr
import pywhatkit
import datetime
import openai
import pyttsx3
import webbrowser
from configapi import Mykey


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# A function to convert speech to text
def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
        listener = sr.Recognizer()
        with sr.Microphone() as source:
            voice = listener.listen(source)
            try:
                print("Recognizing")
                listener.adjust_for_ambient_noise(source)
                command = listener.recognize_google(voice, language="en-in")
                return command
            except:
                talk('Sorry, I could not understand your speech say it again.')
                run_buddy()

chatstr = ""
def chat(command):
    global chatstr
    print(chatstr)
    openai.api_key = Mykey
    chatstr += f"User: {command}\n"
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=chatstr,
        temperature=0.7,
        max_tokens=125,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    talk(response["choices"][0]["text"])
    chatstr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

#
def ai(prompt):
    openai.api_key = Mykey
    text = f"OpenAI response for prompt: {prompt} \n *******\n\n"
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt = prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text += response["choices"][0]["text"]
    if not os.path.exists("openai"):
        os.mkdir('openai')

    with open(f"openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt","w") as f:
        f.write(text)



def run_buddy():
    talk("how can i help you")
    while True:
        print('Listening')
        command = take_command()
        print(command)
        if "play".lower() in command.lower():
            video = command.replace('play', '')
            pywhatkit.playonyt(video)
            talk('playing' + video)
            talk("can i do anything else for you")
            command = take_command()
            if "not now".lower() in command.lower():
                exit()
            else:
                run_buddy()


        elif "whatsapp message".lower() in command.lower():
            # Ask the user to speak the contact name:
                talk('Please speak the contact name:')
                contact_name = take_command()
                # Ask the user to speak the message to be sent:
                talk('Please speak  the message')
                message_text = take_command()
                if contact_name and message_text:
                    # Search for the recipient's number based on their name
                    # Adjust the contact mapping logic based on your requirements
                    contact_mapping = {
                        "myself": 'Your number'
                        # Add more contacts as needed
                    }
                    if contact_name.lower() in contact_mapping:
                        recipient_number = contact_mapping.get(contact_name)
                        pywhatkit.sendwhatmsg_instantly(phone_no=recipient_number, message=message_text)

                        talk('Message sent successfully!')
                        talk("can i do anything else for you")
                        command = take_command()
                        if "not now".lower() in command.lower():
                            exit()
                        else:
                            run_buddy()
                    else:
                        talk('sorry, contact not found')
                else:
                    talk('sorry, cannot understand your speech')

        elif "open calculator".lower() in command.lower():
            talk('Opening calculator')
            os.system(f"start D:\Windows\SysWOW64\calc.exe")
            talk("can i do anything else for you")
            command = take_command()
            if"not now".lower() in command.lower():
                exit()
            else:
                run_buddy()


        elif "search".lower() in command.lower():
            content = command.replace('search', '')
            talk(f"search results for{content}")
            webbrowser.open(content)
            talk("can i do anything else for you")
            print("listening")
            command = take_command()

            if "not now".lower() in command.lower:
                exit()
            else:
                run_buddy()

        elif "tell me the time".lower() in command.lower():
            time = datetime.datetime.now().strftime('%I:%M %p')  # %H is for 24hour %I is for 12hour %p is for AM or PM
            print(time)
            talk('Current time is' + time)

        elif "tell me the date".lower() in command.lower():
            current_date = datetime.datetime.now().strftime("%d %B, %Y")
            print(current_date)
            talk('Today is' + current_date)

        elif "using artificial intelligence".lower() in command.lower():
            ai(prompt=command)

        elif "quit".lower() in command.lower():
            exit()

        elif "reset chat".lower() in command.lower():
            chatstr = ""

        else:
            chat(command)

if __name__ == "__main__":
    run_buddy()


# install pyAudio
# install SpeechRecognition
# install openAi
# install pywhatkit
# install pytt3x
# import webbrowser