# src/nlp/enhanced_tokenizer.py

import re
import json
import os

class EnhancedSinhalaTokenizer:
    def __init__(self):
        self.sinhala_pattern = r'[\u0D80-\u0DFF]+'
        self.number_pattern = r'\d+(?:\.\d+)?'
        self.math_symbol_pattern = r'[+\-*/=^()]'
        self.variable_pattern = r'[a-zA-Z]'
        
        # Load Sinhala mathematical terms dictionary
        self.math_terms = self._load_math_terms()
        
    def _load_math_terms(self):
        """Load Sinhala mathematical terminology"""
        try:
            # Path to the JSON file containing math terms
            file_path = os.path.join(os.path.dirname(__file__), 
                                   '../data/math_terms.json')
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                # Create a basic dictionary if file doesn't exist
                return {
                    "denominator": "හරය",
                    "numerator": "ලවය",
                    "square root": "වර්ගමූලය",
                    "equation": "සමීකරණය",
                    "angle": "කෝණය",
                    "triangle": "ත්‍රිකෝණය",
                    "circle": "වෘත්තය",
                    "rectangle": "ආයතය",
                    "square": "වර්ගය",
                    "addition": "එකතු කිරීම",
                    "subtraction": "අඩු කිරීම",
                    "multiplication": "ගුණ කිරීම",
                    "division": "බෙදීම"
                }
        except Exception as e:
            print(f"Error loading math terms: {e}")
            return {}
    
    def tokenize(self, text):
        """Enhanced tokenization for Sinhala text with math expressions"""
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
        
        # Find all variables
        variables = [(m.group(), m.start(), m.end()) 
                    for m in re.finditer(self.variable_pattern, text)]
        
        # Combine all tokens and sort by position
        all_tokens = sinhala_words + numbers + symbols + variables
        all_tokens.sort(key=lambda x: x[1])
        
        # Extract just the token text
        tokens = [token[0] for token in all_tokens]
        
        return tokens
    
    def identify_math_terms(self, text):
        """Identify Sinhala mathematical terms in text"""
        identified_terms = []
        
        # Check for each math term in the text
        for eng_term, si_term in self.math_terms.items():
            if si_term in text:
                identified_terms.append({
                    "term": si_term,
                    "english_equivalent": eng_term,
                    "position": text.find(si_term)
                })
        
        # Sort by position in text
        identified_terms.sort(key=lambda x: x["position"])
        
        return identified_terms
    
    def resolve_ambiguity(self, term, context):
        """Resolve ambiguity for terms with multiple meanings"""
        # Example: කෝණය can mean "angle" or "corner"
        if term == "කෝණය":
            # Check if geometric context
            geometric_terms = ["ත්‍රිකෝණය", "වෘත්තය", "ආයතය", "චතුරස්‍රය", "ඩිග්රි"]
            for geo_term in geometric_terms:
                if geo_term in context:
                    return "angle"
            return "corner"
        
        # Add more ambiguity resolution as needed
        
        # Default return the term itself
        return term