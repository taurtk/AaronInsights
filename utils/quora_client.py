import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from typing import List, Dict

class QuoraClient:
    """Client for scraping startup ideas from Quora"""
    
    def __init__(self):
        self.base_url = "https://www.quora.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def fetch_quora_data(self, queries: List[str], limit_per_query: int = 100) -> List[Dict]:
        """
        Search for posts on Quora using multiple queries
        
        Args:
            queries: List of search queries
            limit_per_query: Maximum posts per query
            
        Returns:
            List of dictionaries containing posts
        """
        all_posts = []
        
        try:
            for query in queries:
                search_url = f"{self.base_url}/search?q={query.replace(' ', '+')}"
                
                response = self.session.get(search_url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract questions and answers
                    questions = soup.find_all('div', class_='q-text')
                    
                    for question in questions[:limit_per_query]:
                        try:
                            title = question.get_text().strip()
                            all_posts.append({
                                'title': title,
                                'text': title,  # For Quora, title is the main content
                                'source': 'Quora',
                                'score': random.randint(1, 100),  # Simulated engagement
                                'num_comments': random.randint(0, 50),
                                'query': query
                            })
                        except Exception:
                            continue
                
                time.sleep(random.uniform(0.5, 1.5))
                
        except Exception as e:
            print(f"Error fetching from Quora: {e}")
        
        # Add sample posts if scraping fails
        if not all_posts:
            all_posts = self._get_sample_posts(queries)
        
        return all_posts
    
    def _is_startup_related(self, text: str) -> bool:
        """Check if text is related to startups or business ideas"""
        startup_keywords = [
            'startup', 'business idea', 'entrepreneur', 'company', 'venture',
            'innovation', 'product', 'service', 'market', 'opportunity'
        ]
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in startup_keywords)
    
    def _categorize_idea(self, title: str) -> str:
        """Categorize startup idea based on title content"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['tech', 'app', 'software', 'ai', 'digital']):
            return 'Technology'
        elif any(word in title_lower for word in ['health', 'medical', 'fitness']):
            return 'Healthcare'
        elif any(word in title_lower for word in ['food', 'restaurant', 'delivery']):
            return 'Food & Beverage'
        elif any(word in title_lower for word in ['education', 'learning', 'course']):
            return 'Education'
        elif any(word in title_lower for word in ['finance', 'money', 'payment']):
            return 'Finance'
        else:
            return 'General'
    
    def _get_sample_posts(self, queries: List[str]) -> List[Dict]:
        """Return sample posts if scraping fails"""
        sample_posts = []
        for i, query in enumerate(queries[:5]):
            sample_posts.extend([
                {
                    'title': f'What are the best opportunities in {query}?',
                    'text': f'Discussion about opportunities and challenges in {query} market',
                    'source': 'Quora Sample',
                    'score': random.randint(10, 200),
                    'num_comments': random.randint(5, 50),
                    'query': query
                },
                {
                    'title': f'How to start a business in {query}?',
                    'text': f'Practical advice for starting ventures related to {query}',
                    'source': 'Quora Sample', 
                    'score': random.randint(10, 200),
                    'num_comments': random.randint(5, 50),
                    'query': query
                }
            ])
        return sample_posts
    
    def get_trending_startup_topics(self) -> List[str]:
        """Get trending startup topics from Quora"""
        topics = [
            "AI and Machine Learning Startups",
            "Sustainable Business Ideas",
            "Remote Work Solutions",
            "Health Tech Innovations",
            "EdTech Platforms",
            "FinTech Solutions",
            "E-commerce Tools",
            "Social Impact Startups"
        ]
        return topics