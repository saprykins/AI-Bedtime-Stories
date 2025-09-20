"""
Tool 1: Text Analysis Tool

This tool analyzes a child's behavioral problem description and extracts
key information needed for story generation.
"""

import os
import json
from typing import Dict, Any, List
from openai import AzureOpenAI


class TextAnalysisTool:
    """
    Analyzes behavioral problem descriptions to extract:
    - Problem type (conflict, lying, not sharing, etc.)
    - Main character (animal placeholder for the child)
    - Moral of the story (lesson to be taught)
    """
    
    def __init__(self):
        """Initialize the text analysis tool with Azure OpenAI client."""
        try:
            self.client = self._get_azure_client()
        except Exception as e:
            print(f"⚠️  Azure OpenAI not available: {e}")
            self.client = None
        
        # Predefined character options for variety
        self.character_options = [
            "a brave little bear", "a curious rabbit", "a playful fox",
            "a gentle deer", "a clever owl", "a friendly squirrel",
            "a determined mouse", "a kind hedgehog", "a adventurous frog",
            "a wise turtle", "a energetic chipmunk", "a caring bunny"
        ]
    
    def _get_azure_client(self) -> AzureOpenAI:
        """Initialize Azure OpenAI client with credentials from environment."""
        try:
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            if not api_key or api_key == "your_openai_api_key_here":
                raise Exception("Azure OpenAI API key not configured")
                
            client = AzureOpenAI(
                api_key=api_key,
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
            )
            return client
        except Exception as e:
            raise Exception(f"Failed to initialize Azure OpenAI client: {str(e)}")
    
    def analyze_problem(self, problem_description: str) -> Dict[str, Any]:
        """
        Analyze the behavioral problem and extract key story elements.
        
        Args:
            problem_description: The child's behavioral problem description
            
        Returns:
            Dictionary containing problem_type, character, and moral
        """
        try:
            # Check if Azure client is available
            if self.client is None:
                print("⚠️  Azure OpenAI not configured. Using fallback analysis.")
                return self._analyze_problem_fallback(problem_description)
            # Create the analysis prompt
            analysis_prompt = self._create_analysis_prompt(problem_description)
            
            # Call Azure OpenAI to analyze the problem
            response = self.client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4"),
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert child psychologist and storyteller. Analyze behavioral problems and extract key elements for creating therapeutic children's stories."
                    },
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            # Parse the response
            analysis_text = response.choices[0].message.content.strip()
            analysis_result = self._parse_analysis_response(analysis_text)
            
            # Add character selection
            analysis_result["character"] = self._select_character(analysis_result.get("problem_type", ""))
            
            return analysis_result
            
        except Exception as e:
            raise Exception(f"Text analysis failed: {str(e)}")
    
    def _create_analysis_prompt(self, problem_description: str) -> str:
        """Create the prompt for analyzing the behavioral problem."""
        return f"""
Analyze this child behavioral problem and extract key information for creating a therapeutic story:

Problem: "{problem_description}"

Please provide a JSON response with the following structure:
{{
    "problem_type": "Brief description of the core behavioral issue (e.g., 'sharing conflict', 'lying', 'not listening', 'aggression')",
    "emotions": "Primary emotions involved (e.g., 'anger, frustration', 'fear, anxiety', 'sadness, loneliness')",
    "moral": "The main lesson the story should teach (e.g., 'the importance of sharing and friendship', 'honesty builds trust', 'listening shows respect')",
    "story_theme": "Suggested theme for the story (e.g., 'friendship and cooperation', 'honesty and trust', 'respect and listening')"
}}

Focus on:
1. Identifying the core behavioral issue
2. Understanding the underlying emotions
3. Determining the appropriate moral lesson
4. Suggesting a positive theme for the story

Make the moral lesson age-appropriate for children 4-8 years old.
"""
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the JSON response from the analysis."""
        try:
            # Try to extract JSON from the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")
            
            json_text = response_text[start_idx:end_idx]
            return json.loads(json_text)
            
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback parsing if JSON is malformed
            print(f"Warning: Could not parse JSON response, using fallback parsing: {e}")
            return self._fallback_parse(response_text)
    
    def _fallback_parse(self, response_text: str) -> Dict[str, Any]:
        """Fallback parsing when JSON parsing fails."""
        # Simple keyword-based fallback
        problem_type = "behavioral issue"
        emotions = "mixed emotions"
        moral = "the importance of good behavior"
        story_theme = "learning and growing"
        
        # Try to extract information using simple text analysis
        if "share" in response_text.lower():
            problem_type = "sharing conflict"
            moral = "the importance of sharing and friendship"
        elif "lie" in response_text.lower() or "honest" in response_text.lower():
            problem_type = "lying"
            moral = "honesty builds trust"
        elif "listen" in response_text.lower():
            problem_type = "not listening"
            moral = "listening shows respect"
        elif "fight" in response_text.lower() or "aggressive" in response_text.lower():
            problem_type = "aggression"
            moral = "kindness and peaceful resolution"
        
        return {
            "problem_type": problem_type,
            "emotions": emotions,
            "moral": moral,
            "story_theme": story_theme
        }
    
    def _select_character(self, problem_type: str) -> str:
        """Select an appropriate animal character based on the problem type."""
        import random
        
        # Character selection based on problem type
        if "share" in problem_type.lower():
            return random.choice(["a generous little bear", "a sharing rabbit", "a kind squirrel"])
        elif "lie" in problem_type.lower():
            return random.choice(["a truthful little fox", "an honest owl", "a trustworthy deer"])
        elif "listen" in problem_type.lower():
            return random.choice(["an attentive little mouse", "a respectful bunny", "a patient turtle"])
        elif "fight" in problem_type.lower() or "aggressive" in problem_type.lower():
            return random.choice(["a peaceful little bear", "a gentle deer", "a calm hedgehog"])
        else:
            return random.choice(self.character_options)
    
    def _analyze_problem_fallback(self, problem_description: str) -> Dict[str, Any]:
        """Fallback analysis when Azure OpenAI is not available."""
        problem_lower = problem_description.lower()
        
        # Simple keyword-based analysis
        if "share" in problem_lower or "sharing" in problem_lower:
            problem_type = "sharing conflict"
            emotions = "possessiveness, fear of loss"
            moral = "the importance of sharing and friendship"
            story_theme = "friendship and cooperation"
        elif "fight" in problem_lower or "fighting" in problem_lower or "aggressive" in problem_lower:
            problem_type = "aggression"
            emotions = "anger, frustration"
            moral = "kindness and peaceful resolution"
            story_theme = "peace and understanding"
        elif "lie" in problem_lower or "lying" in problem_lower or "honest" in problem_lower:
            problem_type = "lying"
            emotions = "fear, guilt"
            moral = "honesty builds trust"
            story_theme = "honesty and trust"
        elif "listen" in problem_lower or "listening" in problem_lower:
            problem_type = "not listening"
            emotions = "frustration, impatience"
            moral = "listening shows respect"
            story_theme = "respect and communication"
        else:
            problem_type = "behavioral challenge"
            emotions = "mixed emotions"
            moral = "the importance of good behavior"
            story_theme = "learning and growing"
        
        # Select appropriate character
        character = self._select_character(problem_type)
        
        return {
            "problem_type": problem_type,
            "emotions": emotions,
            "moral": moral,
            "story_theme": story_theme,
            "character": character
        }
