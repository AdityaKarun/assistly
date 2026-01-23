import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GeminiClient:
    def __init__(self, model="gemini-2.5-flash", timeout=10):
        """
        Initializes the Gemini LLM client with model and request settings.

        Args:
            model (str): Gemini model identifier to use for generation.
            timeout (int): HTTP timeout in seconds for API calls.

        Returns:
            None
        """
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = model
        self.timeout = timeout
        self.url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        )

    def generate(self, prompt):
        """
        Sends a prompt to the Gemini API and returns generated text.

        Args:
            prompt (str): Prompt text to be sent to the LLM.

        Returns:
            str: Generated text response, or empty string on failure.
        """
        if not self.api_key:
            print("GEMINI_API_KEY not found in environment variables.")
        
        headers = {
            "Content-Type": "application/json"
        }

        params = {
            "key": self.api_key
        }

        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }

        try:
            response = requests.post(
                self.url,
                headers=headers,
                params=params,
                json=payload,
                timeout=self.timeout
            )

            # Raises exception for non-2xx responses
            response.raise_for_status()

            data = response.json()

            # Safely extract nested text without assuming response shape
            return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

        except Exception as e:
            # Network, timeout, or API errors are handled gracefully
            print(f"API call to the LLM failed: {str(e)}")
            return ""
        

if __name__ == "__main__":
    client = GeminiClient()
    prompt = input("Enter a prompt: ")
    result = client.generate(prompt=prompt)
    print(result)
