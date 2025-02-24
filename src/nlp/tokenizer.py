import re

class SinhalaTokenizer:
    def __init__(self):
        # Define patterns for Sinhala text, numbers, and mathematical expressions
        self.sinhala_pattern = r'[\u0D80-\u0DFF]+'
        self.number_pattern = r'\d+(?:\.\d+)?'
        self.math_symbol_pattern = r'[+\-*/=^()]'
        
    def tokenize(self, text):
        """Tokenize Sinhala text with mathematical expressions"""
        tokens = []
        
        # Find all Sinhala words
        sinhala_words = [(m.group(), m.start(), m.end()) 
                        for m in re.finditer(self.sinhala_pattern, text)]
        
        # Find all numbers
        numbers = [(m.group(), m.start(), m.end()) 
                  for m in re.finditer(self.number_pattern, text)]
        
        # Find all mathematical symbols
        symbols = [(m.group(), m.start(), m.end()) 
                  for m in re.finditer(self.math_symbol_pattern, text)]
        
        # Combine all tokens and sort by position
        all_tokens = sinhala_words + numbers + symbols
        all_tokens.sort(key=lambda x: x[1])
        
        # Extract just the token text
        tokens = [token[0] for token in all_tokens]
        
        return tokens