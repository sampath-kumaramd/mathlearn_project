from ..nlp.math_processor import MathProcessor

class MathSpeech:
    def __init__(self, speech_engine):
        self.speech_engine = speech_engine
        self.math_processor = MathProcessor()
        
    def speak_equation(self, equation):
        """Convert equation to speech and speak it"""
        speech_text = self.math_processor.equation_to_speech(equation, 
                                                            language=self.speech_engine.language)
        return self.speech_engine.speak(speech_text)