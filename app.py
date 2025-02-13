import streamlit as st
from utils.reddit_client import RedditClient
from utils.nlp_processor import NLPProcessor
from utils.data_processor import DataProcessor
from utils.auth import check_password
from components.sidebar import render_sidebar
from components.visualizations import (
    plot_sentiment_distribution,
    plot_trending_topics,
    plot_engagement_metrics
)
from components.idea_generator import (
    display_ideas,
    display_trend_analysis,
    display_export_options
)

# Page configuration
st.set_page_config(
    page_title="Aaron's AI Idea Generator",
    page_icon="💡",
    layout="wide"
)

# Initialize components
reddit_client = RedditClient()
nlp_processor = NLPProcessor()
data_processor = DataProcessor()

# Main application
def main():
    if not check_password():
        return

    st.title("💡 Aaron's AI-Powered Idea Generator")
    st.markdown("""
    Discover innovative business ideas powered by DeepSeek AI, analyzing Reddit discussions and trends.
    Use the sidebar to customize your analysis.
    """)

    # Render sidebar and get settings
    settings = render_sidebar()

    # Fetch and process data
    with st.spinner("Fetching and analyzing data..."):
        df = reddit_client.fetch_subreddit_data(
            settings['subreddit'],
            settings['time_filter'],
            settings['post_limit']
        )

        if not df.empty:
            df = nlp_processor.process_dataframe(df)
            trends_df = data_processor.identify_trends(df)

            # Get deep analysis and ideas
            deep_analysis = data_processor.analyze_deep_trends(df)
            ideas = data_processor.generate_ideas(trends_df, settings['num_ideas'])

            # Display raw data if selected
            if settings['show_raw_data']:
                st.subheader("📊 Raw Data")
                st.dataframe(df)

            # Create three columns for metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Posts Analyzed", len(df))
            with col2:
                st.metric("Average Sentiment", f"{df['sentiment'].mean():.2f}")
            with col3:
                st.metric("Trending Topics", len(trends_df))

            # Display visualizations
            if settings['show_sentiment']:
                st.subheader("📈 Sentiment Analysis")
                plot_sentiment_distribution(df)
                plot_engagement_metrics(df)

            if settings['show_trends']:
                st.subheader("📊 Trend Analysis")
                plot_trending_topics(trends_df)
                display_trend_analysis(deep_analysis)

            # Display generated ideas
            display_ideas(ideas)

            # Export options
            export_data = data_processor.prepare_export_data(df, trends_df, deep_analysis)
            display_export_options(export_data)
        else:
            st.error("No data available. Please check your settings and try again.")

if __name__ == "__main__":
    main()