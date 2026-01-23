from core.recognizer import Recognizer
from core.speech import Speech
from core.intent_classifier import IntentEngine
from core.router import Router

from modules.greet import greet

if __name__ == "__main__":
    greeting = greet()

    recognizer = Recognizer()
    speaker = Speech()
    intent = IntentEngine()
    route = Router(speaker)

    speaker.speak(greeting)

    while True:
        command = recognizer.recognize_command()

        # Skip processing if speech recognition failed
        if not command:
            print("Sorry, didn't catch that.")
            continue

        print(command)

        intent_result = intent.classify(user_command=command)
        response = route.define_route(intent_result=intent_result)

        speaker.speak(response)

        # Exit loop when explicit termination intent is returned
        if response == "Goodbye":
            break
