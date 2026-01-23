CONFIDENCE_THRESHOLD = 0.6

from modules.date_and_time import get_date_time
from modules.joke import get_joke
from modules.location import get_location
from modules.news import get_news
from modules.search_google import search_google
from modules.weather import get_weather
from modules.youtube_player import youtube_player
from modules.open_app_or_url import open_app_or_url
from modules.system_info import handle_system_info
from modules.timer import run_timer

class Router:
    def __init__(self, speaker=None):
        """
        Initializes the router with optional speaker dependency.

        Args:
            speaker (object | None): Text-to-speech or output handler for timed responses.

        Returns:
            None
        """
        self.speaker = speaker

    def define_route(self, intent_result):
        """
        Routes the classified intent to the appropriate functionality module.

        Args:
            intent_result (tuple): (intent, entities, confidence) from intent classifier.

        Returns:
            str | None: Response text or result returned by the invoked module.
        """
        intent, entities, confidence = intent_result

        # Reject low-confidence intents to avoid incorrect actions
        if confidence < CONFIDENCE_THRESHOLD:
            response = "I'm not sure what you meant. Could you rephrase?"
            return response
        
        if intent == "date_time":
            current_time, date, day = get_date_time()
            response = (f"Its {current_time}, {day}, {date}")
            return response
        
        if intent == "joke":
            response = get_joke()
            return response
        
        if intent == "location":
            response = get_location()
            return response

        if intent == "news":
            response = get_news()
            return response

        if intent == "weather":
            response = get_weather(entities)
            return response

        if intent == "search":
            return search_google(entities)
        
        if intent == "youtube":
            return youtube_player(entities)
        
        if intent == "opening_app_or_url":
            return open_app_or_url(entities)
        
        if intent == "system_info":
            return handle_system_info(entities)
        
        if intent == "timer":
            # Speaker is passed for real-time feedback during countdown
            return run_timer(entities, self.speaker)

        if intent == "exit":
            response = "Goodbye"
            return response
        
        if intent == "unknown":
            response = "I'm not sure what you meant. Could you rephrase?"
            return response
        

if __name__ == "__main__":
    intent = input("Enter Intent: ")
    entities = input("Enter Entities: ")
    confidence = float(input("Enter Confidence (Range 0-1): "))

    intent_result = intent, entities, confidence

    route = Router()
    functionality = route.define_route(intent_result=intent_result)
    print(functionality)
