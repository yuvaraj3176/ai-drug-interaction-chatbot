"""
Response Generator for Drug Interaction Chatbot
Member 2 Implementation
"""

import random
from datetime import datetime

class ResponseGenerator:
    def __init__(self):
        """Initialize response generator with templates"""
        self.greeting_responses = self._load_greeting_responses()
        self.interaction_responses = self._load_interaction_responses()
        self.info_responses = self._load_info_responses()
        self.side_effect_responses = self._load_side_effect_responses()
        self.dosage_responses = self._load_dosage_responses()
        self.error_responses = self._load_error_responses()
        
    def _load_greeting_responses(self):
        """Load greeting response templates"""
        return [
            "Hello! How can I help you with drug information today?",
            "Hi there! Ask me about any drug interactions or medication information.",
            "Welcome! I'm your drug interaction assistant. What would you like to know?",
            "Hello! I can help check drug interactions, side effects, and more. Just ask!",
            "Hi! Feel free to ask about any medications or their interactions."
        ]
    
    def _load_interaction_responses(self):
        """Load interaction response templates"""
        return {
            'severe': [
                "⚠️ **SEVERE INTERACTION**: {drug1} and {drug2} should NOT be taken together. {description}",
                "🚫 **CONTRAINDICATED**: {drug1} and {drug2} have a severe interaction. {description}",
                "❗ **DANGEROUS COMBINATION**: Avoid taking {drug1} with {drug2}. {description}"
            ],
            'moderate': [
                "⚠️ **MODERATE INTERACTION**: {drug1} and {drug2} may interact. {description}",
                "⚕️ **CAUTION ADVISED**: Taking {drug1} with {drug2} requires monitoring. {description}",
                "📋 **MODERATE INTERACTION**: {description}. Consult your doctor before combining."
            ],
            'mild': [
                "ℹ️ **MILD INTERACTION**: {drug1} and {drug2} have a minor interaction. {description}",
                "📌 **NOTE**: There's a mild interaction between {drug1} and {drug2}. {description}",
                "✓ **MINOR INTERACTION**: {description}. Usually safe but monitor for effects."
            ],
            'none': [
                "✅ **NO KNOWN INTERACTION**: {drug1} and {drug2} are generally safe to take together.",
                "✓ **SAFE COMBINATION**: No significant interactions found between {drug1} and {drug2}.",
                "🟢 **COMPATIBLE**: {drug1} and {drug2} can be taken together safely."
            ]
        }
    
    def _load_info_responses(self):
        """Load drug information response templates"""
        return [
            "💊 **{name}** ({generic_name})\n\n"
            "**Category:** {category}\n"
            "**Uses:** {description}\n\n"
            "**Common side effects:** {side_effects}\n"
            "**Who should avoid:** {contraindications}\n"
            "**Typical dosage:** {dosage}",
            
            "📋 **About {name}**\n\n"
            "{name} ({generic_name}) is a {category} medication.\n\n"
            "**What it's used for:** {description}\n"
            "**Possible side effects:** {side_effects}\n"
            "**Important warnings:** {contraindications}"
        ]
    
    def _load_side_effect_responses(self):
        """Load side effect response templates"""
        return [
            "The common side effects of {drug} include: {side_effects}\n\n"
            "⚠️ Seek medical attention if you experience severe reactions.",
            
            "**Side effects of {drug}:**\n"
            "• Common: {side_effects}\n\n"
            "Contact your doctor if side effects persist or worsen.",
            
            "For {drug}, patients commonly report: {side_effects}\n"
            "This is not a complete list. Report any unusual symptoms to your doctor."
        ]
    
    def _load_dosage_responses(self):
        """Load dosage response templates"""
        return [
            "The typical dosage for {drug} is {dosage}\n\n"
            "⚠️ Always follow your doctor's prescription and read the label carefully.",
            
            "**Dosage information for {drug}:**\n"
            "• Standard dose: {dosage}\n\n"
            "Dosage may vary based on your medical condition and response to treatment.",
            
            "For {drug}, the usual dose is {dosage}\n"
            "Do not change your dose without consulting your healthcare provider."
        ]
    
    def _load_error_responses(self):
        """Load error/fallback response templates"""
        return [
            "I'm not sure about that. Could you rephrase your question?",
            "I couldn't find information about that. Try asking about specific drugs or interactions.",
            "I'm still learning! Could you ask about drug interactions or medication information?",
            "I don't have enough information to answer that. Please ask about specific medications.",
            "That's beyond my current knowledge. Try asking about drug interactions or side effects."
        ]
    
    def generate_response(self, intent, entities, interaction_result=None, drug_info=None):
        """
        Generate appropriate response based on intent and entities
        """
        if not intent or intent == 'unknown':
            return self._get_random_response(self.error_responses)
        
        if intent == 'greeting':
            return self._get_random_response(self.greeting_responses)
        
        elif intent == 'thanks':
            return "You're welcome! Feel free to ask if you have more questions."
        
        elif intent == 'farewell':
            return "Take care! Remember to always consult your healthcare provider. Goodbye!"
        
        elif intent == 'interaction_check':
            return self._generate_interaction_response(entities, interaction_result)
        
        elif intent == 'drug_info':
            return self._generate_info_response(entities, drug_info)
        
        elif intent == 'side_effects':
            return self._generate_side_effect_response(entities, drug_info)
        
        elif intent == 'dosage':
            return self._generate_dosage_response(entities, drug_info)
        
        elif intent == 'contraindications':
            return self._generate_contraindication_response(entities, drug_info)
        
        else:
            return self._get_random_response(self.error_responses)
    
    def _generate_interaction_response(self, entities, interaction_result):
        """Generate response for interaction queries"""
        drugs = entities.get('drugs', [])
        
        if len(drugs) < 2:
            return "Please specify two or more drugs to check for interactions."
        
        if not interaction_result:
            return f"I don't have interaction data for {', '.join(drugs)}. Both are generally considered safe, but always consult your doctor."
        
        severity = interaction_result.get('severity', 'none')
        templates = self.interaction_responses.get(severity, self.interaction_responses['none'])
        template = random.choice(templates)
        
        return template.format(
            drug1=drugs[0].capitalize() if drugs else "Unknown",
            drug2=drugs[1].capitalize() if len(drugs) > 1 else "Unknown",
            description=interaction_result.get('description', 'No specific information available.')
        )
    
    def _generate_info_response(self, entities, drug_info):
        """Generate response for drug information queries"""
        drugs = entities.get('drugs', [])
        
        if not drugs:
            return "Which drug would you like information about?"
        
        if not drug_info:
            return f"I don't have information about {drugs[0]}. Try asking about another medication."
        
        template = random.choice(self.info_responses)
        return template.format(**drug_info)
    
    def _generate_side_effect_response(self, entities, drug_info):
        """Generate response for side effect queries"""
        drugs = entities.get('drugs', [])
        
        if not drugs:
            return "Which drug's side effects would you like to know about?"
        
        if not drug_info or not drug_info.get('side_effects'):
            return f"I don't have side effect information for {drugs[0]}."
        
        template = random.choice(self.side_effect_responses)
        return template.format(
            drug=drugs[0].capitalize(),
            side_effects=drug_info.get('side_effects', 'Not specified')
        )
    
    def _generate_dosage_response(self, entities, drug_info):
        """Generate response for dosage queries"""
        drugs = entities.get('drugs', [])
        
        if not drugs:
            return "Which drug's dosage would you like to know about?"
        
        if not drug_info or not drug_info.get('dosage'):
            return f"I don't have dosage information for {drugs[0]}. Always follow your doctor's prescription."
        
        template = random.choice(self.dosage_responses)
        return template.format(
            drug=drugs[0].capitalize(),
            dosage=drug_info.get('dosage', 'Not specified')
        )
    
    def _generate_contraindication_response(self, entities, drug_info):
        """Generate response for contraindication queries"""
        drugs = entities.get('drugs', [])
        
        if not drugs:
            return "Which drug's contraindications would you like to know about?"
        
        if not drug_info or not drug_info.get('contraindications'):
            return f"I don't have contraindication information for {drugs[0]}."
        
        return f"**Who should avoid {drugs[0].capitalize()}:**\n{drug_info.get('contraindications')}"
    
    def _get_random_response(self, response_list):
        """Get random response from a list"""
        return random.choice(response_list) if response_list else "I'm not sure how to respond to that."