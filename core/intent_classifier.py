import logging
import json

from core.llm_client import GeminiClient

logger = logging.getLogger(__name__)

ALLOWED_INTENTS = {
    "date_time",
    "joke",
    "location",
    "news",
    "weather",
    "search",
    "youtube",
    "opening_app_or_url",
    "system_info",
    "timer",
    "courtesy",
    "exit",
    "unknown"
}

class IntentEngine:
    def __init__(self):
        """
        Initializes the intent classification engine and LLM client.

        Args:
            None

        Returns:
            None
        """
        self.llm = GeminiClient()
        logger.debug("Intent Engine initialized")

    def classify(self, user_command):
        """
        Classifies a user command into a single intent with entities and confidence.

        Args:
            user_command (str): Raw user input from speech or text.

        Returns:
            tuple: (intent, entities, confidence) after validation and normalization.
        """

        # Strict prompt to force deterministic intent + entity + confidence output from the LLM
        prompt = f"""
            You are a precise intent classification system.
            Your ONLY job is to classify user input into predefined categories.

            USER INPUT: "{user_command}"

            ===== INTENT DEFINITIONS =====
            You must classify the input into EXACTLY ONE of these intents:

            1. "date_time" - User asks about current time, date, day, or calendar information
            
            The user may ask for specific information or all information:
            - Time only: "what time is it", "tell me the time", "current time"
            - Date only: "what's the date", "what's today's date", "tell me the date"
            - Day only: "what day is it", "what day is today", "which day"
            - Multiple/All: "what's the time and date", "tell me everything", "date and time"
            
            Extract which information type(s) the user wants:
            - If asking ONLY for time → extract "time"
            - If asking ONLY for date → extract "date"
            - If asking ONLY for day → extract "day"
            - If asking for multiple or unclear → extract all that apply or default to all three
            
            Examples:
            "what time is it" → date_time with info_type: ["time"]
            "what's the date" → date_time with info_type: ["date"]
            "what day is today" → date_time with info_type: ["day"]
            "what's the time and date" → date_time with info_type: ["time", "date"]
            "tell me the date and day" → date_time with info_type: ["date", "day"]
            "what's today" → date_time with info_type: ["date", "day"]
            "time and date please" → date_time with info_type: ["time", "date"]

            2. "joke" - User requests a joke or something funny
            Examples: "tell me a joke", "say something funny", "make me laugh"

            3. "location" - User asks about a place, address, or directions
            Examples: "where is Mumbai", "how do I get to the airport", "find nearest hospital"

            4. "news" - User requests current news, headlines, or recent events
            Examples: "what's happening", "news today", "tell me the headlines"

            5. "weather" - User asks about weather conditions, temperature, or forecast
            Examples: "what's the weather", "will it rain", "temperature in Delhi"

            6. "search" - User wants to search for information on the internet
            Examples: "search for python tutorials", "look up quantum physics", "google elon musk"

            7. "youtube" - User wants to play, search, or open something on YouTube
            Examples: "play despacito", "open youtube", "search songs on youtube"

            8. "opening_app_or_url" - User wants to open an application or website
            
            For APPS: Desktop applications, programs, software
            Examples: "open chrome", "launch calculator", "start notepad", "open terminal"
            
            For WEBSITES: Any website, social media, online service
            Examples: "open facebook", "go to google", "open reddit", "visit imdb website"
            
            KEY DISTINCTIONS:
            - "play [song]" or "search on youtube" → youtube intent
            - "open [app name]" or "launch [program]" → opening_app_or_url intent
            - "search for [topic]" → search intent
            - "go to [website]" or "open [site] website" → opening_app_or_url intent

            9. "system_info" - User asks about computer system information or status
            
            Supported Resources:
            - Battery: Battery level, charging status, power information
            - CPU: Processor usage, CPU performance
            - Memory/RAM: Memory usage, available RAM, memory status
            - Storage/Disk: Disk space, drive capacity, storage availability
            - Uptime: System uptime, how long computer has been running
            
            Examples:
            "what's my battery level" → system_info with resource: battery
            "check cpu usage" → system_info with resource: cpu
            "how much ram is free" → system_info with resource: memory
            "check disk space" → system_info with resource: storage
            "system uptime" → system_info with resource: uptime
            "how long has my computer been on" → system_info with resource: uptime
            "is my battery charging" → system_info with resource: battery
            "memory status" → system_info with resource: memory

            10. "timer" - User wants to set a timer or countdown for a specific duration
            
            Duration Conversion:
            - CRITICAL: ALWAYS convert time to SECONDS in the "duration" entity
            - Extract the numeric value and time unit, then convert to seconds
            - Supported units: seconds, minutes, hours
            - Maximum allowed: 3600 seconds (1 hour)
            
            Conversion Rules:
            - Seconds → keep as is (e.g., 30 seconds = 30)
            - Minutes → multiply by 60 (e.g., 5 minutes = 300)
            - Hours → multiply by 3600 (e.g., 1 hour = 3600)
            - Mixed units → convert each part and sum (e.g., 1 hour 30 minutes = 3600 + 1800 = 5400, but cap at 3600)
            
            Examples:
            "set a timer for 30 seconds" → timer with duration: 30
            "set timer for 5 minutes" → timer with duration: 300
            "timer for 2 mins" → timer with duration: 120
            "set a 1 hour timer" → timer with duration: 3600
            "timer for 45 seconds" → timer with duration: 45
            "set timer 10 minutes" → timer with duration: 600
            "remind me in 3 minutes" → timer with duration: 180
            "countdown 20 seconds" → timer with duration: 20
            
            If duration exceeds 3600 seconds, still classify as timer but keep duration at 3600 (max limit).
            If no duration is specified, use confidence 0.6-0.7 and omit duration entity.

            11. "courtesy" - User expresses gratitude, thanks, or polite acknowledgment
            
            This intent captures polite expressions where the user is thanking the assistant
            or acknowledging its help. These are NOT commands or requests for action.
            
            Examples:
            "thank you" → courtesy
            "thanks" → courtesy
            "thanks a lot" → courtesy
            "appreciate it" → courtesy
            "thank you so much" → courtesy
            "thanks man" → courtesy
            "cheers" → courtesy
            
            IMPORTANT DISTINCTIONS:
            - "thank you" → courtesy (just expressing gratitude)
            - "can you help me" → unknown or search (asking for help, not thanking)
            - "thanks, now search for X" → search (the thanks is incidental to the command)
            
            When classified as courtesy, no entities are needed.
            Confidence should be high (0.9+) for clear expressions of thanks.

            12. "exit" - User wants to quit, stop, or exit the application
            Examples: "exit", "quit", "stop", "close", "shutdown"

            13. "unknown" - Input doesn't match any category above, is gibberish, empty, or unclear
            Examples: "loxacvreb", "asdfgh", "", "what is love"

            ===== ENTITY EXTRACTION RULES =====
            Extract ONLY these entity types if present and relevant to the intent:

            - FOR "date_time" INTENT:
              {{"info_type": ["time", "date", "day"]}}
              
              Analyze what the user is asking for and include ONLY the relevant types:
              - "time" → when asking about current time, hours, minutes, AM/PM
              - "date" → when asking about the date, month, year, today's date
              - "day" → when asking about the day of the week (Monday, Tuesday, etc.)
              
              Rules:
              - If user asks ONLY for time → ["time"]
              - If user asks ONLY for date → ["date"]
              - If user asks ONLY for day → ["day"]
              - If user asks for "date and time" → ["time", "date"]
              - If user asks for "day and date" → ["date", "day"]
              - If user asks "what's today" or similar ambiguous queries → ["date", "day"]
              - If completely unclear what they want → ["time", "date", "day"] (all)
              
              Examples:
              "what time is it" → {{"info_type": ["time"]}}
              "tell me the time" → {{"info_type": ["time"]}}
              "what's the date today" → {{"info_type": ["date"]}}
              "what day is it" → {{"info_type": ["day"]}}
              "what day is today" → {{"info_type": ["day"]}}
              "time and date" → {{"info_type": ["time", "date"]}}
              "what's today" → {{"info_type": ["date", "day"]}}
              "tell me date and day" → {{"info_type": ["date", "day"]}}
              "what's the current time and date" → {{"info_type": ["time", "date"]}}
              "give me all time info" → {{"info_type": ["time", "date", "day"]}}

            - "location": City, country, place name (for weather, location intents)
            Example: "weather in Mumbai" → {{"location": "Mumbai"}}

            - "query": Search terms, song names, video titles (for search, youtube intents)
            Example: "search for python" → {{"query": "python"}}
            Example: "play despacito" → {{"query": "despacito"}}

            - FOR "system_info" INTENT:
              {{"resource": "resource_type"}}
              
              Map user queries to these resource types:
              - "battery" → battery status, charging, power level
              - "cpu" → CPU usage, processor performance
              - "memory" → RAM usage, memory status (also matches: "ram", "memory")
              - "storage" → disk space, drive capacity (also matches: "disk", "storage", "hard drive")
              - "uptime" → system uptime, how long computer has been running
              
              Examples:
              "what's my battery" → {{"resource": "battery"}}
              "check cpu" → {{"resource": "cpu"}}
              "how much ram do I have" → {{"resource": "memory"}}
              "check disk space" → {{"resource": "storage"}}
              "how long has my pc been on" → {{"resource": "uptime"}}
              "is battery charging" → {{"resource": "battery"}}
              "memory usage" → {{"resource": "memory"}}

            - FOR "timer" INTENT:
              {{"duration": seconds_as_integer}}
              
              CRITICAL CONVERSION RULES:
              - ALWAYS return duration in SECONDS as an integer
              - Extract the number and time unit from user input
              - Convert to seconds using these multipliers:
                * seconds/sec/s → × 1
                * minutes/mins/min/m → × 60
                * hours/hrs/hr/h → × 3600
              - Maximum value: 3600 (1 hour cap)
              - If multiple units mentioned, convert each and sum them
              
              Examples with MANDATORY conversions:
              "set timer for 30 seconds" → {{"duration": 30}}
              "timer 5 minutes" → {{"duration": 300}}  (5 × 60 = 300)
              "set a 2 minute timer" → {{"duration": 120}}  (2 × 60 = 120)
              "timer for 1 hour" → {{"duration": 3600}}  (1 × 3600 = 3600)
              "10 min timer" → {{"duration": 600}}  (10 × 60 = 600)
              "45 second timer" → {{"duration": 45}}
              "countdown 3 mins" → {{"duration": 180}}  (3 × 60 = 180)
              "remind me in 20 seconds" → {{"duration": 20}}
              "set timer 7 minutes" → {{"duration": 420}}  (7 × 60 = 420)
              
              IMPORTANT: The LLM must do the math conversion itself!
              Do NOT return "5 minutes" or "2 mins" - convert to seconds: 300, 120
              
              If no duration specified, omit the duration entity entirely.

            - FOR "opening_app_or_url" INTENT:
              
              For APPS: {{"type": "app", "name": "app_name", "executable": "windows_executable"}}
              - Intelligently identify the Windows executable name from what the user said
              - Use your knowledge of Windows OS naming conventions
              - Think: What would Windows recognize for this app?
              
              Examples:
              "open chrome" → {{"type": "app", "name": "chrome", "executable": "chrome"}}
              "launch calculator" → {{"type": "app", "name": "calculator", "executable": "calc"}}
              "start notepad" → {{"type": "app", "name": "notepad", "executable": "notepad"}}
              "open terminal" → {{"type": "app", "name": "terminal", "executable": "cmd"}}
              "launch paint" → {{"type": "app", "name": "paint", "executable": "mspaint"}}
              "open word" → {{"type": "app", "name": "word", "executable": "winword"}}
              
              For WEBSITES: {{"type": "url", "name": "site_name", "url": "complete_url"}}
              - Intelligently construct the full, working URL from what the user said
              - Use your knowledge of popular websites and their actual URLs
              - Think: What's the real URL for this site?
              
              Examples:
              "open facebook" → {{"type": "url", "name": "facebook", "url": "https://facebook.com"}}
              "go to imdb" → {{"type": "url", "name": "imdb", "url": "https://imdb.com"}}
              "visit github" → {{"type": "url", "name": "github", "url": "https://github.com"}}
              "open wikipedia" → {{"type": "url", "name": "wikipedia", "url": "https://wikipedia.org"}}
              "go to stackoverflow" → {{"type": "url", "name": "stackoverflow", "url": "https://stackoverflow.com"}}
              
              Use context clues to decide app vs url:
              - Browser/desktop software → app
              - Online services/social media → url

            DO NOT extract entities for joke, courtesy, exit, or unknown intents.
            DO NOT invent entities that aren't in the user input.

            ===== CONFIDENCE SCORING RULES =====
            Assign confidence based on clarity and specificity:

            0.95-1.0: Perfect match with specific details
            - "play Bohemian Rhapsody on YouTube" (intent + entity clear)
            - "open chrome browser" (clear app intent)
            - "check battery level" (clear system_info intent)
            - "set timer for 5 minutes" (clear timer with duration)
            - "thank you" (clear courtesy expression)
            - "what time is it" (clear date_time with specific info_type)

            0.85-0.94: Clear intent with some details
            - "play a song on YouTube" (clear intent, generic query)
            - "open facebook" (clear but could be app or url)
            - "what's my cpu" (clear intent, inferred resource)
            - "timer for 30 seconds" (clear timer intent)
            - "thanks a lot" (clear courtesy with emphasis)
            - "what's the date" (clear date_time with specific info_type)

            0.70-0.84: Clear intent, no details
            - "what's the news" (clear intent)
            - "tell me a joke" (clear intent)
            - "cheers" (courtesy, less formal)
            - "what's today" (date_time but ambiguous info_type)

            0.50-0.69: Ambiguous, could match multiple intents
            - "what's happening" (could be news or general search)
            - "show me" (unclear what to show)

            0.30-0.49: Very unclear or partially matching
            - "time weather" (conflicting intents)

            0.10-0.29: Gibberish or nonsense
            - "loxacvreb"

            0.0-0.09: Completely empty or only special characters
            - ""

            ===== OUTPUT FORMAT =====
            You MUST respond with ONLY valid JSON. No other text before or after.

            REQUIRED FORMAT:
            {{
            "intent": "one_of_the_13_intents_above",
            "entities": {{}},
            "confidence": 0.85
            }}

            ===== STRICT RULES =====
            1. Intent MUST be one of: date_time, joke, location, news, weather, search, youtube, opening_app_or_url, system_info, timer, courtesy, exit, unknown
            2. DO NOT create new intent names
            3. DO NOT add explanations or comments
            4. DO NOT use markdown code blocks (no ```json or ```)
            5. entities MUST be an object (dict), never null or array
            6. confidence MUST be a number between 0.0 and 1.0
            7. Output MUST be valid JSON that can be parsed
            8. DO NOT hallucinate entities that aren't in the user input
            9. If unsure between two intents, pick the most likely one and lower confidence
            10. Empty input = unknown intent with confidence 0.0
            11. For opening_app_or_url: ALWAYS include "type" field (either "app" or "url")
            12. For opening_app_or_url with type "app": ALWAYS include "executable" field (short name, no .exe)
            13. For opening_app_or_url with type "url": ALWAYS include full "url" field with https://
            14. For system_info: ALWAYS include "resource" field (one of: battery, cpu, memory, storage, uptime)
            15. For timer: ALWAYS include "duration" field as INTEGER in SECONDS (after conversion from minutes/hours)
            16. For timer: YOU MUST do the math conversion (e.g., 5 minutes → 300, not "5 minutes")
            17. For courtesy: NO entities needed, just high confidence for clear expressions of thanks
            18. For date_time: ALWAYS include "info_type" field as an ARRAY of strings (["time"], ["date"], ["day"], or combinations)
            19. For date_time: Analyze the user's query carefully to extract ONLY what they're asking for

            ===== EXAMPLES =====
            Input: "what's the weather in Mumbai"
            Output: {{"intent": "weather", "entities": {{"location": "Mumbai"}}, "confidence": 0.95}}

            Input: "tell me a joke"
            Output: {{"intent": "joke", "entities": {{}}, "confidence": 0.9}}

            Input: "play despacito"
            Output: {{"intent": "youtube", "entities": {{"query": "despacito"}}, "confidence": 0.92}}

            Input: "open chrome"
            Output: {{"intent": "opening_app_or_url", "entities": {{"type": "app", "name": "chrome", "executable": "chrome"}}, "confidence": 0.95}}

            Input: "open facebook website"
            Output: {{"intent": "opening_app_or_url", "entities": {{"type": "url", "name": "facebook", "url": "https://facebook.com"}}, "confidence": 0.93}}

            Input: "what's my battery level"
            Output: {{"intent": "system_info", "entities": {{"resource": "battery"}}, "confidence": 0.95}}

            Input: "check cpu usage"
            Output: {{"intent": "system_info", "entities": {{"resource": "cpu"}}, "confidence": 0.93}}

            Input: "how much ram is free"
            Output: {{"intent": "system_info", "entities": {{"resource": "memory"}}, "confidence": 0.92}}

            Input: "check disk space"
            Output: {{"intent": "system_info", "entities": {{"resource": "storage"}}, "confidence": 0.91}}

            Input: "how long has my computer been on"
            Output: {{"intent": "system_info", "entities": {{"resource": "uptime"}}, "confidence": 0.90}}

            Input: "set timer for 5 minutes"
            Output: {{"intent": "timer", "entities": {{"duration": 300}}, "confidence": 0.95}}

            Input: "timer 30 seconds"
            Output: {{"intent": "timer", "entities": {{"duration": 30}}, "confidence": 0.93}}

            Input: "set a 10 minute timer"
            Output: {{"intent": "timer", "entities": {{"duration": 600}}, "confidence": 0.94}}

            Input: "countdown 2 mins"
            Output: {{"intent": "timer", "entities": {{"duration": 120}}, "confidence": 0.91}}

            Input: "remind me in 1 hour"
            Output: {{"intent": "timer", "entities": {{"duration": 3600}}, "confidence": 0.88}}

            Input: "thank you"
            Output: {{"intent": "courtesy", "entities": {{}}, "confidence": 0.98}}

            Input: "thanks a lot"
            Output: {{"intent": "courtesy", "entities": {{}}, "confidence": 0.95}}

            Input: "appreciate it"
            Output: {{"intent": "courtesy", "entities": {{}}, "confidence": 0.93}}

            Input: "thanks for your help"
            Output: {{"intent": "courtesy", "entities": {{}}, "confidence": 0.96}}

            Input: "cheers"
            Output: {{"intent": "courtesy", "entities": {{}}, "confidence": 0.85}}

            Input: "go to imdb"
            Output: {{"intent": "opening_app_or_url", "entities": {{"type": "url", "name": "imdb", "url": "https://imdb.com"}}, "confidence": 0.91}}

            Input: "launch calculator"
            Output: {{"intent": "opening_app_or_url", "entities": {{"type": "app", "name": "calculator", "executable": "calc"}}, "confidence": 0.92}}

            Input: "open terminal"
            Output: {{"intent": "opening_app_or_url", "entities": {{"type": "app", "name": "terminal", "executable": "cmd"}}, "confidence": 0.93}}

            Input: "what time is it"
            Output: {{"intent": "date_time", "entities": {{"info_type": ["time"]}}, "confidence": 0.98}}

            Input: "what's the date"
            Output: {{"intent": "date_time", "entities": {{"info_type": ["date"]}}, "confidence": 0.97}}

            Input: "what day is today"
            Output: {{"intent": "date_time", "entities": {{"info_type": ["day"]}}, "confidence": 0.96}}

            Input: "what's the time and date"
            Output: {{"intent": "date_time", "entities": {{"info_type": ["time", "date"]}}, "confidence": 0.95}}

            Input: "tell me the date and day"
            Output: {{"intent": "date_time", "entities": {{"info_type": ["date", "day"]}}, "confidence": 0.94}}

            Input: "what's today"
            Output: {{"intent": "date_time", "entities": {{"info_type": ["date", "day"]}}, "confidence": 0.85}}

            Input: "give me all the time info"
            Output: {{"intent": "date_time", "entities": {{"info_type": ["time", "date", "day"]}}, "confidence": 0.78}}

            Input: "loxacvreb"
            Output: {{"intent": "unknown", "entities": {{}}, "confidence": 0.15}}

            Input: "what's happening in the world"
            Output: {{"intent": "news", "entities": {{}}, "confidence": 0.88}}

            Input: ""
            Output: {{"intent": "unknown", "entities": {{}}, "confidence": 0.0}}

            Now classify this input: "{user_command}"
        """
        # Send the constructed prompt to the LLM for intent classification
        raw_data = self.llm.generate(prompt)

        # Treat missing or None LLM responses and fall back safely
        if not raw_data:
            logger.warning("LLM response is missing or empty, falling back to default (unknown) intent result")
            return "unknown", {}, 0.0
        
        raw_data = raw_data.strip()
        if raw_data.startswith("```"):
            lines = raw_data.splitlines()

            # Drop opening fence (``` or ```json)
            lines = lines[1:]

            # Remove closing code fence if present
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            raw_data = "\n".join(lines).strip()

        try:
            # LLM output must be valid JSON to proceed
            data = json.loads(raw_data.strip())
            logger.debug("Parsed LLM JSON output: %s", data)


        except json.JSONDecodeError:
            logger.warning("Invalid JSON from LLM, falling back to default (unknown) intent result")
            logger.debug("Raw LLM output: %s", raw_data)
            return "unknown", {}, 0.0

        except Exception:
            # Any parsing failure is considered an unsafe response
            logger.exception("Failed to parse LLM response, falling back to default (unknown) intent result")
            logger.debug("Raw LLM output: %s", raw_data)
            return "unknown", {}, 0.0

        # Non-dict responses are treated as invalid model behavior
        if not isinstance(data, dict):
            logger.warning("LLM output is not a JSON object, falling back to default (unknown) intent result")
            return "unknown", {}, 0.0
        
        # Extract expected fields with defensive defaults
        intent = data.get("intent", "unknown")
        confidence = data.get("confidence", 0.0)
        entities = data.get("entities", {})

        # Enforce intent whitelist to prevent hallucinated labels
        if intent not in ALLOWED_INTENTS:
            logger.warning("Intent is not matching any allowed intent, falling back to default (unknown) intent result")
            return "unknown", {}, 0.0

        # Ensure entities is always a dictionary for downstream safety
        if not isinstance(entities, dict):
            entities = {}

        try:
            # Normalize confidence to a bounded float
            confidence = float(confidence)
            confidence = max(0.0, min(1.0, confidence))
        except Exception:
            logger.debug("Invalid confidence value from LLM: %s", data.get("confidence"))
            confidence = 0.0

        intent_result = intent, entities, confidence
        logger.info("Intent classified | %s", intent_result)
        return intent_result
    

if __name__ == "__main__":
    from core.logger_config import setup_logging

    setup_logging()
    user_intent = IntentEngine()

    user_command = input("Enter the command: ")
    intent_result = user_intent.classify(user_command)
