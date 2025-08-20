import openai
import os
import json
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class PromptProcessor:
    """Converts user prompts into subreddit and Quora search queries"""
    
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.sambanova.ai/v1"
        )
    
    def generate_search_queries(self, user_prompt: str) -> Dict[str, List[str]]:
        """Convert user prompt into relevant subreddits and Quora queries"""
        
        system_prompt = """You are an expert at finding relevant online communities and search queries. 
        Given a user's prompt about business ideas or topics, generate:
        1. 5-10 relevant subreddits (without r/ prefix)
        2. 5-10 Quora search queries
        
        Return ONLY valid JSON in this exact format:
        {
            "subreddits": ["subreddit1", "subreddit2", ...],
            "quora_queries": ["query1", "query2", ...]
        }"""
        
        user_message = f"""User prompt: "{user_prompt}"
        
        Generate relevant subreddits and Quora search queries for this topic.
        Focus on communities and searches that would contain discussions about business opportunities, problems, trends, and ideas related to this topic."""
        
        try:
            response = self.client.chat.completions.create(
                model="DeepSeek-R1-Distill-Llama-70B",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                result = json.loads(json_str)
                
                # Validate and limit results
                subreddits = result.get('subreddits', [])[:10]
                quora_queries = result.get('quora_queries', [])[:10]
                
                return {
                    'subreddits': subreddits,
                    'quora_queries': quora_queries
                }
        except Exception as e:
            print(f"Error generating queries: {e}")
        
        # Fallback for common business topics
        return self._get_fallback_queries(user_prompt)
    
    def _get_fallback_queries(self, prompt: str) -> Dict[str, List[str]]:
        """Fallback queries based on common patterns"""
        prompt_lower = prompt.lower()
        
        subreddits = ['startups', 'entrepreneur', 'business', 'smallbusiness']
        quora_queries = ['startup ideas', 'business opportunities', 'entrepreneurship']
        
        # Add specific subreddits based on keywords
        if any(word in prompt_lower for word in ['tech', 'app', 'software', 'ai']):
            subreddits.extend(['technology', 'programming', 'artificial'])
        if any(word in prompt_lower for word in ['health', 'fitness', 'medical']):
            subreddits.extend(['health', 'fitness', 'medical'])
        if any(word in prompt_lower for word in ['food', 'restaurant']):
            subreddits.extend(['food', 'cooking', 'restaurant'])
        
        return {
            'subreddits': subreddits[:10],
            'quora_queries': quora_queries[:10]
        }