#!/usr/bin/env python3
"""
Test script for the Story Teller AI Agent

This script provides a simple way to test the agent without command-line arguments.
"""

import os
import sys
from story_agent import StoryAgent


def test_agent():
    """Test the agent with a sample behavioral problem."""
    
    # Check if environment variables are set
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT", 
        "AZURE_SPEECH_KEY",
        "AZURE_SPEECH_REGION"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set up your Azure credentials as described in the README.md")
        return False
    
    # Test problem description
    test_problem = "My daughter won't share her favorite toy with her little brother"
    
    print("🧪 Testing Story Teller AI Agent...")
    print(f"📝 Test problem: {test_problem}")
    print()
    
    try:
        # Initialize and run the agent
        agent = StoryAgent()
        agent.run(test_problem)
        
        print("\n✅ Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_agent()
    sys.exit(0 if success else 1)
