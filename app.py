import streamlit as st
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

# Enhanced CSS for beautiful modern design
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%, #f093fb 200%);
    padding: 3rem 2rem;
    border-radius: 20px;
    margin-bottom: 3rem;
    text-align: center;
    color: white;
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(180deg); }
}

.main-header h1 {
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    text-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.main-header p {
    font-size: 1.2rem;
    font-weight: 300;
    opacity: 0.9;
    margin: 0.5rem 0;
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.95);
    border: 2px solid transparent;
    border-radius: 15px;
    padding: 1rem 1.5rem;
    font-size: 1.1rem;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus {
    border-color: #667eea;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    transform: translateY(-2px);
}

.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 1rem 3rem;
    font-weight: 600;
    font-size: 1.1rem;
    width: 100%;
    transition: all 0.3s ease;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
}

.unique-idea {
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
    padding: 2rem;
    border-radius: 20px;
    border: 1px solid rgba(102, 126, 234, 0.1);
    margin: 1.5rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.unique-idea::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.unique-idea:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.12);
}

.tag {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
    margin: 0.5rem 0.5rem 0.5rem 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.reddit-tag { 
    background: linear-gradient(135deg, #ff4500 0%, #ff6b35 100%);
    color: white;
    box-shadow: 0 4px 15px rgba(255, 69, 0, 0.3);
}

.quora-tag { 
    background: linear-gradient(135deg, #b92b27 0%, #d63384 100%);
    color: white;
    box-shadow: 0 4px 15px rgba(185, 43, 39, 0.3);
}

.unique-idea h5 {
    color: #2d3748;
    font-size: 1.3rem;
    font-weight: 600;
    margin: 1rem 0;
}

.unique-idea p {
    color: #4a5568;
    font-size: 1rem;
    line-height: 1.6;
    margin: 0;
}

.example-button {
    background: linear-gradient(145deg, #f7fafc 0%, #edf2f7 100%);
    border: 2px solid #e2e8f0;
    border-radius: 15px;
    padding: 1rem;
    margin: 0.5rem 0;
    transition: all 0.3s ease;
    cursor: pointer;
    text-align: center;
    font-weight: 500;
}

.example-button:hover {
    background: linear-gradient(145deg, #667eea 0%, #764ba2 100%);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.loading-container {
    text-align: center;
    padding: 2rem;
    background: linear-gradient(145deg, #f7fafc 0%, #edf2f7 100%);
    border-radius: 20px;
    margin: 2rem 0;
}

.pulse {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}

.stSpinner {
    text-align: center;
    padding: 2rem;
}

.ideas-header {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 15px;
    margin: 2rem 0 1rem 0;
    text-align: center;
    box-shadow: 0 8px 25px rgba(240, 147, 251, 0.3);
}

.ideas-count {
    background: rgba(255,255,255,0.2);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    display: inline-block;
    margin-top: 0.5rem;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# Initialize components
reddit_client = RedditClient()
quora_client = QuoraClient()
deepseek_client = DeepSeekClient()

# Main application
def main():
    # Enhanced Header
    st.markdown("""
    <div class="main-header">
        <h1>✨ NicheGenius</h1>
        <p>AI-Powered Niche Product Idea Generator</p>
        <p>Discover untapped market opportunities and innovative business ideas</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Input section
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h3 style="color: #2d3748; font-weight: 600; margin-bottom: 1rem;">🎯 What's your interest area?</h3>
        </div>
        """, unsafe_allow_html=True)
        prompt = st.text_input(
            "Enter your topic:", 
            placeholder="e.g., sustainable living, remote work, fitness tech...",
            label_visibility="collapsed"
        )

    if st.button("Generate Ideas"):
        if prompt:
            with st.spinner("⏳ Loading ideas... This may take up to 1 minute"):
                queries = deepseek_client.generate_search_queries(prompt)

                # Check if queries were generated successfully
                if not queries['subreddits'] and not queries['quora']:
                    st.error("🚫 Failed to generate search queries. Please try a different topic.")
                    return
                reddit_data = reddit_client.fetch_subreddit_data(queries['subreddits'])
                quora_data = quora_client.fetch_quora_data(queries['quora'])
                
                combined_data = reddit_data + quora_data
                
                # Generate ideas with source tracking
                unique_ideas = deepseek_client.generate_unique_ideas(prompt, combined_data, 20)
                
                if unique_ideas:
                    reddit_count = sum(1 for idea in unique_ideas if idea['source'] == 'reddit')
                    quora_count = sum(1 for idea in unique_ideas if idea['source'] == 'quora')
                    
                    st.markdown(f"""
                    <div class="ideas-header">
                        <h3>💡 {len(unique_ideas)} Unique Business Ideas</h3>
                        <div class="ideas-count">
                            🔴 Reddit: {reddit_count} | 🟣 Quora: {quora_count}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
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
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(145deg, #f7fafc 0%, #edf2f7 100%); border-radius: 20px; margin: 2rem 0;">
                <h4 style="color: #4a5568; margin-bottom: 1rem;">💭 Ready to discover your next big idea?</h4>
                <p style="color: #718096;">Enter a topic above to discover niche product opportunities!</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced example topics
            st.markdown("""
            <div style="text-align: center; margin: 3rem 0 2rem 0;">
                <h3 style="color: #2d3748; font-weight: 600;">🌟 Popular Topics</h3>
                <p style="color: #718096; margin-bottom: 2rem;">Click any topic to get started instantly</p>
            </div>
            """, unsafe_allow_html=True)
            
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