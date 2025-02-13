import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Trends Analysis", page_icon="📈")

st.title("📈 Trends Analysis")

# Get data from session state
if 'reddit_analyzer' in st.session_state:
    analyzer = st.session_state.reddit_analyzer
    nlp = st.session_state.nlp_processor
    
    try:
        posts = analyzer.fetch_posts("startups", "month", 100)
        
        # Time series analysis
        dates = [post['created_utc'] for post in posts]
        scores = [post['score'] for post in posts]
        
        fig = px.line(
            x=dates, 
            y=scores,
            title='Post Engagement Over Time',
            labels={'x': 'Date', 'y': 'Score'}
        )
        st.plotly_chart(fig)
        
        # Keyword analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Keywords")
            keywords = nlp.extract_keywords(
                [post['title'] + " " + post['selftext'] for post in posts]
            )
            
            keyword_df = px.bar(
                x=[k[0] for k in keywords],
                y=[k[1] for k in keywords],
                title="Most Common Keywords"
            )
            st.plotly_chart(keyword_df)
        
        with col2:
            st.subheader("Topic Distribution")
            # Simple topic categorization based on keywords
            topics = {
                'Technology': ['tech', 'software', 'app'],
                'Business': ['business', 'startup', 'company'],
                'Marketing': ['marketing', 'sales', 'advertising'],
                'Finance': ['finance', 'money', 'investment']
            }
            
            topic_counts = {topic: 0 for topic in topics}
            for post in posts:
                text = (post['title'] + " " + post['selftext']).lower()
                for topic, keywords in topics.items():
                    if any(keyword in text for keyword in keywords):
                        topic_counts[topic] += 1
            
            fig = px.pie(
                values=list(topic_counts.values()),
                names=list(topic_counts.keys()),
                title='Topic Distribution'
            )
            st.plotly_chart(fig)
            
    except Exception as e:
        st.error(f"Error loading trends: {str(e)}")
else:
    st.warning("Please run the main page first to initialize the analyzers.")
