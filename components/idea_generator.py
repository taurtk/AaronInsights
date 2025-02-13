import streamlit as st
import json

def display_ideas(ideas):
    """Display generated business ideas"""
    st.subheader("💡 AI-Generated Business Ideas")

    for i, idea in enumerate(ideas, 1):
        with st.container():
            try:
                # Try to parse as JSON if it's a string
                if isinstance(idea, str):
                    idea_data = json.loads(idea)
                else:
                    idea_data = idea

                # Create an expander for each idea
                with st.expander(f"Idea #{i}: {idea_data.get('problem', 'New Business Opportunity')}"):
                    if 'problem' in idea_data:
                        st.markdown("**🎯 Problem Statement**")
                        st.write(idea_data['problem'])

                    if 'solution' in idea_data:
                        st.markdown("**💡 Proposed Solution**")
                        st.write(idea_data['solution'])

                    if 'target_market' in idea_data:
                        st.markdown("**👥 Target Market**")
                        st.write(idea_data['target_market'])

                    if 'features' in idea_data:
                        st.markdown("**⚡ Key Features**")
                        st.write(idea_data['features'])

                    # If it's a simple idea format
                    if 'idea' in idea_data:
                        st.write(idea_data['idea'])

            except (json.JSONDecodeError, AttributeError):
                # Fallback for simple string format
                st.markdown(
                    f"""
                    <div style="
                        padding: 1rem;
                        border-radius: 0.5rem;
                        background-color: #f0f2f6;
                        margin-bottom: 1rem;
                    ">
                        <p style="margin: 0.5rem 0 0 0;">{str(idea)}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

def display_trend_analysis(analysis_data):
    """Display deep trend analysis"""
    if not analysis_data:
        return

    st.subheader("📊 Deep Trend Analysis")

    try:
        # Try to parse as JSON if it's a string
        if isinstance(analysis_data, str):
            analysis = json.loads(analysis_data)
        else:
            analysis = analysis_data

        col1, col2 = st.columns(2)

        with col1:
            if 'market_trends' in analysis:
                st.markdown("**📈 Market Trends**")
                for trend in analysis['market_trends']:
                    st.write(f"- {trend}")

            if 'pain_points' in analysis:
                st.markdown("**❗ User Pain Points**")
                for point in analysis['pain_points']:
                    st.write(f"- {point}")

        with col2:
            if 'opportunities' in analysis:
                st.markdown("**🎯 Opportunities**")
                for opp in analysis['opportunities']:
                    st.write(f"- {opp}")

            if 'themes' in analysis:
                st.markdown("**🔄 Common Themes**")
                for theme in analysis['themes']:
                    st.write(f"- {theme}")

    except (json.JSONDecodeError, AttributeError):
        st.write(str(analysis_data))

def display_export_options(export_data):
    """Display export options for generated ideas"""
    st.subheader("📤 Export Options")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Export as CSV"):
            st.download_button(
                label="Download CSV",
                data=str(export_data),
                file_name="idea_generation_report.csv",
                mime="text/csv"
            )

    with col2:
        if st.button("Export as JSON"):
            st.download_button(
                label="Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name="idea_generation_report.json",
                mime="application/json"
            )