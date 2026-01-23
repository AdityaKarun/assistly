import pyttsx3

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

            # Set the speaking rate (words per minute)
            engine.setProperty('rate', self.rate)

            # Select Microsoft Zira voice if available
            voices = engine.getProperty('voices')
            for voice in voices:
                if "Zira" in voice.name:
                    engine.setProperty('voice', voice.id)
                    break

            # Print the text for visual feedback
            print(text)

            # Convert text to speech
            engine.say(text)

            # Wait for the speech to complete
            engine.runAndWait()

            # Stop the engine to free up resources
            engine.stop()

        except Exception:
            # Fallback to console output if TTS fails
            print(text)


if __name__ == "__main__":
    phrase = input("Enter phrase: ")
    speaker = Speech()
    speaker.speak(phrase)
