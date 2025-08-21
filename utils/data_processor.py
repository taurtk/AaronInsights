from datetime import datetime, timedelta
from collections import Counter
from utils.deepseek_client import DeepSeekClient

class DataProcessor:
    def __init__(self):
        self.deepseek = DeepSeekClient()

    @staticmethod
    def identify_trends(data: list) -> list:
        """Identify trends in the processed data"""
        if not data:
            return []

        all_keywords = [keyword for item in data for keyword in item.get('keywords', [])]
        keyword_counts = Counter(all_keywords)

        keyword_sentiments = {}
        for item in data:
            sentiment = item.get('sentiment', 0)
            for keyword in item.get('keywords', []):
                if keyword not in keyword_sentiments:
                    keyword_sentiments[keyword] = []
                keyword_sentiments[keyword].append(sentiment)

        trends = [
            {
                'keyword': keyword,
                'frequency': count,
                'avg_sentiment': sum(keyword_sentiments.get(keyword, [0])) / len(keyword_sentiments.get(keyword, [1]))
            }
            for keyword, count in keyword_counts.items()
        ]

        return sorted(trends, key=lambda x: x['frequency'], reverse=True)

    def generate_ideas(self, trends_data: list, num_ideas=5):
        """Generate business ideas using DeepSeek"""
        if not trends_data:
            return []

        return self.deepseek.generate_business_ideas(trends_data, num_ideas)

    def analyze_deep_trends(self, data: list):
        """Perform deep trend analysis using DeepSeek"""
        if not data:
            return None

        return self.deepseek.analyze_trends(data)

    @staticmethod
    def prepare_export_data(data: list, trends_data: list, deep_analysis=None):
        """Prepare data for export"""
        top_posts = sorted(data, key=lambda x: x.get('score', 0), reverse=True)[:10]
        export_data = {
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'posts_analyzed': len(data),
            'trending_topics': [trend['keyword'] for trend in trends_data[:10]],
            'average_sentiment': sum(item.get('sentiment', 0) for item in data) / len(data) if data else 0,
            'top_posts': [
                {'title': post.get('title'), 'score': post.get('score'), 'sentiment': post.get('sentiment')}
                for post in top_posts
            ],
            'deep_analysis': deep_analysis
        }
        return export_data