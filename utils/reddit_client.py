import praw
from datetime import datetime, timedelta
import streamlit as st
import os
# from dotenv import load_dotenv

# load_dotenv()

class RedditClient:
    def __init__(self):
        # Debugging: Print environment variables
        print("Checking environment variables in reddit_client.py:")
        # print(f"REDDIT_CLIENT_ID: {os.getenv('REDDIT_CLIENT_ID')}")
        # print(f"REDDIT_CLIENT_SECRET: {os.getenv('REDDIT_CLIENT_SECRET')}")
        print("---------------------------------------")
        
        try:
            self.reddit = praw.Reddit(
                client_id="WCJasChIwA9F6W3DnVmIiQ",
                client_secret="c2GNbz0F-KwrB3-BGuNIzDpED_HZ1A",
                user_agent="AaronInsights/1.0"
            )
        except Exception as e:
            st.error(f"Reddit authentication failed: {e}")
            self.reddit = None

    @st.cache_data(ttl=3600)
    def fetch_subreddit_data(_self, subreddit_names: list, time_filter='week', limit=50):
        """Fetch posts from specified subreddits with high-value startup communities"""
        # Top 20 verified high-value startup subreddits for speed
        high_value_subreddits = [
            'YCombinator', 'startups', 'business', 'technology', 'innovation', 'SideProject', 
            'smallbusiness', 'Entrepreneur', 'BusinessIdeas', 'indiehackers', 'investing', 
            'artificial', 'MachineLearning', 'programming', 'webdev', 'marketing', 
            'ecommerce', 'cryptocurrency', 'Bitcoin', 'fitness'
        ]
        
        # Combine user queries with high-value subreddits (remove duplicates)
        all_subreddits = list(set(subreddit_names + high_value_subreddits))
        
        all_posts = []
        for subreddit_name in all_subreddits:
            try:
                subreddit = _self.reddit.subreddit(subreddit_name)
                # Test if subreddit exists
                subreddit.display_name
                
                # Get only hot posts for speed
                posts_to_fetch = list(subreddit.hot(limit=10))
                
                for post in posts_to_fetch:
                    all_posts.append({
                        'title': post.title,
                        'text': post.selftext or post.title,
                        'score': post.score,
                        'comments': post.num_comments,
                        'created_utc': datetime.fromtimestamp(post.created_utc),
                        'url': post.url,
                        'id': post.id,
                        'subreddit': subreddit_name
                    })
            except Exception as e:
                st.warning(f"Skipping subreddit '{subreddit_name}': {str(e)}")
                continue
        
        return all_posts

    def get_comments(self, post_id, limit=50):
        """Fetch comments for a specific post"""
        try:
            submission = self.reddit.submission(id=post_id)
            comments = []
            submission.comments.replace_more(limit=0)

            for comment in submission.comments.list()[:limit]:
                comments.append({
                    'text': comment.body,
                    'score': comment.score,
                    'created_utc': datetime.fromtimestamp(comment.created_utc)
                })

            return comments
        except Exception as e:
            st.error(f"Error fetching comments: {str(e)}")
            return []