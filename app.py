import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
from utils.reddit_client import RedditClient
from utils.quora_client import QuoraClient
from utils.deepseek_client import DeepSeekClient

# Page configuration
st.set_page_config(
    page_title="NicheGenius - AI Idea Generator",
    page_icon="🚀",
    layout="centered"
)

# Hide sidebar completely
st.markdown("""
<style>
[data-testid="stSidebar"] {display: none;}
.css-1d391kg {display: none;}
.css-1rs6os {display: none;}
.css-17eq0hr {display: none;}
</style>
""", unsafe_allow_html=True)

# Custom CSS for modern design
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
}
.idea-card {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #667eea;
    margin: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.metric-container {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    text-align: center;
}
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    width: 100%;
}
.data-card {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    margin: 0.5rem 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.tag {
    display: inline-block;
    background: #667eea;
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 12px;
    font-size: 0.8rem;
    margin: 0.2rem;
}
.reddit-tag { background: #ff4500; }
.quora-tag { background: #b92b27; }
.unique-idea {
    background: white;
    padding: 1.2rem;
    border-radius: 8px;
    border-left: 3px solid #667eea;
    margin: 0.8rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# Initialize components
reddit_client = RedditClient()
quora_client = QuoraClient()
deepseek_client = DeepSeekClient()

# Main application
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 NicheGenius</h1>
        <p>AI-Powered Niche Product Idea Generator</p>
        <p>Discover untapped market opportunities and innovative business ideas</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🎯 What's your interest area?")
        prompt = st.text_input(
            "Enter your topic:", 
            placeholder="e.g., sustainable living, remote work, fitness tech...",
            label_visibility="collapsed"
        )

    if st.button("Generate Ideas"):
        if prompt:
            with st.spinner("🔍 Analyzing market trends..."):
                queries = deepseek_client.generate_search_queries(prompt)

            # Check if queries were generated successfully
            if not queries['subreddits'] and not queries['quora']:
                st.error("🚫 Failed to generate search queries. Please try a different topic.")
                return
            
            # Show generated queries in expandable section
            with st.expander("🔍 View Generated Search Queries"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Reddit Subreddits:**")
                    for sub in queries['subreddits']:
                        st.markdown(f"• r/{sub}")
                with col2:
                    st.markdown("**Quora Topics:**")
                    for query in queries['quora'][:5]:  # Limit display
                        st.markdown(f"• {query[:50]}..." if len(query) > 50 else f"• {query}")

            with st.spinner("🚀 Generating unique business ideas..."):
                reddit_data = reddit_client.fetch_subreddit_data(queries['subreddits'])
                quora_data = quora_client.fetch_quora_data(queries['quora'])
                
                # Generate ideas with source tracking
                unique_ideas = deepseek_client.generate_unique_ideas(prompt, reddit_data, quora_data, 50)
                
                if unique_ideas:
                    reddit_count = sum(1 for idea in unique_ideas if idea['source'] == 'reddit')
                    quora_count = sum(1 for idea in unique_ideas if idea['source'] == 'quora')
                    
                    st.markdown(f"### 💡 {len(unique_ideas)} Unique Business Ideas")
                    st.markdown(f"**🔴 Reddit Ideas: {reddit_count} | 🔴 Quora Ideas: {quora_count}**")
                    
                    for i, idea_data in enumerate(unique_ideas, 1):
                        source_tag = 'reddit-tag' if idea_data['source'] == 'reddit' else 'quora-tag'
                        st.markdown(f'''
                        <div class="unique-idea">
                            <span class="tag {source_tag}">{idea_data['source'].title()}</span>
                            <h5>💡 Idea #{i}</h5>
                            <p>{idea_data['idea']}</p>
                        </div>
                        ''', unsafe_allow_html=True)
                    

                else:
                    st.error("🚫 No data found for the given topic. Try a different search term.")
        else:
            st.info("💭 Enter a topic above to discover niche product opportunities!")
            
            # Show example topics
            st.markdown("### 🌟 Popular Topics")
            example_cols = st.columns(3)
            examples = [
                "🌱 Sustainable Living", "💻 Remote Work Tools", "🏋️ Fitness Tech",
                "🎨 Creative Hobbies", "🏠 Smart Home", "📚 Online Learning"
            ]
            for i, example in enumerate(examples):
                with example_cols[i % 3]:
                    if st.button(example, key=f"example_{i}"):
                        st.rerun()

if __name__ == "__main__":
    main()