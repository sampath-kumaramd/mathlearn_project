# src/tts/enhanced_speech_engine.py

import os
import tempfile
from gtts import gTTS
import pygame
import re

class EnhancedSpeechEngine:
    def __init__(self, language='si'):
        self.language = language
        pygame.mixer.init()
        
        # Math terminology mapping
        self.math_terms = {
            "+": "එකතු",
            "-": "අඩු",
            "*": "ගුණ",
            "/": "බෙදා",
            "=": "සමානයි",
            "^": "න්තු",
            "x": "එක්ස්",
            "y": "වයි",
            "z": "සෙඩ්",
            "√": "වර්ගමූලය",
            "(": "වරහන ආරම්භය",
            ")": "වරහන අවසානය"
        }
    
    def _preprocess_math_equation(self, text):
        """Process mathematical equations for better speech output"""
        # Replace mathematical symbols with words
        for symbol, word in self.math_terms.items():
            text = text.replace(symbol, f" {word} ")
        
        # Handle superscripts for powers
        text = re.sub(r'(\d+)\^(\d+)', r'\1 න්තු \2', text)
        
        # Handle fractions (simplified approach)
        text = re.sub(r'(\d+)/(\d+)', r'\1 බෙදා \2', text)
        
        # Handle square roots
        text = re.sub(r'√(\d+)', r'වර්ගමූලය \1', text)
        
        # Clean up excess spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def speak(self, text, is_equation=False):
        """Convert text to speech and play it"""
        try:
            # Preprocess if it's an equation
            if is_equation:
                text = self._preprocess_math_equation(text)
            
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_filename = fp.name
                
            # Generate speech
            tts = gTTS(text=text, lang=self.language, slow=False)
            tts.save(temp_filename)
            
            # Play the audio
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            # Clean up temp file
            os.unlink(temp_filename)
            return True
        except Exception as e:
            print(f"Error in TTS: {e}")
            return False
    
    def speak_equation(self, equation):
        """Specifically process and speak a mathematical equation"""
        return self.speak(equation, is_equation=True)