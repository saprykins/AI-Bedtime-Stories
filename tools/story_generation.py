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
                max_tokens=1500
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
Create a delightful children's fairy tale with the following elements, using a dialogue format between a Man (Dad/Father) and Woman (Mom/Mother) telling the story together:

Main Character: {character}
Problem Theme: {problem_type}
Moral Lesson: {moral}
Story Theme: {story_theme}
Emotions to Address: {emotions}

Story Requirements:
1. Format: Write as a dialogue between Mom and Dad telling the story together
2. Length: 300-500 words (perfect for a 3-5 minute audio story)
3. Structure: Parents take turns telling parts of the story, using dialogue markers:
   - Start lines with "Man:" or "Woman:" to indicate who's speaking
   - Example:
     Woman: Once upon a time...
     Man: In a magical forest, there lived...
     Woman: One sunny morning...
4. Tone: Warm, parental, and encouraging
5. Language: Simple, clear, and engaging for young children
6. Setting: A magical forest, meadow, or other enchanting place
7. Characters: Include animal friends or wise mentors
8. Resolution: Show character learning and growing
9. Ending: Positive and uplifting with a clear moral message

Important Guidelines:
- Format ALL story content as dialogue between Mom and Dad
- Use natural turn-taking between parents telling the story
- Never directly mention the child's actual problem
- Make the story feel like a bedtime story told by both parents
- Add parental warmth and gentle guidance in the dialogue
- Include reactions and gentle comments from both parents

Example Format:
Woman: Once upon a time, in a magical forest...
Man: There lived a little rabbit who loved to play...
Woman: One day, this little rabbit met a friend...
[continue in this format]

Write the story now as a dialogue between Mom and Dad:
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
Woman: Once upon a time, there was {character} who lived in a beautiful forest.

Man: This little {character} had a very special toy that they loved to play with every day. It was their most favorite thing in the whole world.

Woman: One sunny morning, while {character} was playing, a friendly rabbit hopped by with a hopeful smile.

Man: The rabbit looked at the toy with big, gentle eyes and asked very politely, "May I play with your toy too?"

Woman: Oh, our little {character} felt quite worried about this. They held the toy close and thought, "This is MY toy. What if it gets broken or lost?"

Man: But just then, something wonderful happened. {character.title()} remembered the wise words of their friend, the old owl.

Woman: The owl had once said, "The best toys are the ones we share with friends, because then we have twice as much fun!"

Man: And you know what our brave little {character} did next? They took a deep breath, smiled warmly, and said...

Woman: "Of course! Let's play together!" And oh, what fun they had!

Man: They played and laughed and had the most wonderful time together. The toy seemed even more special when it was shared.

Woman: From that day on, {character} discovered something magical - sharing made everything more special. The toy was still theirs, but now it brought joy to their friends too.

Man: And that made {character} feel happier than they'd ever felt before.

Woman: The end, sweetheart. Sweet dreams.
""",
            "aggression": f"""
Woman: Once upon a time, in a peaceful meadow, there lived {character}. They were usually very kind and friendly.

Man: But sometimes, when things didn't go exactly their way, our little {character} would get very frustrated and want to fight.

Woman: One sunny day, {character} was playing a fun game with all their forest friends. Everyone was having such a wonderful time.

Man: But when the game ended, {character} discovered they hadn't won. Instead of being happy for their friends who won, they started to feel very angry inside.

Woman: Just as {character} was about to lose their temper, something wonderful happened. Their wise old friend, the turtle, slowly walked over.

Man: The turtle looked at {character} with kind, gentle eyes and said softly, "My dear friend, fighting never solves anything. It only makes everyone sad, including you."

Woman: {character.title()} looked at their friend's caring face and took a deep, calming breath. They could feel their anger starting to melt away.

Man: And you know what? The turtle was absolutely right. Fighting wouldn't make the game any more fun, and it wouldn't make anyone feel better.

Woman: So our brave {character} did something really wonderful. They turned to their friends with a warm smile.

Man: "I'm sorry," they said, "I was wrong to get angry. Would you like to play another game together?"

Woman: From that day on, whenever things didn't go their way, {character} remembered to take a deep breath and talk about their feelings calmly.

Man: And you know what the most amazing part was? Everyone had so much more fun playing together after that!

Woman: The end, little one. Sweet dreams.
""",
            "default": f"""
Woman: Once upon a time, in a magical forest full of wonder, there lived {character}.

Man: Each day, this little {character} was learning something very special - they were learning about {moral}.

Woman: One bright morning, {character} faced a challenge that would test everything they had learned so far.

Man: At first, it seemed very difficult, and our little friend wasn't sure what to do.

Woman: But you know what made all the difference? Their wonderful forest friends came to help, sharing their wisdom and support.

Man: With their friends by their side, {character} found the courage and wisdom to handle the situation in just the right way.

Woman: Through this amazing experience, {character} learned something very important about {moral}.

Man: And you should have seen how proud everyone was! The whole forest celebrated {character}'s growth and wisdom.

Woman: From that day forward, whenever another friend needed help, {character} was there to share what they had learned.

Man: They made the magical forest an even more wonderful place for everyone.

Woman: The end, sweetheart. Time for sweet dreams.
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
