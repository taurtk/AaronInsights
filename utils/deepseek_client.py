import os
import openai
import streamlit as st
import json

class DeepSeekClient:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key="301a3eec-c4c9-4920-836e-7fdc0b3639d4",
            base_url="https://api.sambanova.ai/v1",
        )

    @st.cache_data(ttl=3600)
    def generate_business_ideas(_self, trends_data, num_ideas=5):
        """Generate business ideas using DeepSeek"""
        try:
            # Prepare context from trends data
            trends_context = "\n".join([
                f"- {trend['keyword']} (frequency: {trend['frequency']}, sentiment: {trend['avg_sentiment']:.2f})"
                for trend in trends_data.head(10).to_dict('records')
            ])

            system_prompt = """You are an expert business consultant and idea generator. Your task is to analyze market trends and generate innovative business ideas in a structured JSON format. Each idea must include:
1. A clear problem statement
2. A detailed solution
3. A specific target market
4. Key features
Always return exactly the requested number of ideas in a valid JSON array."""

            user_prompt = f"""Based on these market trends and user discussions:
{trends_context}

Generate exactly {num_ideas} structured business ideas.
Return them in this exact JSON format:
[
    {{
        "problem": "A clear and specific problem statement",
        "solution": "A detailed description of how the solution works",
        "target_market": "Specific description of who will use this",
        "features": ["Key feature 1", "Key feature 2", "Key feature 3"]
    }},
    ...
]

Important:
- Return exactly {num_ideas} ideas
- Ensure each idea is detailed and specific
- Keep the JSON structure exactly as shown
- Make sure the response is valid JSON"""

            response = _self.client.chat.completions.create(
                model="DeepSeek-R1-Distill-Llama-70B",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                top_p=0.9,
            )

            # Parse and validate response
            content = response.choices[0].message.content.strip()
            try:
                # Try to find JSON array in the response
                start_idx = content.find('[')
                end_idx = content.rfind(']') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = content[start_idx:end_idx]
                    ideas = json.loads(json_str)
                    if isinstance(ideas, list):
                        # Ensure exactly num_ideas are returned
                        if len(ideas) > num_ideas:
                            ideas = ideas[:num_ideas]
                        elif len(ideas) < num_ideas:
                            # Pad with placeholder ideas if needed
                            while len(ideas) < num_ideas:
                                ideas.append({
                                    "problem": "Additional opportunity identified",
                                    "solution": "Analysis in progress",
                                    "target_market": "Market research ongoing",
                                    "features": ["Feature analysis pending"]
                                })
                        return ideas

                # Fallback for invalid JSON array
                raise json.JSONDecodeError("Invalid JSON array", content, 0)

            except json.JSONDecodeError:
                st.warning("⚠️ The AI response format was unexpected. Retrying with simplified format...")
                # Retry with more basic prompt
                retry_response = _self.client.chat.completions.create(
                    model="DeepSeek-R1-Distill-Llama-70B",
                    messages=[
                        {"role": "system", "content": "Generate simple business ideas in JSON format."},
                        {"role": "user", "content": f"Generate {num_ideas} business ideas based on these trends: {trends_context}"}
                    ],
                    temperature=0.5,
                )

                try:
                    retry_content = retry_response.choices[0].message.content
                    # Try to extract any JSON-like content
                    ideas = []
                    lines = retry_content.split('\n')
                    for i in range(min(num_ideas, len(lines))):
                        ideas.append({
                            "problem": f"Trend Analysis #{i+1}",
                            "solution": lines[i].strip(),
                            "target_market": "Market analysis in progress",
                            "features": ["Detailed features coming soon"]
                        })
                    return ideas
                except Exception:
                    return [{
                        "problem": "AI Response Processing Error",
                        "solution": "Our AI service is currently experiencing issues with response formatting",
                        "target_market": "Please try again in a few moments",
                        "features": ["System will retry automatically"]
                    }] * num_ideas

        except Exception as e:
            st.error(f"Error generating ideas: {str(e)}")
            return [{
                "problem": "Service Temporarily Unavailable",
                "solution": "We're experiencing technical difficulties",
                "target_market": "Please try again later",
                "features": ["Service will be restored shortly"]
            }] * num_ideas

    def analyze_trends(_self, posts_data):
        """Analyze trends using DeepSeek for deeper insights"""
        try:
            combined_text = "\n".join([
                f"Title: {post['title']}\nText: {post['text']}\n"
                for post in posts_data.head(10).to_dict('records')
            ])

            system_prompt = """You are an expert market analyst. Analyze the provided content and return insights in valid JSON format with these exact categories:
- market_trends: List of emerging market trends
- pain_points: List of user problems and challenges
- opportunities: List of potential business opportunities
- themes: List of common themes or patterns"""

            user_prompt = f"""Analyze these Reddit posts and provide structured insights:

{combined_text}

Return the analysis in this exact JSON format:
{{
    "market_trends": ["trend 1", "trend 2", "trend 3"],
    "pain_points": ["pain point 1", "pain point 2", "pain point 3"],
    "opportunities": ["opportunity 1", "opportunity 2", "opportunity 3"],
    "themes": ["theme 1", "theme 2", "theme 3"]
}}"""

            response = _self.client.chat.completions.create(
                model="DeepSeek-R1-Distill-Llama-70B",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,
                top_p=0.8,
            )

            try:
                content = response.choices[0].message.content.strip()
                # Try to find JSON object in the response
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = content[start_idx:end_idx]
                    return json.loads(json_str)
                raise json.JSONDecodeError("Invalid JSON object", content, 0)
            except json.JSONDecodeError:
                return {
                    "market_trends": ["Currently analyzing market trends..."],
                    "pain_points": ["Processing user feedback..."],
                    "opportunities": ["Identifying business opportunities..."],
                    "themes": ["Extracting common themes..."]
                }

        except Exception as e:
            st.error(f"Error analyzing trends: {str(e)}")
            return {
                "market_trends": ["Analysis temporarily unavailable"],
                "pain_points": ["Service disruption"],
                "opportunities": ["Please try again later"],
                "themes": ["System recovery in progress"]
            }