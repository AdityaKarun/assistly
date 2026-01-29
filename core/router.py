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
from modules.courtesy_handler import handle_courtesy

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
            response = get_date_time(entities)
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
            response = search_google(entities)
            return response
        
        if intent == "youtube":
            response = youtube_player(entities)
            return response
        
        if intent == "opening_app_or_url":
            response = open_app_or_url(entities)
            return response
        
        if intent == "system_info":
            response = handle_system_info(entities)
            return response
        
        if intent == "timer":
            # Speaker is passed for real-time feedback during countdown
            response = run_timer(entities, self.speaker)
            return response
        
        if intent == "courtesy":
            response = handle_courtesy()
            return response

        if intent == "exit":
            response = "Goodbye"
            return response
        
        if intent == "unknown":
            response = "I'm not sure what you meant. Could you rephrase?"
            return response
        

if __name__ == "__main__":
    import ast
    raw_input = input("Enter intent result: ")
    intent_result = ast.literal_eval(raw_input)

    route = Router()
    functionality = route.define_route(intent_result)
    print(functionality)
