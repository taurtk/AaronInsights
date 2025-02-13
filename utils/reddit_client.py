import praw
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import os

class RedditClient:
    def __init__(self):
        # Initialize with credentials from environment variables
        self.reddit = praw.Reddit(
            client_id=os.environ.get("REDDIT_CLIENT_ID"),
            client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
            user_agent="IdeaGenerator/1.0 (by /u/IdeasBot)"
        )

    @st.cache_data(ttl=3600)
    def fetch_subreddit_data(_self, subreddit_name, time_filter='week', limit=100):
        """Fetch posts from specified subreddit"""
        try:
            subreddit = _self.reddit.subreddit(subreddit_name)
            posts = []

            for post in subreddit.top(time_filter=time_filter, limit=limit):
                posts.append({
                    'title': post.title,
                    'text': post.selftext,
                    'score': post.score,
                    'comments': post.num_comments,
                    'created_utc': datetime.fromtimestamp(post.created_utc),
                    'url': post.url,
                    'id': post.id
                })

            return pd.DataFrame(posts)
        except Exception as e:
            st.error(f"Error fetching Reddit data: {str(e)}")
            return pd.DataFrame()

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

            return pd.DataFrame(comments)
        except Exception as e:
            st.error(f"Error fetching comments: {str(e)}")
            return pd.DataFrame()