import os
import openai
import streamlit as st
import json
import httpx
import pandas as pd

class DeepSeekClient:
    def __init__(self):
        api_key = os.getenv("DEEPSEEK_API_KEY")
        
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.sambanova.ai/v1",
            http_client=httpx.Client(),
        )
        self.model = "Llama-4-Maverick-17B-128E-Instruct"

    @st.cache_data(ttl=3600)
    def generate_business_ideas(_self, trends_data, num_ideas=5):
        """Generate business ideas using DeepSeek"""
        try:
            # Prepare context from trends data
            trends_context = "\n".join([
                f"- {trend['keyword']} (frequency: {trend['frequency']}, sentiment: {trend['avg_sentiment']:.2f})"
                for trend in trends_data.head(10).to_dict('records')
            ])

            system_prompt = """You are an expert business consultant and idea generator. Your task is to analyze market trends and generate innovative business ideas in a structured JSON format. Each idea must include:
1. A clear problem statement
2. A detailed solution
3. A specific target market
4. Key features
Always return exactly the requested number of ideas in a valid JSON array."""

            user_prompt = f"""Based on these market trends and user discussions:
{trends_context}

Generate exactly {num_ideas} structured business ideas.
Return them in this exact JSON format:
[
    {{
        "problem": "A clear and specific problem statement",
        "solution": "A detailed description of how the solution works",
        "target_market": "Specific description of who will use this",
        "features": ["Key feature 1", "Key feature 2", "Key feature 3"]
    }},
    ...
]

Important:
- Return exactly {num_ideas} ideas
- Ensure each idea is detailed and specific
- Keep the JSON structure exactly as shown
- Make sure the response is valid JSON"""

            response = _self.client.chat.completions.create(
                model=_self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                top_p=0.9,
            )

            # Parse and validate response
            content = response.choices[0].message.content.strip()
            try:
                # Try to find JSON array in the response
                start_idx = content.find('[')
                end_idx = content.rfind(']') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = content[start_idx:end_idx]
                    ideas = json.loads(json_str)
                    if isinstance(ideas, list):
                        # Ensure exactly num_ideas are returned
                        if len(ideas) > num_ideas:
                            ideas = ideas[:num_ideas]
                        elif len(ideas) < num_ideas:
                            # Pad with placeholder ideas if needed
                            while len(ideas) < num_ideas:
                                ideas.append({
                                    "problem": "Additional opportunity identified",
                                    "solution": "Analysis in progress",
                                    "target_market": "Market research ongoing",
                                    "features": ["Feature analysis pending"]
                                })
                        return ideas

                # Fallback for invalid JSON array
                raise json.JSONDecodeError("Invalid JSON array", content, 0)

            except json.JSONDecodeError:
                st.warning("⚠️ The AI response format was unexpected. Retrying with simplified format...")
                # Retry with more basic prompt
                retry_response = _self.client.chat.completions.create(
                    model=_self.model,
                    messages=[
                        {"role": "system", "content": "Generate simple business ideas in JSON format."},
                        {"role": "user", "content": f"Generate {num_ideas} business ideas based on these trends: {trends_context}"}
                    ],
                    temperature=0.5,
                )

                try:
                    retry_content = retry_response.choices[0].message.content
                    # Try to extract any JSON-like content
                    ideas = []
                    lines = retry_content.split('\n')
                    for i in range(min(num_ideas, len(lines))):
                        ideas.append({
                            "problem": f"Trend Analysis #{i+1}",
                            "solution": lines[i].strip(),
                            "target_market": "Market analysis in progress",
                            "features": ["Detailed features coming soon"]
                        })
                    return ideas
                except Exception:
                    return [{
                        "problem": "AI Response Processing Error",
                        "solution": "Our AI service is currently experiencing issues with response formatting",
                        "target_market": "Please try again in a few moments",
                        "features": ["System will retry automatically"]
                    }] * num_ideas

        except Exception as e:
            st.error(f"Error generating ideas: {str(e)}")
            return [{
                "problem": "Service Temporarily Unavailable",
                "solution": "We're experiencing technical difficulties",
                "target_market": "Please try again later",
                "features": ["Service will be restored shortly"]
            }] * num_ideas

    def _validate_subreddits(self, subreddits: list) -> list:
        """Map AI-generated subreddit names to valid ones with Y Combinator priority"""
        valid_mapping = {
            'AI': 'artificial',
            'MachineLearning': 'MachineLearning',
            'Technology': 'technology',
            'Business': 'business',
            'Entrepreneur': 'Entrepreneur',
            'Startups': 'startups',
            'Innovation': 'innovation',
            'SustainableLiving': 'ZeroWaste',
            'RemoteWork': 'remotework',
            'FitnessTech': 'fitness',
            'CreativeHobbies': 'crafts',
            'SmartHome': 'homeautomation',
            'OnlineLearning': 'OnlineEducation'
        }
        
        # High-value subreddits prioritized
        high_value_subreddits = [
            'YCombinator', 'startups', 'entrepreneur', 'business', 'SideProject',
            'indiehackers', 'SaaS', 'EntrepreneurRideAlong', 'smallbusiness',
            'growmybusiness', 'BusinessIdeas', 'startup_ideas'
        ]
        
        validated = []
        for sub in subreddits:
            if sub in valid_mapping:
                validated.append(valid_mapping[sub])
            elif sub in high_value_subreddits:
                validated.append(sub)
            elif sub.lower() in [s.lower() for s in high_value_subreddits]:
                validated.append(sub)
            else:
                # Replace invalid with high-value fallback
                if len(validated) < 10:
                    validated.append(high_value_subreddits[len(validated) % len(high_value_subreddits)])
        
        return validated[:10]  # Increased limit to capture more sources

    def generate_search_queries(_self, prompt: str) -> dict:
        """Generate subreddit and Quora search queries from a prompt with high-value sources."""
        try:
            # Top 15 verified high-value startup subreddits for speed
            base_subreddits = [
                'YCombinator', 'startups', 'Entrepreneur', 'business', 'SideProject', 'indiehackers', 
                'smallbusiness', 'BusinessIdeas', 'investing', 'technology', 'artificial', 'MachineLearning', 
                'marketing', 'ecommerce', 'cryptocurrency'
            ]
            
            # Add topic-specific subreddits
            topic_keywords = prompt.lower()
            topic_subreddits = []
            
            if any(word in topic_keywords for word in ['ai', 'artificial', 'machine', 'tech']):
                topic_subreddits = ['artificial', 'MachineLearning', 'technology', 'SaaS', 'indiehackers']
            elif any(word in topic_keywords for word in ['fitness', 'health', 'wellness']):
                topic_subreddits = ['fitness', 'health', 'nutrition', 'bodyweightfitness', 'loseit']
            elif any(word in topic_keywords for word in ['sustainable', 'eco', 'green', 'environment']):
                topic_subreddits = ['ZeroWaste', 'sustainability', 'environment', 'renewable', 'climatechange']
            elif any(word in topic_keywords for word in ['finance', 'money', 'fintech']):
                topic_subreddits = ['investing', 'SecurityAnalysis', 'financialindependence', 'personalfinance']
            elif any(word in topic_keywords for word in ['education', 'learning', 'course']):
                topic_subreddits = ['OnlineEducation', 'GetStudying', 'studytips', 'teachers']
            else:
                topic_subreddits = ['innovation', 'smallbusiness', 'growmybusiness', 'BusinessIdeas']
            
            # Combine base and topic subreddits
            all_subreddits = base_subreddits + topic_subreddits
            
            # Top 10 high-value Quora queries for speed
            quora_queries = [
                f"Y Combinator {prompt} startup ideas", f"successful {prompt} business models", 
                f"best {prompt} business ideas", f"profitable {prompt} niches", 
                f"unicorn {prompt} startups", f"bootstrapped {prompt} businesses",
                f"{prompt} market opportunities", f"{prompt} SaaS business", 
                f"{prompt} AI applications", f"{prompt} fintech solutions"
            ]
            
            return {
                "subreddits": all_subreddits,
                "quora": quora_queries
            }
            
        except Exception as e:
            st.error(f"An error occurred while generating search queries: {e}")
            return {
                "subreddits": ['YCombinator', 'startups', 'entrepreneur', 'business', 'SideProject'],
                "quora": [f"Y Combinator {prompt} ideas", f"successful {prompt} startups"]
            }
    
    def generate_unique_ideas(self, prompt: str, reddit_data, quora_data, num_ideas: int = 20):
        """Generate 10 ideas from Reddit and 10 from Quora for speed"""
        try:
            all_ideas = []
            
            # Generate 10 ideas from Reddit
            reddit_ideas = self._generate_ideas_from_source(prompt, reddit_data, 'reddit', 10)
            all_ideas.extend(reddit_ideas)
            
            # Generate 10 ideas from Quora
            quora_ideas = self._generate_ideas_from_source(prompt, quora_data, 'quora', 10)
            all_ideas.extend(quora_ideas)
            
            return all_ideas
            
        except Exception as e:
            st.error(f"Error generating unique ideas: {e}")
            return []
    
    def _generate_ideas_from_source(self, prompt: str, data, source: str, target_count: int):
        """Generate ideas from a specific source"""
        ideas = []
        idea_texts = []
        
        # Process data based on type
        content_list = []
        if isinstance(data, pd.DataFrame) and not data.empty:
            for _, row in data.iterrows():
                content_list.append(f"{row.get('title', '')} {row.get('text', '')}")
        elif isinstance(data, list) and data:
            for item in data:
                if isinstance(item, dict):
                    content_list.append(f"{item.get('title', '')} {item.get('text', '')}")
                else:
                    content_list.append(str(item))
        
        # If no data, generate generic ideas
        if not content_list:
            content_list = [f"General {prompt} business opportunities and market trends"]
        
        # Generate ideas until we reach target count
        attempts = 0
        while len(ideas) < target_count and attempts < 20:
            for content in content_list:
                if len(ideas) >= target_count:
                    break
                    
                system_prompt = f"""You are a creative business consultant specializing in {prompt}. Generate innovative, specific business ideas. Each idea should be:
1. Unique and actionable
2. Market-focused and profitable
3. Solve a real problem
4. Be 2-3 sentences describing the business concept"""
                
                user_prompt = f"""Based on this market insight about {prompt}:

{content[:400]}

Generate 5 completely unique business ideas. Make each idea specific, actionable, and different from typical solutions. Return only the ideas, one per line."""
                
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=0.9,
                        max_tokens=400
                    )
                    
                    if response.choices and response.choices[0].message.content:
                        new_ideas = response.choices[0].message.content.strip().split('\n')
                        
                        for idea in new_ideas:
                            idea = idea.strip().lstrip('1234567890.-• ')
                            if idea and len(idea) > 30 and self._is_unique_idea(idea, idea_texts):
                                ideas.append({
                                    'idea': idea,
                                    'source': source
                                })
                                idea_texts.append(idea)
                                
                                if len(ideas) >= target_count:
                                    break
                except Exception:
                    continue
            
            attempts += 1
        
        # Fill remaining slots with generic ideas if needed
        while len(ideas) < target_count:
            generic_idea = f"Innovative {prompt} solution #{len(ideas)+1} - A unique approach to solving market challenges in the {prompt} industry using modern technology and customer-centric design."
            ideas.append({
                'idea': generic_idea,
                'source': source
            })
        
        return ideas[:target_count]
    
    def _is_unique_idea(self, new_idea: str, existing_ideas: list) -> bool:
        """Check if idea is unique using simple text comparison"""
        if not existing_ideas:
            return True
        
        new_words = set(new_idea.lower().split())
        
        for existing in existing_ideas:
            existing_words = set(existing.lower().split())
            # Check if ideas share more than 50% of words
            common_words = new_words.intersection(existing_words)
            similarity = len(common_words) / max(len(new_words), len(existing_words))
            
            if similarity > 0.5:
                return False
        
        return True

    def analyze_trends(_self, posts_data):
        """Analyze trends using DeepSeek for deeper insights"""
        try:
            combined_text = "\n".join([
                f"Title: {post['title']}\nText: {post['text']}\n"
                for post in posts_data.head(10).to_dict('records')
            ])

            system_prompt = """You are an expert market analyst. Analyze the provided content and return insights in valid JSON format with these exact categories:
- market_trends: List of emerging market trends
- pain_points: List of user problems and challenges
- opportunities: List of potential business opportunities
- themes: List of common themes or patterns"""

            user_prompt = f"""Analyze these Reddit posts and provide structured insights:

{combined_text}

Return the analysis in this exact JSON format:
{{
    "market_trends": ["trend 1", "trend 2", "trend 3"],
    "pain_points": ["pain point 1", "pain point 2", "pain point 3"],
    "opportunities": ["opportunity 1", "opportunity 2", "opportunity 3"],
    "themes": ["theme 1", "theme 2", "theme 3"]
}}"""

            response = _self.client.chat.completions.create(
                model=_self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,
                top_p=0.8,
            )

            try:
                content = response.choices[0].message.content.strip()
                # Try to find JSON object in the response
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = content[start_idx:end_idx]
                    return json.loads(json_str)
                raise json.JSONDecodeError("Invalid JSON object", content, 0)
            except json.JSONDecodeError:
                return {
                    "market_trends": ["Currently analyzing market trends..."],
                    "pain_points": ["Processing user feedback..."],
                    "opportunities": ["Identifying business opportunities..."],
                    "themes": ["Extracting common themes..."]
                }

        except Exception as e:
            st.error(f"Error analyzing trends: {str(e)}")
            return {
                "market_trends": ["Analysis temporarily unavailable"],
                "pain_points": ["Service disruption"],
                "opportunities": ["Please try again later"],
                "themes": ["System recovery in progress"]
            }