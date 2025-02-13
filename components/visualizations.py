import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def plot_sentiment_distribution(df):
    """Plot sentiment distribution"""
    fig = px.histogram(
        df,
        x='sentiment',
        nbins=20,
        title='Sentiment Distribution',
        labels={'sentiment': 'Sentiment Score', 'count': 'Number of Posts'},
        color_discrete_sequence=['#FF4B4B']
    )
    
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_trending_topics(trends_df):
    """Plot trending topics"""
    fig = px.bar(
        trends_df.head(10),
        x='keyword',
        y='frequency',
        title='Top 10 Trending Topics',
        labels={'keyword': 'Topic', 'frequency': 'Frequency'},
        color='avg_sentiment',
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_engagement_metrics(df):
    """Plot post engagement metrics"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['created_utc'],
        y=df['score'],
        name='Score',
        mode='markers',
        marker=dict(size=8, color='#FF4B4B')
    ))
    
    fig.add_trace(go.Scatter(
        x=df['created_utc'],
        y=df['comments'],
        name='Comments',
        mode='markers',
        marker=dict(size=8, color='#0068C9')
    ))
    
    fig.update_layout(
        title='Post Engagement Over Time',
        xaxis_title='Date',
        yaxis_title='Count',
        plot_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
