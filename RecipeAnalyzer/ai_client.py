from abc import ABC, abstractmethod
import logging
import os
import openai
import json
from typing import List

logger = logging.getLogger(__name__)

class AIClientInterface(ABC):
    """Interface for AI clients."""
    @abstractmethod
    def extract_ingredients(self, text: str) -> List[str]:
        pass
    @abstractmethod
    def extract_allergens(self, text: str) -> List[str]:
        pass

class AzureOpenAIAIClient(AIClientInterface):
    """
    Azure OpenAI client for extracting ingredients and allergens from recipe text.
    """
    
    # Initialize the client with environment variables for Azure OpenAI configuration.
    def __init__(self):
        self.deployment_name = os.environ.get('AZURE_OPENAI_DEPLOYMENT') 
        self.client = openai.AzureOpenAI(
            api_key=os.environ.get('AZURE_OPENAI_KEY'),
            api_version=os.environ.get('AZURE_OPENAI_API_VERSION'),
            azure_endpoint=os.environ.get('AZURE_OPENAI_ENDPOINT'),
        )
        
    # Helper method to call the Azure OpenAI chat completion API.
    def _chat_completion(self, system_prompt: str, user_text: str, log_label: str = None) -> List[str]:
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text}
                ],
                temperature=0.0,
            )
            result = json.loads(response.choices[0].message.content.strip())
            
            logger.info("\nExtracted %s:\n%s\n", log_label, '\n'.join(f"- {item}" for item in result))
            return result
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error extracting {log_label}: {e}")
            raise ValueError(f"AI returned invalid JSON for {log_label}")
        except Exception as e:
            logger.error(f"Error extracting {log_label}: {e}")
            raise ValueError(f"AI extraction failed for {log_label}")

    def extract_ingredients(self, text: str) -> List[str]:
        """
        Extract ingredient lines from the provided recipe text.
        """
        system_prompt = (
            "Extract only the real ingredient lines from the following recipe page text. "
            "Return only the list as a JSON array of strings. Do not include any explanation or text, only the JSON array."
        )
        
        return self._chat_completion(system_prompt, text, log_label="ingredients")

    def extract_allergens(self, text: str) -> List[str]:
        """
        Extract potential allergens from the provided recipe text.
        """
        system_prompt = (
            "Given the following list of recipe ingredients, return ONLY a deduplicated JSON array of ingredients that can cause any allergic response. "
            "For each ingredient, if it can cause any allergic reaction, add it to the list as-is (do not convert to base ingredients; e.g., if 'yogurt' is present, include 'yogurt', not 'milk'). "
            "It it very important to carefully identify potential allergens, and any ingredient that can cause an allergic reaction should be included in the list. "
            "Return ONLY the JSON array of ingredient names that are potential allergens, with no explanation or extra text."
        )
        
        return self._chat_completion(system_prompt, text, log_label="allergens")
