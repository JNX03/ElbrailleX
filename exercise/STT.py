import speech_recognition as sr

recognizer = sr.Recognizer()

trans = {
    "เอ": "A",
    "บี": "B",
    "ซี": "C",
    "ดี": "D",
    "อี": "E",
    "เอฟ": "F",
    "จี": "G",
    "เอช": "H",
    "ไอ": "I",
    "เจ": "J",
    "เค": "K",
    "แอล": "L",
    "เอ็ม": "M",
    "เอ็น": "N",
    "โอ": "O",
    "พี": "P",
    "คิว": "Q",
    "อาร์": "R",
    "เอส": "S",
    "ที": "T",
    "ยู": "U",
    "วี": "V",
    "ดับเบิลยู": "W",
    "เอ็ก": "X",
    "วาย": "Y",
    "แซด": "Z"
}

def correction_system():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")

        while True:
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = recognizer.recognize_google(audio, language="th-TH")
                print(f"Recognized text: {text}")
                
                if text in trans:
                    return trans[text]
                else:
                    return "No corresponding English letter found."
                    
            except sr.WaitTimeoutError:
                return "Listening timed out, please speak again."
            except sr.UnknownValueError:
                return "Could not understand audio."
            except sr.RequestError as e:
                return f"Could not request results; {e}"

