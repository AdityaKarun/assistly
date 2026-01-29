import logging
import pyttsx3

logger = logging.getLogger(__name__)

class Speech:
    def __init__(self):
        """
        Initializes speech configuration parameters.

        Args:
            None

        Returns:
            None
        """
        self.rate = 170
        logger.debug("Speech initialized")

    def speak(self, text):
        """
        Converts the given text into audible speech.

        Args:
            text (str): Text content to be spoken aloud.

        Returns:
            None
        """
        try:
            # Initialize the text-to-speech engine
            engine = pyttsx3.init()
            logger.debug("Speech engine started")

            # Set the speaking rate (words per minute)
            engine.setProperty('rate', self.rate)
            logger.debug("Speech speaking rate set to %s", self.rate)

            # Select Microsoft Zira voice if available
            voices = engine.getProperty('voices')
            for voice in voices:
                if "Zira" in voice.name:
                    engine.setProperty('voice', voice.id)
                    logger.debug("Selected speech voice: %s", voice.name)
                    break

            # Convert text to speech
            logger.info("Speaking: %s", text)
            engine.say(text)

            # Wait for the speech to complete
            engine.runAndWait()

            # Stop the engine to free up resources
            engine.stop()
            logger.debug("Speech engine stopped")            

        except Exception:
            # Fallback to console output if TTS fails
            logger.exception("Text-to-speech failed, falling back to text output")
            logger.info("TTS fallback output: %s", text)


if __name__ == "__main__":
    from core.logger_config import setup_logging

    setup_logging()
    speaker = Speech()

    phrase = input("Enter phrase: ")
    speaker.speak(phrase)
