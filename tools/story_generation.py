"""
Tool 2: Story Generation Tool

This tool generates personalized children's fairy tales based on the analysis
from the Text Analysis Tool.
"""

import os
from typing import Dict, Any
from openai import AzureOpenAI


class StoryGenerationTool:
    """
    Generates personalized children's fairy tales that teach moral lessons
    through storytelling without being accusatory or direct.
    """
    
    def __init__(self):
        """Initialize the story generation tool with Azure OpenAI client."""
        try:
            self.client = self._get_azure_client()
        except Exception as e:
            print(f"⚠️  Azure OpenAI not available: {e}")
            self.client = None
    
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
    
    def generate_story(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generate a personalized children's story based on the analysis.
        
        Args:
            analysis_result: Dictionary containing problem_type, character, moral, etc.
            
        Returns:
            The complete story text
        """
        try:
            # Check if Azure client is available
            if self.client is None:
                print("⚠️  Azure OpenAI not configured. Using fallback story generation.")
                return self._generate_fallback_story(analysis_result)
            # Create the story generation prompt
            story_prompt = self._create_story_prompt(analysis_result)
            
            # Call Azure OpenAI to generate the story
            response = self.client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4"),
                messages=[
                    {
                        "role": "system",
                        "content": """You are a master storyteller who creates enchanting children's fairy tales. 
                        Your stories are:
                        - Age-appropriate for children 4-8 years old
                        - Non-accusatory and gentle in teaching lessons
                        - Engaging with vivid imagery and simple language
                        - Positive and uplifting with happy endings
                        - Subtle in delivering moral lessons through story events
                        
                        Write stories that feel magical and entertaining while naturally teaching important life lessons."""
                    },
                    {
                        "role": "user",
                        "content": story_prompt
                    }
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            story_text = response.choices[0].message.content.strip()
            
            # Clean and format the story
            formatted_story = self._format_story(story_text)
            
            return formatted_story
            
        except Exception as e:
            raise Exception(f"Story generation failed: {str(e)}")
    
    def _create_story_prompt(self, analysis_result: Dict[str, Any]) -> str:
        """Create the prompt for generating the story."""
        character = analysis_result.get("character", "a little animal")
        problem_type = analysis_result.get("problem_type", "a behavioral challenge")
        moral = analysis_result.get("moral", "an important life lesson")
        story_theme = analysis_result.get("story_theme", "friendship and learning")
        emotions = analysis_result.get("emotions", "mixed feelings")
        
        return f"""
Create a delightful children's fairy tale with the following elements:

Main Character: {character}
Problem Theme: {problem_type}
Moral Lesson: {moral}
Story Theme: {story_theme}
Emotions to Address: {emotions}

Story Requirements:
1. Length: 300-500 words (perfect for a 3-5 minute audio story)
2. Structure: Beginning (introduce character and setting), Middle (challenge/problem), End (resolution and lesson learned)
3. Tone: Warm, magical, and encouraging
4. Language: Simple, clear, and engaging for young children
5. Setting: A magical forest, meadow, or other enchanting place
6. Supporting Characters: Include 1-2 friendly animal friends or wise mentors
7. Conflict: Present the behavioral challenge in a gentle, non-threatening way
8. Resolution: Show the character learning and growing through the experience
9. Ending: Positive and uplifting with a clear but subtle moral message

Important Guidelines:
- Never directly mention the child's actual problem
- Use the animal character as a gentle mirror, not a direct parallel
- Make the story feel like entertainment, not a lecture
- Include sensory details (sounds, colors, textures) to make it engaging
- Use dialogue to bring characters to life
- End with the character feeling proud and happy about their growth

Write the story now:
"""
    
    def _format_story(self, story_text: str) -> str:
        """Format the story text for better readability and audio narration."""
        # Remove any markdown formatting that might interfere with TTS
        formatted = story_text.replace("**", "").replace("*", "").replace("_", "")
        
        # Ensure proper paragraph breaks
        paragraphs = formatted.split('\n\n')
        formatted_paragraphs = []
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if paragraph:
                # Add a title if the first paragraph looks like a title
                if len(formatted_paragraphs) == 0 and len(paragraph) < 100:
                    formatted_paragraphs.append(f"🎭 {paragraph}")
                else:
                    formatted_paragraphs.append(paragraph)
        
        return '\n\n'.join(formatted_paragraphs)
    
    def _validate_story(self, story_text: str) -> bool:
        """Validate that the generated story meets quality requirements."""
        # Basic validation checks
        if len(story_text) < 200:
            return False
        
        if len(story_text) > 1000:
            return False
        
        # Check for appropriate content
        inappropriate_words = ["bad", "wrong", "naughty", "stupid", "hate"]
        story_lower = story_text.lower()
        
        for word in inappropriate_words:
            if word in story_lower:
                return False
        
        return True
    
    def _generate_fallback_story(self, analysis_result: Dict[str, Any]) -> str:
        """Generate a simple fallback story when Azure OpenAI is not available."""
        character = analysis_result.get("character", "a little bear")
        problem_type = analysis_result.get("problem_type", "a behavioral challenge")
        moral = analysis_result.get("moral", "an important life lesson")
        
        # Simple template-based story generation
        story_templates = {
            "sharing conflict": f"""
Once upon a time, there was {character} who lived in a beautiful forest. {character.title()} had a favorite toy that they loved to play with every day.

One sunny morning, {character} was playing with their special toy when a friendly rabbit came by. "May I play with your toy too?" asked the rabbit with a hopeful smile.

{character.title()} felt a little worried. "This is MY toy," they thought. "What if it gets broken or lost?"

But then {character} remembered something their wise owl friend had once said: "The best toys are the ones we share with friends, because then we have twice as much fun!"

So {character} smiled and said, "Of course! Let's play together!" And you know what? They had the most wonderful time playing together, laughing and having fun.

From that day on, {character} learned that sharing makes everything more special. The toy was still theirs, but now it brought joy to their friends too, and that made {character} feel very happy indeed.

The end.
""",
            "aggression": f"""
Once upon a time, there was {character} who lived in a peaceful meadow. {character.title()} was usually very kind, but sometimes when things didn't go their way, they would get very angry and want to fight.

One day, {character} was playing a game with their friends when they didn't win. Instead of being happy for the winner, {character} felt angry and wanted to fight about it.

But then their wise turtle friend came over and said gently, "My dear {character}, fighting never solves anything. It only makes everyone sad, including you."

{character.title()} took a deep breath and thought about it. The turtle was right. Fighting made everyone feel bad, and it didn't make the game any more fun.

So {character} apologized to their friends and said, "You're right, I was wrong to get angry. Let's play again and have fun together!"

From that day on, {character} learned that when things don't go their way, it's better to take a deep breath, talk about it calmly, and find a peaceful solution. And you know what? Everyone had much more fun playing together after that!

The end.
""",
            "default": f"""
Once upon a time, there was {character} who lived in a magical forest. {character.title()} was learning about {moral} through their daily adventures.

One day, {character} faced a challenge that tested their understanding of this important lesson. At first, it was difficult, but with the help of their forest friends and their own growing wisdom, {character} found the right way to handle the situation.

Through this experience, {character} learned that {moral}, and this made them feel proud and happy. Their friends were proud of them too, and everyone in the forest celebrated {character}'s growth and wisdom.

From that day forward, {character} remembered this important lesson and used it to help others in the forest, making it a more wonderful place for everyone.

The end.
"""
        }
        
        # Select appropriate template
        if "share" in problem_type.lower():
            story = story_templates["sharing conflict"]
        elif "fight" in problem_type.lower() or "aggressive" in problem_type.lower():
            story = story_templates["aggression"]
        else:
            story = story_templates["default"]
        
        return story.strip()
