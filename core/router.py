CONFIDENCE_THRESHOLD = 0.6

import logging

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

logger = logging.getLogger(__name__)

class Router:
    def __init__(self, speaker=None):
        """
        Initializes the router with optional speaker dependency.

        Args:
            speaker (object | None): Text-to-speech handler used by modules
                                     that require asynchronous feedback.

        Returns:
            None
        """
        self.fallback = "I'm not sure what you meant. Could you rephrase?"
        self.speaker = speaker
        logger.debug("Router initialized")

    def define_route(self, intent_result):
        """
        Routes the classified intent to the appropriate functionality module.

        Args:
            intent_result (tuple): (intent, entities, confidence) from intent classifier.

        Returns:
            str | None: Response returned by the invoked module.
        """
        intent, entities, confidence = intent_result

        # Reject low-confidence intents to avoid incorrect actions
        if confidence < CONFIDENCE_THRESHOLD:
            logger.debug(
                "Low confidence intent, no module invoked | confidence=%.2f threshold=%.2f",
                confidence,
                CONFIDENCE_THRESHOLD
            )
            response = self.fallback
            return response
        
        if intent == "date_time":
            logger.debug("get_date_time module invoked")
            response = get_date_time(entities)
            return response
        
        if intent == "joke":
            logger.debug("get_joke module invoked")
            response = get_joke()
            return response
        
        if intent == "location":
            logger.debug("get_location module invoked")
            response = get_location()
            return response

        if intent == "news":
            logger.debug("get_news module invoked")
            response = get_news()
            return response

        if intent == "weather":
            logger.debug("get_weather module invoked")
            response = get_weather(entities)
            return response

        if intent == "search":
            logger.debug("search_google module invoked")
            response = search_google(entities)
            return response
        
        if intent == "youtube":
            logger.debug("youtube_player module invoked")
            response = youtube_player(entities)
            return response
        
        if intent == "opening_app_or_url":
            logger.debug("open_app_or_url module invoked")
            response = open_app_or_url(entities)
            return response
        
        if intent == "system_info":
            logger.debug("handle_system_info module invoked")
            response = handle_system_info(entities)
            return response
        
        if intent == "timer":
            logger.debug("run_timer module invoked")

            # Speaker is passed for real-time feedback during countdown
            response = run_timer(entities, self.speaker)
            return response
        
        if intent == "courtesy":
            logger.debug("handle_courtesy module invoked")
            response = handle_courtesy()
            return response

        if intent == "exit":
            logger.debug("Intent is exit, no module invoked and assistant stops")
            response = "Goodbye"
            return response
        
        if intent == "unknown":
            logger.debug("Intent is unknown, no module invoked")
            response = self.fallback
            return response
        
        logger.debug("Unhandled intent value, falling back | intent=%s", intent)
        return self.fallback
        

if __name__ == "__main__":
    import ast

    from core.logger_config import setup_logging

    setup_logging()
    route = Router()

    raw_input = input("Enter intent result: ")
    intent_result = ast.literal_eval(raw_input)

    route.define_route(intent_result)
