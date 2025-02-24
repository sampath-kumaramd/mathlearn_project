import re

class MathProcessor:
    def __init__(self):
        # Sinhala mathematics terminology
        self.terms = {
            "plus": "එකතු කිරීම",
            "minus": "අඩු කිරීම",
            "multiply": "ගුණ කිරීම",
            "divide": "බෙදීම",
            "equals": "සමානයි",
            "square": "වර්ගය",
            "root": "මූලය"
        }
        
    def parse_equation(self, equation):
        """Parse a mathematical equation into components"""
        # Simple regex to extract components (can be enhanced)
        components = re.findall(r'(\d+\.?\d*|[+\-*/=^()]|[xyzabc])', equation)
        return components
        
    def equation_to_speech(self, equation, language="si"):
        """Convert equation to speech-friendly format"""
        components = self.parse_equation(equation)
        
        # Convert components to speech text
        speech_parts = []
        for i, comp in enumerate(components):
            if comp == '+':
                speech_parts.append("plus" if language == "en" else self.terms["plus"])
            elif comp == '-':
                speech_parts.append("minus" if language == "en" else self.terms["minus"])
            elif comp == '*':
                speech_parts.append("times" if language == "en" else self.terms["multiply"])
            elif comp == '/':
                speech_parts.append("divided by" if language == "en" else self.terms["divide"])
            elif comp == '=':
                speech_parts.append("equals" if language == "en" else self.terms["equals"])
            elif comp == '^':
                speech_parts.append("to the power of" if language == "en" else "බලය")
            else:
                speech_parts.append(comp)
        
        return " ".join(speech_parts)