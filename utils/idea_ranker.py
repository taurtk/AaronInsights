import openai
import os
import json
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class IdeaRanker:
    """Ranks and filters ideas to return top 50"""
    
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.sambanova.ai/v1"
        )
    
    def rank_ideas(self, all_posts: List[Dict], user_prompt: str, limit: int = 50) -> List[Dict]:
        """Rank all collected posts and return top ideas"""
        
        if not all_posts:
            return []
        
        # First, filter and score posts
        scored_posts = self._score_posts(all_posts, user_prompt)
        
        # Sort by score and take top posts
        top_posts = sorted(scored_posts, key=lambda x: x.get('relevance_score', 0), reverse=True)[:100]
        
        # Generate final ideas from top posts
        return self._generate_final_ideas(top_posts, user_prompt, limit)
    
    def _score_posts(self, posts: List[Dict], user_prompt: str) -> List[Dict]:
        """Score posts based on relevance to user prompt"""
        scored_posts = []
        
        for post in posts:
            score = 0
            text = f"{post.get('title', '')} {post.get('text', '')}".lower()
            prompt_words = user_prompt.lower().split()
            
            # Basic keyword matching
            for word in prompt_words:
                if word in text:
                    score += 1
            
            # Engagement score
            score += min(post.get('score', 0) / 100, 5)  # Cap at 5 points
            score += min(post.get('num_comments', 0) / 50, 3)  # Cap at 3 points
            
            post['relevance_score'] = score
            scored_posts.append(post)
        
        return scored_posts
    
    def _generate_final_ideas(self, top_posts: List[Dict], user_prompt: str, limit: int) -> List[Dict]:
        """Generate final ranked ideas from top posts"""
        
        # Prepare context from top posts
        posts_context = "\n".join([
            f"Title: {post.get('title', '')}\nContent: {post.get('text', '')[:200]}...\nSource: {post.get('source', '')}\n"
            for post in top_posts[:50]  # Use top 50 posts for context
        ])
        
        system_prompt = f"""You are an expert business analyst. Based on the user's interest in "{user_prompt}" and the provided discussions, generate exactly {limit} ranked business ideas.

Each idea should be:
1. Directly relevant to the user's prompt
2. Based on real problems/opportunities from the discussions
3. Actionable and specific
4. Ranked by potential impact and feasibility

Return ONLY valid JSON array:
[
    {{
        "rank": 1,
        "title": "Specific business idea title",
        "problem": "Clear problem statement",
        "solution": "Detailed solution description",
        "market": "Target market description",
        "potential": "High/Medium/Low",
        "source_insight": "Key insight from discussions"
    }},
    ...
]"""
        
        user_message = f"""User's interest: "{user_prompt}"

Relevant discussions:
{posts_context}

Generate {limit} ranked business ideas based on these discussions."""
        
        try:
            response = self.client.chat.completions.create(
                model="DeepSeek-R1-Distill-Llama-70B",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON array
            start_idx = content.find('[')
            end_idx = content.rfind(']') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                ideas = json.loads(json_str)
                return ideas[:limit]
                
        except Exception as e:
            print(f"Error generating final ideas: {e}")
        
        # Fallback: convert top posts to simple ideas
        return self._create_fallback_ideas(top_posts[:limit], user_prompt)
    
    def _create_fallback_ideas(self, posts: List[Dict], user_prompt: str) -> List[Dict]:
        """Create simple ideas from posts as fallback"""
        ideas = []
        for i, post in enumerate(posts, 1):
            ideas.append({
                "rank": i,
                "title": f"Opportunity based on: {post.get('title', 'Discussion')[:50]}...",
                "problem": "Problem identified from community discussions",
                "solution": post.get('text', 'Solution details from analysis')[:200],
                "market": "Market identified from user discussions",
                "potential": "Medium",
                "source_insight": f"From {post.get('source', 'community')} discussion"
            })
        return ideas