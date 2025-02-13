import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd
import streamlit as st

# Download required NLTK data
nltk.download('punkt')
nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('punkt_tab')

class NLPProcessor:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))

    def analyze_sentiment(self, text):
        """Analyze sentiment of given text"""
        if not isinstance(text, str):
            return 0

        sentiment_scores = self.sia.polarity_scores(text)
        return sentiment_scores['compound']

    def extract_keywords(self, text, top_n=10):
        """Extract most common keywords from text"""
        if not isinstance(text, str):
            return []

        # Tokenize and clean text
        words = text.lower().split()  # Simplified tokenization
        words = [word for word in words if word.isalnum() 
                and word not in self.stop_words]

        # Count frequencies
        word_freq = Counter(words)
        return word_freq.most_common(top_n)

    def process_dataframe(self, df):
        """Process DataFrame with sentiment analysis and keyword extraction"""
        if df.empty:
            return df

        # Combine title and text for analysis
        df['combined_text'] = df['title'] + ' ' + df['text'].fillna('')

        # Add sentiment scores
        df['sentiment'] = df['combined_text'].apply(self.analyze_sentiment)

        # Extract keywords
        df['keywords'] = df['combined_text'].apply(
            lambda x: [kw[0] for kw in self.extract_keywords(x)]
        )

        return df