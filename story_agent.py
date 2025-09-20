#!/usr/bin/env python3
"""
Story Teller AI Agent

A goal-oriented AI agent that creates personalized children's stories
to help address behavioral problems through storytelling.

Usage:
    python story_agent.py "My son got into a fight at school because he didn't want to share a toy."
"""

import argparse
import sys
import os
from typing import Dict, Any
import json

# Load environment variables from .env file
def load_env_file():
    """Load environment variables from .env file if it exists."""
    env_file = '.env'
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value
        except UnicodeDecodeError:
            print("⚠️  .env file has encoding issues. Please check the file format.")
            print("💡 You can set environment variables directly or fix the .env file.")
        except Exception as e:
            print(f"⚠️  Error loading .env file: {e}")
            print("💡 You can set environment variables directly or check the .env file.")

# Load environment variables
load_env_file()

from tools.text_analysis import TextAnalysisTool
from tools.story_generation import StoryGenerationTool
from tools.text_to_speech import TextToSpeechTool


class StoryAgent:
    """
    Main orchestrator for the Story Teller AI Agent.
    
    This agent processes a child's behavioral problem and creates a personalized
    fairy tale to help teach appropriate behavior through storytelling.
    """
    
    def __init__(self):
        """Initialize the agent with its three core tools."""
        self.text_analyzer = TextAnalysisTool()
        self.story_generator = StoryGenerationTool()
        self.tts_engine = TextToSpeechTool()
    
    def process_request(self, user_prompt: str) -> str:
        """
        Process a user's request through the three-tool pipeline.
        
        Args:
            user_prompt: Description of the child's behavioral problem
            
        Returns:
            Path to the generated audio file
        """
        print("🎭 Story Teller AI Agent starting...")
        print(f"📝 Processing: {user_prompt}")
        print()
        
        # Tool 1: Analyze the text and extract key information
        print("🔍 Tool 1: Analyzing the problem...")
        analysis_result = self.text_analyzer.analyze_problem(user_prompt)
        print(f"✅ Analysis complete: {analysis_result['problem_type']} - {analysis_result['moral']}")
        print()
        
        # Tool 2: Generate the story based on analysis
        print("📚 Tool 2: Generating personalized story...")
        story_text = self.story_generator.generate_story(analysis_result)
        print("✅ Story generated successfully")
        print()
        
        # Tool 3: Convert story to speech
        print("🎵 Tool 3: Converting story to audio...")
        audio_file_path = self.tts_engine.text_to_speech(story_text)
        print(f"✅ Audio saved to: {audio_file_path}")
        print()
        
        return audio_file_path
    
    def run(self, user_prompt: str) -> None:
        """
        Main entry point for the agent.
        
        Args:
            user_prompt: The behavioral problem description
        """
        try:
            audio_path = self.process_request(user_prompt)
            print("🎉 Story generated and saved successfully!")
            print(f"📁 Audio file: {audio_path}")
            print("\n💡 Tip: Play the audio file to share the story with your child!")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("Please check your Azure credentials and try again.")
            sys.exit(1)


def main():
    """Main function to handle command-line interface."""
    parser = argparse.ArgumentParser(
        description="Story Teller AI Agent - Generate personalized children's stories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python story_agent.py "My daughter won't clean her room"
  python story_agent.py "My son keeps interrupting when adults are talking"
  python story_agent.py "My child refuses to eat vegetables"
        """
    )
    
    parser.add_argument(
        "problem_description",
        help="Description of the child's behavioral problem"
    )
    
    parser.add_argument(
        "--output-dir",
        default="./output",
        help="Directory to save the generated audio file (default: ./output)"
    )
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Set the output directory environment variable
    os.environ["OUTPUT_DIR"] = args.output_dir
    
    # Initialize and run the agent
    agent = StoryAgent()
    agent.run(args.problem_description)


if __name__ == "__main__":
    main()
