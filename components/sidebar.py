import streamlit as st

def render_sidebar():
    """Render the sidebar with controls"""
    st.sidebar.title("Settings")
    
    # Subreddit selection
    subreddit = st.sidebar.text_input(
        "Enter Subreddit",
        value="startups",
        help="Enter the name of the subreddit to analyze"
    )
    
    # Time filter
    time_filter = st.sidebar.selectbox(
        "Time Period",
        options=['day', 'week', 'month', 'year'],
        index=1,
        help="Select the time period for data analysis"
    )
    
    # Number of posts
    post_limit = st.sidebar.slider(
        "Number of Posts",
        min_value=10,
        max_value=500,
        value=100,
        step=10,
        help="Select the number of posts to analyze"
    )
    
    # Analysis options
    st.sidebar.subheader("Analysis Options")
    
    show_raw_data = st.sidebar.checkbox(
        "Show Raw Data",
        value=False,
        help="Display the raw data table"
    )
    
    show_sentiment = st.sidebar.checkbox(
        "Show Sentiment Analysis",
        value=True,
        help="Display sentiment analysis results"
    )
    
    show_trends = st.sidebar.checkbox(
        "Show Trends",
        value=True,
        help="Display trending topics"
    )
    
    num_ideas = st.sidebar.number_input(
        "Number of Ideas to Generate",
        min_value=1,
        max_value=10,
        value=5,
        help="Select the number of ideas to generate"
    )
    
    return {
        'subreddit': subreddit,
        'time_filter': time_filter,
        'post_limit': post_limit,
        'show_raw_data': show_raw_data,
        'show_sentiment': show_sentiment,
        'show_trends': show_trends,
        'num_ideas': num_ideas
    }
