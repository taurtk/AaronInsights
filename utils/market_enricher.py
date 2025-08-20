import json
import streamlit as st
from typing import Dict, List, Any

class MarketEnricher:
    def __init__(self, deepseek_client):
        self.client = deepseek_client
    
    @st.cache_data(ttl=7200)
    def enrich_idea_with_market_data(_self, idea: Dict[str, Any]) -> Dict[str, Any]:
        """Auto-enrich idea with market size, competitors, monetization, and roadmaps"""
        
        system_prompt = """You are a YC-tier startup analyst. Enrich business ideas with comprehensive market intelligence.
Return ONLY valid JSON with this exact structure:
{
    "market_analysis": {
        "tam": "Total Addressable Market estimate with source reasoning",
        "cagr": "Compound Annual Growth Rate estimate with timeframe",
        "market_trends": ["trend1", "trend2", "trend3"]
    },
    "competitive_landscape": {
        "direct_competitors": [{"name": "CompanyName", "description": "What they do"}],
        "indirect_competitors": [{"name": "CompanyName", "description": "What they do"}],
        "differentiator": "Key competitive advantage"
    },
    "monetization": {
        "primary_model": "Main revenue model",
        "secondary_models": ["model1", "model2"],
        "pricing_strategy": "Pricing approach",
        "revenue_streams": ["stream1", "stream2"]
    },
    "roadmaps": {
        "hackathon_mvp": {
            "timeline": "2-4 weeks",
            "milestones": ["milestone1", "milestone2", "milestone3"]
        },
        "investor_pitch": {
            "timeline": "3-6 months", 
            "milestones": ["milestone1", "milestone2", "milestone3", "milestone4"]
        }
    }
}"""

        user_prompt = f"""Analyze this business idea and provide comprehensive market intelligence:

Problem: {idea.get('problem', 'N/A')}
Solution: {idea.get('solution', 'N/A')}
Target Market: {idea.get('target_market', 'N/A')}

Provide realistic market data, real competitor examples, viable monetization models, and actionable roadmaps."""

        try:
            response = _self.client.client.chat.completions.create(
                model=_self.client.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                top_p=0.8,
            )

            content = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                enrichment_data = json.loads(json_str)
                
                # Merge with original idea
                enriched_idea = {**idea, **enrichment_data}
                return enriched_idea
            
            return idea
            
        except Exception as e:
            st.warning(f"Market enrichment failed: {str(e)}")
            return idea

    def format_market_display(self, enriched_idea: Dict[str, Any]) -> str:
        """Format enriched data for display"""
        if not enriched_idea.get('market_analysis'):
            return ""
            
        market = enriched_idea.get('market_analysis', {})
        competitive = enriched_idea.get('competitive_landscape', {})
        monetization = enriched_idea.get('monetization', {})
        roadmaps = enriched_idea.get('roadmaps', {})
        
        display_html = f"""
        <div style="background: linear-gradient(145deg, #f8fafc 0%, #e2e8f0 100%); padding: 1.5rem; border-radius: 15px; margin: 1rem 0;">
            <h4 style="color: #2d3748; margin-bottom: 1rem;">📊 Market Intelligence</h4>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <h5 style="color: #4a5568; margin-bottom: 0.5rem;">🎯 Market Size</h5>
                    <p style="margin: 0.25rem 0; font-size: 0.9rem;"><strong>TAM:</strong> {market.get('tam', 'Analyzing...')}</p>
                    <p style="margin: 0.25rem 0; font-size: 0.9rem;"><strong>Growth:</strong> {market.get('cagr', 'Calculating...')}</p>
                </div>
                
                <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <h5 style="color: #4a5568; margin-bottom: 0.5rem;">💰 Revenue Model</h5>
                    <p style="margin: 0.25rem 0; font-size: 0.9rem;"><strong>Primary:</strong> {monetization.get('primary_model', 'TBD')}</p>
                    <p style="margin: 0.25rem 0; font-size: 0.9rem;"><strong>Pricing:</strong> {monetization.get('pricing_strategy', 'TBD')}</p>
                </div>
            </div>
            
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h5 style="color: #4a5568; margin-bottom: 0.5rem;">🏆 Competitive Edge</h5>
                <p style="margin: 0; font-size: 0.9rem;">{competitive.get('differentiator', 'Unique value proposition to be defined')}</p>
            </div>
        </div>
        """
        
        return display_html

    def get_roadmap_data(self, enriched_idea: Dict[str, Any]) -> Dict[str, Any]:
        """Extract roadmap data for detailed view"""
        return enriched_idea.get('roadmaps', {
            'hackathon_mvp': {
                'timeline': '2-4 weeks',
                'milestones': ['Define core features', 'Build MVP', 'Test with users']
            },
            'investor_pitch': {
                'timeline': '3-6 months',
                'milestones': ['Market validation', 'Product development', 'User acquisition', 'Pitch preparation']
            }
        })