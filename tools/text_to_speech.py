"""
Tool 3: Text-to-Speech Tool

This tool converts the generated story text into audio using Azure Speech Services.
"""


import os
import time
from typing import Optional

# Load .env at the very top, before any Azure SDK import (to match working script)
from dotenv import load_dotenv
load_dotenv()

# Import Azure Speech SDK
try:
    import azure.cognitiveservices.speech as speechsdk
    AZURE_SPEECH_AVAILABLE = True
except ImportError as import_error:
    print(f"Warning: Azure Speech Services import failed: {import_error}")
    print("💡 Please ensure 'azure-cognitiveservices-speech' is installed.")
    AZURE_SPEECH_AVAILABLE = False

# Try to import pyttsx3 as fallback
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False


class TextToSpeechTool:
    def _get_speech_config(self):
        """
        Create and return an Azure SpeechConfig object using environment variables.
        """
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        speech_region = os.getenv("AZURE_SPEECH_REGION")
        if not speech_key or not speech_region:
            raise Exception("Azure Speech Services credentials not found. Please set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables.")
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        voice_name = os.getenv("AZURE_VOICE_NAME", "en-US-AriaNeural")
        speech_config.speech_synthesis_voice_name = voice_name
        return speech_config
    """
    Converts story text to audio using Azure Speech Services.
    Provides child-friendly voice synthesis with appropriate pacing and tone.
    """
    
    def __init__(self):
        """Initialize the text-to-speech tool with Azure Speech Services."""
        if not AZURE_SPEECH_AVAILABLE:
            print("⚠️  Azure Speech Services not available. Text-to-speech will be disabled.")
            self.speech_config = None
            self.output_dir = os.getenv("OUTPUT_DIR", "./output")
            os.makedirs(self.output_dir, exist_ok=True)
            return
            
        self.speech_config = self._get_speech_config()
        self.output_dir = os.getenv("OUTPUT_DIR", "./output")
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
    
    
    def text_to_speech(self, story_text: str, filename: Optional[str] = None) -> str:
        """
        Convert story text to audio file.
        
        Args:
            story_text: The story text to convert to speech
            filename: Optional custom filename (without extension)
            
        Returns:
            Path to the generated audio file
        """
        if not AZURE_SPEECH_AVAILABLE:
            # Try pyttsx3 fallback for audio generation
            if PYTTSX3_AVAILABLE:
                return self._generate_audio_with_pyttsx3(story_text, filename)
            else:
                # Final fallback: save story as text file
                if not filename:
                    timestamp = int(time.time())
                    filename = f"story_{timestamp}.txt"
                elif not filename.endswith('.txt'):
                    filename += '.txt'
                
                output_path = os.path.join(self.output_dir, filename)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(story_text)
                
                print(f"📝 Story saved as text file: {output_path}")
                print("💡 To enable audio generation, please set up Azure Speech Services credentials or install pyttsx3.")
                return output_path
            
        try:
            # Generate filename if not provided
            if not filename:
                timestamp = int(time.time())
                filename = f"story_{timestamp}"
            
            # Ensure filename has .wav extension
            if not filename.endswith('.wav'):
                filename += '.wav'
            
            # Full path to output file
            output_path = os.path.join(self.output_dir, filename)
            
            # Get Azure Speech Services credentials
            speech_key = os.getenv("AZURE_SPEECH_KEY")
            speech_region = os.getenv("AZURE_SPEECH_REGION")
            
            if not speech_key or not speech_region:
                raise Exception("Azure Speech Services credentials not found. Please set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables.")
            
            # Create speech configuration using your working approach
            speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
            
            # Set voice for child-friendly speech
            voice_name = os.getenv("AZURE_VOICE_NAME", "en-US-AriaNeural")
            speech_config.speech_synthesis_voice_name = voice_name
            
            # Create audio output configuration
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
            
            # Create speech synthesizer
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
            
            # Prepare text for speech synthesis
            speech_text = self._prepare_text_for_speech(story_text)
            
            print(f"🎤 Synthesizing speech with Azure Speech Services... (this may take a moment)")
            
            # Perform speech synthesis using your working approach
            result = synthesizer.speak_text_async(speech_text).get()
            
            # Check if synthesis was successful
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print(f"✅ Speech synthesis completed successfully")
                return output_path
            else:
                print(f"❌ Speech synthesis failed: {result.reason}")
                # Fallback to pyttsx3 if available
                if PYTTSX3_AVAILABLE:
                    print("🔄 Falling back to pyttsx3...")
                    return self._generate_audio_with_pyttsx3(story_text, filename)
                else:
                    raise Exception(f"Speech synthesis failed with reason: {result.reason}")
                
        except Exception as e:
            print(f"❌ Azure Speech Services failed: {e}")
            # Fallback to pyttsx3 if available
            if PYTTSX3_AVAILABLE:
                print("🔄 Falling back to pyttsx3...")
                return self._generate_audio_with_pyttsx3(story_text, filename)
            else:
                # Final fallback: save as text file
                if not filename:
                    timestamp = int(time.time())
                    filename = f"story_{timestamp}.txt"
                elif not filename.endswith('.txt'):
                    filename += '.txt'
                
                output_path = os.path.join(self.output_dir, filename)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(story_text)
                
                print(f"📝 Final fallback: Story saved as text file: {output_path}")
                return output_path
    
    def _prepare_text_for_speech(self, story_text: str) -> str:
        """
        Prepare the story text for optimal speech synthesis.
        
        Args:
            story_text: Raw story text
            
        Returns:
            Text optimized for speech synthesis
        """
        # Remove emojis and special characters that might interfere with TTS
        import re
        
        # Remove emojis
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        
        speech_text = emoji_pattern.sub('', story_text)
        
        # Add pauses for better pacing
        speech_text = speech_text.replace('\n\n', ' ... ')  # Paragraph breaks
        speech_text = speech_text.replace('\n', ' ')        # Line breaks
        
        # Add emphasis for important words (SSML-like markup)
        # This is a simple approach - for more advanced SSML, you'd use Azure's SSML support
        speech_text = speech_text.replace('"', '"')  # Smart quotes to regular quotes
        
        # Clean up multiple spaces
        speech_text = re.sub(r'\s+', ' ', speech_text).strip()
        
        return speech_text
    
    def get_available_voices(self) -> list:
        """
        Get list of available voices (for future enhancement).
        This would require additional Azure API calls to list available voices.
        """
        # Common child-friendly voices
        return [
            "en-US-AriaNeural",    # Warm, friendly female voice
            "en-US-JennyNeural",   # Clear, professional female voice
            "en-US-GuyNeural",     # Warm male voice
            "en-US-DavisNeural",   # Friendly male voice
        ]
    
    def set_voice(self, voice_name: str) -> None:
        """
        Change the voice used for speech synthesis.
        
        Args:
            voice_name: Name of the Azure voice to use
        """
        try:
            self.speech_config.speech_synthesis_voice_name = voice_name
            print(f"✅ Voice changed to: {voice_name}")
        except Exception as e:
            raise Exception(f"Failed to set voice: {str(e)}")
    
    def set_speech_rate(self, rate: float) -> None:
        """
        Set the speech rate (0.5 = half speed, 2.0 = double speed).
        Note: This would require SSML implementation for full functionality.
        
        Args:
            rate: Speech rate multiplier
        """
        print(f"ℹ️  Speech rate configuration would be set to: {rate}")
        print("   (Full rate control requires SSML implementation)")
    
    def _generate_audio_with_pyttsx3(self, story_text: str, filename: str = None) -> str:
        """
        Generate audio using pyttsx3 as fallback when Azure Speech Services is not available.
        
        Args:
            story_text: The story text to convert to speech
            filename: Optional custom filename (without extension)
            
        Returns:
            Path to the generated audio file
        """
        try:
            # Generate filename if not provided
            if not filename:
                timestamp = int(time.time())
                filename = f"story_{timestamp}"
            
            # Ensure filename has .wav extension for pyttsx3
            if not filename.endswith('.wav'):
                filename += '.wav'
            
            # Full path to output file
            output_path = os.path.join(self.output_dir, filename)
            
            print(f"🎤 Generating audio with pyttsx3... (this may take a moment)")
            
            # Initialize pyttsx3 engine
            engine = pyttsx3.init()
            
            # Configure voice properties for child-friendly speech
            voices = engine.getProperty('voices')
            if voices:
                # Try to find a female voice (usually more child-friendly)
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
            
            # Set speech rate (slower for children)
            engine.setProperty('rate', 130)  # Lowered for softer sound
            
            # Set volume
            engine.setProperty('volume', 0.9)
            
            # Prepare text for speech
            speech_text = self._prepare_text_for_speech(story_text)
            
            # Save to file
            engine.save_to_file(speech_text, output_path)
            engine.runAndWait()

            return output_path

        except Exception as e:
            print(f"❌ Error generating audio with pyttsx3: {str(e)}")
            raise

    def _build_dialogue_ssml(self, story_text: str) -> str:
        """
        Build SSML for a dialogue between a man (low bass) and a woman (natural).
        Detects lines starting with 'Man:' and 'Woman:' and assigns voices.
        """
        # Azure recommended voices
        man_voice = "en-US-GuyNeural"  # or en-US-DavisNeural
        woman_voice = "en-US-AriaNeural"  # or en-US-JennyNeural
        # SSML prosody for low bass man
        man_prosody = "<prosody pitch='-6st' rate='-10%'>"
        woman_prosody = "<prosody pitch='+0st' rate='-10%'>"
        # Build SSML
        ssml_lines = []
        import re
        for line in story_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            m = re.match(r'^(Man|Мужчина|Папа|Отец|Папа|Папочка|Папа\w*|Муж\w*|Father|Dad|Papa|Male):\s*(.*)', line, re.IGNORECASE)
            w = re.match(r'^(Woman|Женщина|Мама|Мать|Мамочка|Мама\w*|Жен\w*|Mother|Mom|Mama|Female):\s*(.*)', line, re.IGNORECASE)
            if m:
                text = m.group(2)
                ssml_lines.append(f"<voice name='{man_voice}'>{man_prosody}{text}</prosody></voice>")
            elif w:
                text = w.group(2)
                ssml_lines.append(f"<voice name='{woman_voice}'>{woman_prosody}{text}</prosody></voice>")
            else:
                # Default to woman for narration, but neutral prosody
                ssml_lines.append(f"<voice name='{woman_voice}'><prosody rate='-10%'>{line}</prosody></voice>")
        ssml_body = '\n'.join(ssml_lines)
        ssml = f'''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
{ssml_body}
</speak>'''
        return ssml
    def _build_dialogue_ssml(self, story_text: str) -> str:
        """
        Build SSML for a dialogue between a man (low bass) and a woman (natural).
        Detects lines starting with 'Man:' and 'Woman:' and assigns voices.
        """
        # Azure recommended voices
        man_voice = "en-US-GuyNeural"  # or en-US-DavisNeural
        woman_voice = "en-US-AriaNeural"  # or en-US-JennyNeural
        # SSML prosody for low bass man
        man_prosody = "<prosody pitch='-6st' rate='-10%'>"
        woman_prosody = "<prosody pitch='+0st' rate='-10%'>"
        # Build SSML
        ssml_lines = []
        import re
        for line in story_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            m = re.match(r'^(Man|Мужчина|Папа|Отец|Папа|Папочка|Папа\w*|Муж\w*|Father|Dad|Papa|Male):\s*(.*)', line, re.IGNORECASE)
            w = re.match(r'^(Woman|Женщина|Мама|Мать|Мамочка|Мама\w*|Жен\w*|Mother|Mom|Mama|Female):\s*(.*)', line, re.IGNORECASE)
            if m:
                text = m.group(2)
                ssml_lines.append(f"<voice name='{man_voice}'>{man_prosody}{text}</prosody></voice>")
            elif w:
                text = w.group(2)
                ssml_lines.append(f"<voice name='{woman_voice}'>{woman_prosody}{text}</prosody></voice>")
            else:
                # Default to woman for narration, but neutral prosody
                ssml_lines.append(f"<voice name='{woman_voice}'><prosody rate='-10%'>{line}</prosody></voice>")
        ssml_body = '\n'.join(ssml_lines)
        ssml = f'''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
{ssml_body}
</speak>'''
        return ssml


        def _build_dialogue_ssml(self, story_text: str) -> str:
            """
            Build SSML for a dialogue between a man (low bass) and a woman (natural).
            Detects lines starting with 'Man:' and 'Woman:' and assigns voices.
            """
            # Azure recommended voices
            man_voice = "en-US-GuyNeural"  # or en-US-DavisNeural
            woman_voice = "en-US-AriaNeural"  # or en-US-JennyNeural
            # SSML prosody for low bass man
            man_prosody = "<prosody pitch='-6st' rate='-10%'>"
            woman_prosody = "<prosody pitch='+0st' rate='-10%'>"
            # Build SSML
            ssml_lines = []
            import re
            for line in story_text.split('\n'):
                line = line.strip()
                if not line:
                    continue
                m = re.match(r'^(Man|Мужчина|Папа|Отец|Папа|Папочка|Папа\w*|Муж\w*|Father|Dad|Papa|Male):\s*(.*)', line, re.IGNORECASE)
                w = re.match(r'^(Woman|Женщина|Мама|Мать|Мамочка|Мама\w*|Жен\w*|Mother|Mom|Mama|Female):\s*(.*)', line, re.IGNORECASE)
                if m:
                    text = m.group(2)
                    ssml_lines.append(f"<voice name='{man_voice}'>{man_prosody}{text}</prosody></voice>")
                elif w:
                    text = w.group(2)
                    ssml_lines.append(f"<voice name='{woman_voice}'>{woman_prosody}{text}</prosody></voice>")
                else:
                    # Default to woman for narration, but neutral prosody
                    ssml_lines.append(f"<voice name='{woman_voice}'><prosody rate='-10%'>{line}</prosody></voice>")
            ssml_body = '\n'.join(ssml_lines)
            ssml = f'''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    {ssml_body}
    </speak>'''
            return ssml
