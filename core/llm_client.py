import logging
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

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
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        
        logger.debug(
            "GeminiClient initialized | Model=%s Timeout=%s URL=%s",
            self.model,
            self.timeout,
            self.url
        )

    def generate(self, prompt):
        """
        Sends a prompt to the Gemini API and returns generated text.

        Args:
            prompt (str): Prompt text to be sent to the LLM.

        Returns:
            str | None: Generated text response, or None on failure.
        """
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
            return None
        
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
            logger.debug(
                "API request to Gemini | URL=%s Headers=%s Timeout=%s",
                self.url,
                headers,
                self.timeout
            )

            logger.debug(
                "API response from Gemini | Status=%s",
                response.status_code,
            )

            # Raises exception for non-2xx responses
            response.raise_for_status()

            # Decode JSON response from Gemini into Python objects
            data = response.json()
            logger.debug("Parsed JSON response from Gemini: %s", data)

            # Safely extract nested text without assuming response shape
            result = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            logger.debug("Gemini generated text: %s", result)

            return result

        except requests.RequestException as e:
            # Network issues, timeouts, or non-2xx HTTP responses
            logger.warning("HTTP/network error calling Gemini API: %s", e)
            return None

        except ValueError as e:
            # Response body was not valid JSON
            logger.warning("Failed to decode JSON response from Gemini: %s", e)
            return None

        except Exception:
            # Unexpected programming or runtime error
            logger.exception("Unexpected error in GeminiClient")
            return None
        

if __name__ == "__main__":
    from core.logger_config import setup_logging

    setup_logging()
    client = GeminiClient()

    prompt = input("Enter a prompt: ")
    client.generate(prompt=prompt)
