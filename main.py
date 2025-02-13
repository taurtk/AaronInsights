import streamlit as st
import plotly.express as px
from utils.reddit_analyzer import RedditAnalyzer
from utils.nlp_processor import NLPProcessor
from utils.idea_generator import IdeaGenerator

# Page configuration
st.set_page_config(
    page_title="AI Idea Generator",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'reddit_analyzer' not in st.session_state:
    st.session_state.reddit_analyzer = RedditAnalyzer()
if 'nlp_processor' not in st.session_state:
    st.session_state.nlp_processor = NLPProcessor()
if 'idea_generator' not in st.session_state:
    st.session_state.idea_generator = IdeaGenerator()

# Main page header
st.title("💡 AI-Powered Idea Generator")
st.markdown("""
Discover innovative business ideas by analyzing Reddit discussions and trends.
This tool uses AI to process user discussions and generate valuable insights.
""")

# Sidebar
st.sidebar.title("Settings")
subreddit = st.sidebar.text_input("Enter Subreddit", "startups")
time_filter = st.sidebar.selectbox(
    "Time Period",
    ["day", "week", "month", "year", "all"]
)
post_limit = st.sidebar.slider("Number of Posts", 10, 100, 50)

# Main content
try:
    with st.spinner("Fetching data from Reddit..."):
        posts = st.session_state.reddit_analyzer.fetch_posts(
            subreddit, 
            time_filter, 
            post_limit
        )
        
    if posts:
        # Overview metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Posts Analyzed", len(posts))
        with col2:
            avg_score = sum(post['score'] for post in posts) / len(posts)
            st.metric("Average Score", f"{avg_score:.1f}")
        with col3:
            total_comments = sum(post['num_comments'] for post in posts)
            st.metric("Total Comments", total_comments)
        
        # Sentiment Analysis
        st.subheader("Sentiment Analysis")
        sentiments = st.session_state.nlp_processor.analyze_sentiments(
            [post['title'] + " " + post['selftext'] for post in posts]
        )
        
        # Sentiment Distribution Plot
        fig = px.pie(
            values=[sentiments.count('positive'), 
                   sentiments.count('neutral'), 
                   sentiments.count('negative')],
            names=['Positive', 'Neutral', 'Negative'],
            title='Sentiment Distribution',
            color_discrete_sequence=['#00CC96', '#FFA15A', '#EF553B']
        )
        st.plotly_chart(fig)
        
        # Export data
        if st.button("Export Data"):
            df = st.session_state.reddit_analyzer.export_to_dataframe(posts)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="reddit_data.csv",
                mime="text/csv"
            )
            
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please check the subreddit name and try again.")
