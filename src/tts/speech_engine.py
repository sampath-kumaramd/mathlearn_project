import os
import tempfile
from gtts import gTTS
import pygame

class SpeechEngine:
    def __init__(self, language='si'):
        self.language = language
        pygame.mixer.init()
        
    def speak(self, text):
        """Convert text to speech and play it"""
        try:
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