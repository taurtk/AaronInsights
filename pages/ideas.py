import streamlit as st
import pandas as pd

st.set_page_config(page_title="Generated Ideas", page_icon="💭")

st.title("💭 Generated Ideas")

# Get data from session state
if all(key in st.session_state for key in ['reddit_analyzer', 'nlp_processor', 'idea_generator']):
    analyzer = st.session_state.reddit_analyzer
    nlp = st.session_state.nlp_processor
    generator = st.session_state.idea_generator
    
    try:
        # Fetch fresh data
        posts = analyzer.fetch_posts("startups", "month", 50)
        
        # Extract keywords
        keywords = nlp.extract_keywords(
            [post['title'] + " " + post['selftext'] for post in posts]
        )
        
        # Generate ideas
        ideas = generator.generate_ideas(posts, keywords)
        
        # Display ideas
        for i, idea in enumerate(ideas, 1):
            with st.expander(f"Idea {i}: Based on {idea['problem'][:100]}..."):
                st.write("**Problem Identified:**")
                st.write(idea['problem'])
                
                st.write("**Potential Solution:**")
                st.write(idea['potential_solution'])
                
                st.write("**Relevance Score:**", idea['relevance_score'])
                
                # Add action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Save Idea {i}", key=f"save_{i}"):
                        st.success("Idea saved! (Feature to be implemented)")
                with col2:
                    if st.button(f"Refine Idea {i}", key=f"refine_{i}"):
                        st.info("Refinement feature coming soon!")
        
        # Export all ideas
        if st.button("Export All Ideas"):
            ideas_df = pd.DataFrame(ideas)
            csv = ideas_df.to_csv(index=False)
            st.download_button(
                label="Download Ideas CSV",
                data=csv,
                file_name="generated_ideas.csv",
                mime="text/csv"
            )
            
    except Exception as e:
        st.error(f"Error generating ideas: {str(e)}")
else:
    st.warning("Please run the main page first to initialize the analyzers.")
