#!/usr/bin/env python3
"""
Test script for Quora client functionality
"""

from utils.quora_client import QuoraClient

def test_quora_client():
    """Test the Quora client"""
    print("Testing Quora Client...")
    
    client = QuoraClient()
    
    # Test startup ideas search
    print("\n1. Fetching startup ideas...")
    ideas = client.search_startup_ideas(limit=5)
    
    if ideas:
        print(f"Found {len(ideas)} startup ideas:")
        for i, idea in enumerate(ideas, 1):
            print(f"{i}. {idea['title']}")
            print(f"   Category: {idea['category']}")
            print(f"   Source: {idea['source']}")
            print()
    else:
        print("No ideas found")
    
    # Test trending topics
    print("2. Fetching trending topics...")
    topics = client.get_trending_startup_topics()
    print(f"Found {len(topics)} trending topics:")
    for topic in topics:
        print(f"- {topic}")

if __name__ == "__main__":
    test_quora_client()