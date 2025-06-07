from app.config import Config
import google.generativeai as genai
from openai import OpenAI
from loguru import logger
import json
import re


class LLMClient:
    def __init__(self):
        self.provider = Config.LLM_PROVIDER.lower()
        self.model = Config.LLM_MODEL
        logger.info(
            f"Initializing LLM client with provider: {self.provider}, model: {self.model}"
        )

        if self.provider == "gemini":
            if not Config.GEMINI_API_KEY:
                logger.error("GEMINI_API_KEY not set")
                raise ValueError("GEMINI_API_KEY not set")
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.client = genai.GenerativeModel(self.model)
        elif self.provider == "openai":
            if not Config.OPENAI_API_KEY:
                logger.error("OPENAI_API_KEY not set")
                raise ValueError("OPENAI_API_KEY not set")
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        else:
            logger.error(f"Unsupported LLM provider: {self.provider}")
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def clean_json_response(self, response: str) -> dict:
        """
        Clean and parse JSON response from LLM, handling ```json markers and formatting issues.

        Args:
            response (str): Raw LLM response.

        Returns:
            dict: Parsed JSON object.

        Raises:
            ValueError: If JSON parsing fails.
        """
        logger.debug("Cleaning LLM JSON response")
        try:
            # Remove ```json and ``` markers, and any leading/trailing whitespace
            cleaned = re.sub(
                r"^```json\s*|\s*```$", "", response.strip(), flags=re.MULTILINE
            )
            # Remove any extra newlines or whitespace
            cleaned = cleaned.strip()
            logger.debug(f"Cleaned JSON response: {cleaned[:100]}...")
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(
                f"Failed to parse JSON response: {response[:100]}... Error: {str(e)}"
            )
            raise ValueError(f"Invalid JSON response: {str(e)}")

    def generate_json(self, system_prompt: str, user_prompt: str) -> dict:
        """
        Generate a JSON response from the LLM and parse it.

        Args:
            system_prompt (str): System prompt to set the context for the LLM.
            user_prompt (str): User prompt to send to the LLM.

        Returns:
            dict: Parsed JSON response.
        """
        logger.info(f"Generating JSON response with {self.provider} LLM")
        try:
            if self.provider == "gemini":
                response = self.client.generate_content(
                    f"System: {system_prompt}\nUser: {user_prompt}",
                )
                return self.clean_json_response(response.text)
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                return self.clean_json_response(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"LLM API call failed: {str(e)}")
            raise
