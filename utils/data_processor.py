import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from utils.deepseek_client import DeepSeekClient

class DataProcessor:
    def __init__(self):
        self.deepseek = DeepSeekClient()

    @staticmethod
    def identify_trends(df):
        """Identify trends in the processed data"""
        if df.empty:
            return pd.DataFrame()

        # Group keywords and calculate metrics
        all_keywords = []
        for keywords in df['keywords']:
            all_keywords.extend(keywords)

        keyword_stats = pd.DataFrame({
            'keyword': all_keywords
        }).value_counts().reset_index()
        keyword_stats.columns = ['keyword', 'frequency']

        # Calculate average sentiment per keyword
        keyword_sentiments = {}
        for _, row in df.iterrows():
            sentiment = row['sentiment']
            for keyword in row['keywords']:
                if keyword in keyword_sentiments:
                    keyword_sentiments[keyword].append(sentiment)
                else:
                    keyword_sentiments[keyword] = [sentiment]

        keyword_stats['avg_sentiment'] = keyword_stats['keyword'].apply(
            lambda x: sum(keyword_sentiments[x])/len(keyword_sentiments[x])
        )

        return keyword_stats.sort_values('frequency', ascending=False)

    def generate_ideas(self, trends_df, num_ideas=5):
        """Generate business ideas using DeepSeek"""
        if trends_df.empty:
            return []

        return self.deepseek.generate_business_ideas(trends_df, num_ideas)

    def analyze_deep_trends(self, df):
        """Perform deep trend analysis using DeepSeek"""
        if df.empty:
            return None

        return self.deepseek.analyze_trends(df)

    @staticmethod
    def prepare_export_data(df, trends_df, deep_analysis=None):
        """Prepare data for export"""
        export_data = {
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'posts_analyzed': len(df),
            'trending_topics': trends_df['keyword'].tolist()[:10],
            'average_sentiment': df['sentiment'].mean(),
            'top_posts': df[['title', 'score', 'sentiment']].head(10).to_dict('records'),
            'deep_analysis': deep_analysis
        }
        return export_data