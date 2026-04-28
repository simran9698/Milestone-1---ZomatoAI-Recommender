import os
import json
import time
from groq import Groq
from dotenv import load_dotenv
from src.config import config
from src.phase5_infra.logger import logger

load_dotenv()

class GroqLLMClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key or self.api_key == "your_groq_api_key_here":
            logger.warning("GROQ_API_KEY not set or is default. LLM will not function correctly.")
        self.client = Groq(api_key=self.api_key) if self.api_key and self.api_key != "your_groq_api_key_here" else None
        self.model = config['llm']['model']
        self.max_tokens = config['llm']['max_tokens']
        self.temperature = config['llm']['temperature']

    def generate_recommendations(self, prompt: str, max_retries: int = 3) -> dict:
        if not self.client:
            logger.error("Groq client not initialized")
            return {"recommendations": []}

        for attempt in range(max_retries):
            try:
                logger.info(f"Calling Groq LLM (Attempt {attempt+1}/{max_retries})")
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert restaurant recommender. You output ONLY valid JSON. CRITICAL: Be mathematically and logically precise. When comparing ratings, ensure your logic is sound. For example, a rating of 4.6 is HIGHER than or equal to a minimum requirement of 4.0, NOT below it. Never state a value is below a requirement if it is greater than or equal to it."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model=self.model,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    response_format={"type": "json_object"}
                )
                
                response_content = chat_completion.choices[0].message.content
                parsed_json = json.loads(response_content)
                logger.info("Successfully generated and parsed LLM response")
                return parsed_json
            except json.JSONDecodeError as e:
                logger.error(f"JSON Parsing failed: {e}")
            except Exception as e:
                logger.error(f"LLM Call failed: {e}")
            
            backoff_time = 2 ** attempt
            logger.info(f"Retrying in {backoff_time} seconds...")
            time.sleep(backoff_time)
            
        logger.error("All retries failed for LLM generation")
        return {"recommendations": []}

    def merge_with_catalog(self, llm_output: dict, catalog_shortlist: list) -> list:
        merged = []
        llm_recs = {r.get('name', '').lower(): r.get('explanation', '') for r in llm_output.get('recommendations', [])}
        
        for item in catalog_shortlist:
            name_lower = item['name'].lower()
            explanation = llm_recs.get(name_lower, "Highly rated restaurant matching your preferences.")
            
            merged_item = item.copy()
            merged_item['explanation'] = explanation
            merged.append(merged_item)
            
        return merged
