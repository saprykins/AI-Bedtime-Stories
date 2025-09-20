#!/usr/bin/env python3
"""Test Azure Speech Services with the working approach"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_azure_speech():
    try:
        import azure.cognitiveservices.speech as speechsdk
        
        # Get credentials
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        speech_region = os.getenv("AZURE_SPEECH_REGION")
        
        print(f"Speech Key: {speech_key[:10]}..." if speech_key else "Not found")
        print(f"Speech Region: {speech_region}")
        
        if not speech_key or not speech_region:
            print("❌ Missing credentials")
            return False
        
        # Create speech configuration
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"
        
        # Create audio output configuration
        audio_config = speechsdk.audio.AudioOutputConfig(filename="test_output.wav")
        
        # Create speech synthesizer
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        
        # Test text
        text = "Hello, this is a test of Azure Speech Services for bedtime stories."
        
        print("🎤 Testing Azure Speech Services...")
        result = synthesizer.speak_text_async(text).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("✅ Azure Speech Services test successful!")
            return True
        else:
            print(f"❌ Speech synthesis failed: {result.reason}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_azure_speech()
