import praw
import pandas as pd
from datetime import datetime

class RedditAnalyzer:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id="YOUR_CLIENT_ID",
            client_secret="YOUR_CLIENT_SECRET",
            user_agent="Idea Generator v1.0"
        )
    
    def fetch_posts(self, subreddit_name, time_filter, limit):
        """Fetch posts from specified subreddit."""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []
            
            for post in subreddit.top(time_filter=time_filter, limit=limit):
                posts.append({
                    'title': post.title,
                    'selftext': post.selftext,
                    'score': post.score,
                    'num_comments': post.num_comments,
                    'created_utc': datetime.fromtimestamp(post.created_utc),
                    'url': post.url
                })
            
            return posts
        except Exception as e:
            raise Exception(f"Error fetching Reddit data: {str(e)}")
    
    def export_to_dataframe(self, posts):
        """Convert posts to pandas DataFrame for export."""
        return pd.DataFrame(posts)
