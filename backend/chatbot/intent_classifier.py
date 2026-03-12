"""
Intent Classifier using NLP and Machine Learning
Member 2 Implementation
"""

import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import json
import os

class IntentClassifier:
    def __init__(self):
        """Initialize the intent classifier with NLP model"""
        self.nlp = spacy.load("en_core_web_sm")
        self.vectorizer = TfidfVectorizer()
        self.intent_patterns = self._load_intent_patterns()
        self.vectorizer.fit(self.intent_patterns['all_patterns'])
        
    def _load_intent_patterns(self):
        """Load intent patterns for classification"""
        patterns = {
            'interaction_check': [
                "can i take {drug1} with {drug2}",
                "is it safe to take {drug1} and {drug2} together",
                "interaction between {drug1} and {drug2}",
                "can {drug1} be taken with {drug2}",
                "does {drug1} interact with {drug2}",
                "taking {drug1} and {drug2} together",
                "combine {drug1} with {drug2}",
                "{drug1} and {drug2} interaction",
                "can i use {drug1} while on {drug2}",
                "mixing {drug1} and {drug2}"
            ],
            'drug_info': [
                "tell me about {drug}",
                "what is {drug} used for",
                "information on {drug}",
                "details about {drug}",
                "what does {drug} do",
                "about {drug} medication",
                "what is {drug}",
                "tell me about {drug} drug",
                "info on {drug}"
            ],
            'side_effects': [
                "side effects of {drug}",
                "what are the side effects of {drug}",
                "does {drug} cause side effects",
                "adverse effects of {drug}",
                "can {drug} cause {effect}",
                "common side effects of {drug}",
                "{drug} side effects",
                "what are the risks of taking {drug}"
            ],
            'dosage': [
                "how much {drug} should i take",
                "dosage of {drug}",
                "recommended dose of {drug}",
                "how often to take {drug}",
                "{drug} dosage instructions",
                "what is the correct dosage for {drug}",
                "how many mg of {drug}",
                "dosing information for {drug}"
            ],
            'contraindications': [
                "who should not take {drug}",
                "contraindications for {drug}",
                "when not to take {drug}",
                "{drug} warnings",
                "who should avoid {drug}",
                "medical conditions that interact with {drug}"
            ],
            'greeting': [
                "hi", "hello", "hey", "good morning", "good afternoon", 
                "good evening", "howdy", "greetings", "what's up"
            ],
            'thanks': [
                "thank you", "thanks", "thank you so much", "thanks a lot",
                "appreciate it", "thank you for your help"
            ],
            'farewell': [
                "bye", "goodbye", "see you later", "take care", "exit",
                "quit", "end chat"
            ]
        }
        
        # Flatten patterns for vectorization
        all_patterns = []
        for intent, pattern_list in patterns.items():
            all_patterns.extend(pattern_list)
            
        return {
            'patterns': patterns,
            'all_patterns': all_patterns
        }
    
    def classify(self, text):
        """
        Classify user intent using multiple methods
        Returns: (intent, confidence_score)
        """
        if not text or len(text.strip()) == 0:
            return 'unknown', 0.0
        
        # Preprocess text
        text = text.lower().strip()
        
        # Method 1: Rule-based matching for greetings (fast)
        simple_intent = self._rule_based_match(text)
        if simple_intent and simple_intent[1] > 0.8:
            return simple_intent
        
        # Method 2: TF-IDF similarity for complex intents
        intent, confidence = self._tfidf_match(text)
        
        # Method 3: SpaCy similarity for better understanding
        if confidence < 0.5:
            spacy_intent, spacy_conf = self._spacy_match(text)
            if spacy_conf > confidence:
                return spacy_intent, spacy_conf
        
        return intent, confidence
    
    def _rule_based_match(self, text):
        """Simple rule-based matching for common intents"""
        # Greeting patterns
        greeting_patterns = [
            r'\bhi\b', r'\bhello\b', r'\bhey\b', r'good morning',
            r'good afternoon', r'good evening', r'greetings'
        ]
        
        for pattern in greeting_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return 'greeting', 0.9
        
        # Thanks patterns
        if re.search(r'thank', text, re.IGNORECASE):
            return 'thanks', 0.9
        
        # Farewell patterns
        if re.search(r'\bbye\b|\bgoodbye\b|see you|take care', text, re.IGNORECASE):
            return 'farewell', 0.9
        
        return None, 0.0
    
    def _tfidf_match(self, text):
        """Match using TF-IDF similarity"""
        # Transform text to vector
        text_vector = self.vectorizer.transform([text])
        
        # Calculate similarity with each pattern
        best_intent = 'unknown'
        best_score = 0.0
        
        for intent, patterns in self.intent_patterns['patterns'].items():
            for pattern in patterns:
                pattern_vector = self.vectorizer.transform([pattern])
                similarity = cosine_similarity(text_vector, pattern_vector)[0][0]
                
                if similarity > best_score:
                    best_score = similarity
                    best_intent = intent
        
        return best_intent, best_score
    
    def _spacy_match(self, text):
        """Use spaCy for semantic similarity"""
        doc = text.lower()
        
        # Keywords for each intent
        intent_keywords = {
            'interaction_check': ['interaction', 'together', 'with', 'combine', 'mix', 'versus', 'vs'],
            'drug_info': ['what', 'about', 'tell', 'information', 'details', 'what is'],
            'side_effects': ['side effect', 'adverse', 'cause', 'risk', 'safe', 'dangerous'],
            'dosage': ['dose', 'how much', 'how many', 'mg', 'milligram', 'take', 'frequency'],
            'contraindications': ['avoid', 'should not', 'contraindication', 'warning', 'contraindicated']
        }
        
        best_intent = 'unknown'
        best_score = 0.0
        words = set(doc.split())
        
        for intent, keywords in intent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in doc) / len(keywords)
            if score > best_score:
                best_score = score
                best_intent = intent
        
        return best_intent, best_score
    
    def get_intent_description(self, intent):
        """Get human-readable description of intent"""
        descriptions = {
            'interaction_check': "Checking drug interactions",
            'drug_info': "Requesting drug information",
            'side_effects': "Asking about side effects",
            'dosage': "Inquiring about dosage",
            'contraindications': "Checking contraindications",
            'greeting': "Greeting",
            'thanks': "Expressing gratitude",
            'farewell': "Ending conversation",
            'unknown': "Unknown intent"
        }
        return descriptions.get(intent, intent)