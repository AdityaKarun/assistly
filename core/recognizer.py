import speech_recognition

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
            print("Listening...")

            # Adjust for ambient noise to improve recognition accuracy
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Listen for user's voice input
            audio = self.recognizer.listen(source)

        try:
            # Use Google's speech recognition backend for transcription
            command = self.recognizer.recognize_google(audio)
            command = command.lower()
            return command

        except Exception as e:
            # Any recognition failure is treated as non-fatal
            print(f"Recognition error: {e}")
            return None


if __name__ == "__main__":
    recognizer_object = Recognizer()
    
    while True:
        input("Hit enter to listen (Ctrl+C to exit)")
        command = recognizer_object.recognize_command()
        print(command)
