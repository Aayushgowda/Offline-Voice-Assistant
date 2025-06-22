import queue
import sounddevice as sd
import vosk
import json
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext


engine = pyttsx3.init()
engine.setProperty('rate', 160)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


qa_dict = {
    "what is your name": "I am your offline voice assistant.",
    "who made you": "ayush made me.",
    "who is your creator": "ayush is my creater.",
    "what is python": "Python is a popular programming language.",
    "what is ai": "AI stands for artificial intelligence.",
    "how are you": "I am doing great.",
    "what can you do": "I can answer questions completely offline.",
    "who is the prime minister of india": "Narendra Modi is the current Prime Minister of India.",
    "what is our country name": "india is our country",
     "what is the capital of india": "New Delhi",
    "who is the president of india": "Droupadi Murmu",
    "who is the prime minister of india": "Narendra Modi",
    "what is the capital of france": "Paris",
    "what is the capital of the united states": "Washington, D.C.",
    "who discovered gravity": "Sir Isaac Newton",
    "which planet is known as the red planet": "Mars",
    "how many continents are there": "Seven",
    "how many planets are there in the solar system": "Eight",
    "what is the largest ocean": "Pacific Ocean",
    "which is the smallest country in the world": "Vatican City",
    "which is the largest country in the world": "Russia",
    "which is the most populated country": "China",
    "what is the speed of light": "Approximately 299,792 kilometers per second",
    "who wrote the national anthem of india": "Rabindranath Tagore",
    "what is the national animal of india": "Bengal Tiger",
    "what is the national bird of india": "Indian Peacock",
    "what is the national flower of india": "Lotus",
    "what is the national fruit of india": "Mango",
    "which river is the longest in the world": "The Nile River",
    "which river is the longest in india": "The Ganga",
    "what is the capital of japan": "Tokyo",
    "what is the capital of australia": "Canberra",
    "who invented the telephone": "Alexander Graham Bell",
    "who is known as the father of the nation": "Mahatma Gandhi",
    "who is the founder of microsoft": "Bill Gates",
    "who is the founder of facebook": "Mark Zuckerberg",
    "who is the founder of tesla": "Elon Musk",
    "which planet is closest to the sun": "Mercury",
    "which is the hottest planet in the solar system": "Venus",
    "which planet has rings": "Saturn",
    "how many states are there in india": "28",
    "what is the currency of japan": "Yen",
    "what is the currency of usa": "Dollar",
    "what is the square root of 64": "8",
    "how many bones are there in the human body": "206",
    "how many colors are there in a rainbow": "Seven",
    "which animal is known as the ship of the desert": "Camel",
    "which animal is known as the king of jungle": "Lion",
    "what is the largest mammal": "Blue Whale",
    "what is the tallest mountain in the world": "Mount Everest",
    "which country is known as the land of rising sun": "Japan",
    "who invented the computer": "Charles Babbage",
    "what is the full form of wifi": "Wireless Fidelity",
    "what is the full form of sim": "Subscriber Identity Module",
    "what is the full form of cp you": "Central Processing Unit",
    "what is the full form of atm": "Automated Teller Machine",
    "which bird can fly backwards": "Hummingbird",
    "which gas do plants absorb": "Carbon Dioxide",
    "which vitamin is gained from sunlight": "Vitamin D",
    "how many players in a cricket team": "11",
    "how many players in a football team": "11",
    "how many days in a year": "365",
    "how many hours in a day": "24",
    "which month has 28 or 29 days": "February",
    "what is the freezing point of water": "0 degrees Celsius",
    "what is the boiling point of water": "100 degrees Celsius",
    "which is the national sport of india": "Hockey",
    "what is the largest desert in the world": "Sahara Desert",
    "which is the biggest island in the world": "Greenland",
    "who wrote the ramayana": "Valmiki",
    "who wrote the mahabharata": "Vyasa",
    "what is the capital of china": "Beijing",
    "what is the capital of russia": "Moscow",
    "who is the ceo of google": "Sundar Pichai",
    "who is the ceo of apple": "Tim Cook",
    "what is the national flag of india called": "Tiranga",
    "which festival is known as the festival of lights": "Diwali",
    "which festival is known as the festival of colors": "Holi",
    "which is the largest continent": "Asia",
    "which is the smallest continent": "Australia",
    "how many teeth does an adult human have": "32",
    "what is the main gas in the air we breathe": "Nitrogen",
    "which metal is liquid at room temperature": "Mercury",
    "which country gifted the statue of liberty to usa": "France",
    "how many legs does a spider have": "8",
    "how many hearts does an octopus have": "3",
    "which is the fastest land animal": "Cheetah",
    "which bird lays the largest eggs": "Ostrich",
    "which is the largest internal organ in human body": "Liver",
    "which instrument is used to measure temperature": "Thermometer",
    "who was the first man to walk on the moon": "Neil Armstrong",
    "what is the main source of energy on earth": "The Sun",
    "what is photosynthesis": "The process by which green plants make their food using sunlight",
    "what is the largest bone in the human body": "Femur",
    "which organ purifies blood in humans": "Kidney",
    "what is the name of our galaxy": "Milky Way",
    "which is the hardest natural substance": "Diamond",
    "who invented electricity": "Benjamin Franklin",
    "what does dna stand for": "Deoxyribonucleic Acid",
    "which is the coldest place on earth": "Antarctica",
    "what is the name of india's first satellite": "Aryabhata",
    "which country is known as the land of thousand lakes": "Finland",
    "who is the current chief minister of karnataka": "Siddaramaiah",
    "how many spokes in the ashok chakra": "24",
    "how many states and union territories in india": "28 states and 8 union territories",
    "who composed the indian national song": "Bankim Chandra Chatterjee",
    "which is the first university in the world": "Takshashila University",
}



model = vosk.Model("model")
q = queue.Queue()


def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def talk(text):
    response_box.insert(tk.END, "Assistant: " + text + "\n")
    engine.say(text)
    engine.runAndWait()


def listen():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        response_box.insert(tk.END, "Listening (offline)...\n")
        response_box.see(tk.END)
        root.update()

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    return text


def run_assistant():
    command = listen()
    response_box.insert(tk.END, "You said: " + command + "\n")

    if command in qa_dict:
        talk(qa_dict[command])
    elif "exit" in command or "stop" in command:
        talk("Goodbye!")
        root.destroy()
    else:
        talk("Sorry, I didn't get that.")


root = tk.Tk()
root.title("Offline Voice Assistant")
root.geometry("500x400")

title_label = tk.Label(root, text="Ayush's Voice Assistant", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

response_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
response_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

start_button = tk.Button(root, text="Start Listening", font=("Arial", 14), bg="green", fg="white", command=run_assistant)
start_button.pack(pady=10)

root.mainloop()
