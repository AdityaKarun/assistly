import logging
import speech_recognition

logger = logging.getLogger(__name__)

class Recognizer:
    def __init__(self):
        """
        Initializes the speech recognition engine.

        Args:
            None

        Returns:
            None
        """
        self.recognizer = speech_recognition.Recognizer()
        logger.debug("Recognizer initialized")

    def recognize_command(self):
        """
        Listens to microphone input and converts spoken speech to text.

        Args:
            None

        Returns:
            str | None: Recognized command in lowercase, or None if recognition fails.
        """

        # Acquire microphone input as the audio source
        with speech_recognition.Microphone() as source:
            logger.info("Listening...")

            # Adjust for ambient noise to improve recognition accuracy
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            logger.debug("Ambience noise adjusted")
            
            # Listen for user's voice input
            audio = self.recognizer.listen(source)
            logger.debug("Audio captured from microphone")

        try:
            # Use Google's speech recognition backend for transcription
            command = self.recognizer.recognize_google(audio)
            command = command.lower()
            logger.info("Recognized command: %s", command)

            return command

        except speech_recognition.UnknownValueError:
            # Expected, common, non-fatal
            logger.warning("Speech could not be understood")
            return None
        
        except Exception:
            # Unexpected, real bug
            logger.exception("Unexpected error during speech recognition")
            return None


if __name__ == "__main__":
    from core.logger_config import setup_logging

    setup_logging()
    recognizer_object = Recognizer()
    
    while True:
        input("Hit enter to listen (Ctrl+C to exit)")
        recognizer_object.recognize_command()
