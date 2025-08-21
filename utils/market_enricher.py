import json
from typing import Dict, List, Any

class MarketEnricher:
    def __init__(self, deepseek_client):
        self.client = deepseek_client
    
    def batch_enrich_ideas(self, ideas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Batch enrich ideas to avoid rate limiting."""
        
        system_prompt = """You are a YC-tier startup analyst. For each business idea provided, enrich it with essential market intelligence.
Return ONLY a valid JSON object with a single key "enriched_ideas", which is a list of JSON objects, each corresponding to an original idea.
Each object must have this exact structure:
{
    "original_idea": "The original idea description",
    "market_analysis": { "tam": "...", "cagr": "..." },
    "competitive_landscape": { "differentiator": "..." }
}"""

        user_prompt = f"""Analyze these business ideas and provide comprehensive market intelligence for each:
{json.dumps(ideas, indent=2)}
"""

        try:
            response = self.client.client.chat.completions.create(
                model=self.client.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                top_p=0.8,
            )

            content = response.choices[0].message.content.strip()
            
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                try:
                    enrichment_data = json.loads(json_str).get("enriched_ideas", [])
                    
                    # Merge with original ideas
                    for i, original_idea in enumerate(ideas):
                        if i < len(enrichment_data):
                            ideas[i] = {**original_idea, **enrichment_data[i]}
                    return ideas
                except json.JSONDecodeError:
                    # Fallback for malformed JSON
                    for idea in ideas:
                        idea['market_analysis'] = {'tam': 'Analysis Failed', 'cagr': 'N/A'}
                        idea['competitive_landscape'] = {'differentiator': 'Analysis Failed'}
                    return ideas
            
            return ideas
            
        except Exception as e:
            print(f"Warning: Market enrichment failed: {str(e)}")
            return ideas

    def batch_get_detailed_analysis(self, ideas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Batch get detailed market and competitor analysis for multiple ideas."""
        
        system_prompt = """You are a YC-tier startup analyst. For each business idea provided, provide detailed market and competitor analysis.
Return ONLY a valid JSON object with a single key "detailed_analysis", which is a list of JSON objects, each corresponding to an original idea.
Each object must have this exact structure:
{
    "original_idea": "The original idea description",
    "market_analysis": { "tam": "...", "cagr": "...", "market_trends": [...] },
    "competitive_landscape": { "direct_competitors": [...], "indirect_competitors": [...], "differentiator": "..." }
}"""

        user_prompt = f"""Analyze these business ideas and provide detailed market and competitor analysis for each:
{json.dumps(ideas, indent=2)}
"""

        try:
            response = self.client.client.chat.completions.create(
                model=self.client.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                top_p=0.8,
            )

            content = response.choices[0].message.content.strip()
            
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                try:
                    return json.loads(json_str).get("detailed_analysis", [])
                except json.JSONDecodeError:
                    return []
            
            return []
            
        except Exception as e:
            print(f"Warning: Detailed analysis failed: {str(e)}")
            return []

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