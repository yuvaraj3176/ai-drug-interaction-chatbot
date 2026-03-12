"""
NLP Model for Drug Interaction Chatbot
Member 2 Implementation
"""

import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import os

class NLPModel:
    def __init__(self):
        """Initialize NLP models"""
        self.nlp = spacy.load("en_core_web_sm")
        self._download_nltk_data()
        self.stop_words = set(stopwords.words('english'))
        
    def _download_nltk_data(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
    
    def preprocess(self, text):
        """
        Preprocess text for NLP tasks
        Returns cleaned and processed text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def tokenize(self, text):
        """Tokenize text into words"""
        return word_tokenize(text)
    
    def remove_stopwords(self, tokens):
        """Remove stopwords from token list"""
        return [token for token in tokens if token not in self.stop_words]
    
    def get_entities(self, text):
        """Extract named entities using spaCy"""
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char
            })
        
        return entities
    
    def get_pos_tags(self, text):
        """Get part-of-speech tags"""
        doc = self.nlp(text)
        return [(token.text, token.pos_) for token in doc]
    
    def get_dependency_parse(self, text):
        """Get dependency parse tree"""
        doc = self.nlp(text)
        dependencies = []
        
        for token in doc:
            dependencies.append({
                'word': token.text,
                'dep': token.dep_,
                'head': token.head.text,
                'children': [child.text for child in token.children]
            })
        
        return dependencies
    
    def extract_keywords(self, text, top_n=5):
        """
        Extract keywords from text using TF-IDF like approach
        (simplified version using noun chunks and entities)
        """
        doc = self.nlp(text)
        keywords = []
        
        # Add named entities
        for ent in doc.ents:
            if ent.text.lower() not in keywords:
                keywords.append(ent.text.lower())
        
        # Add noun chunks
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.lower()
            if chunk_text not in keywords and len(chunk_text.split()) <= 3:
                keywords.append(chunk_text)
        
        # Add important tokens (nouns, proper nouns)
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN', 'ADJ']:
                if token.text.lower() not in keywords:
                    keywords.append(token.text.lower())
        
        return keywords[:top_n]
    
    def calculate_similarity(self, text1, text2):
        """
        Calculate semantic similarity between two texts
        Returns similarity score between 0 and 1
        """
        doc1 = self.nlp(text1)
        doc2 = self.nlp(text2)
        
        return doc1.similarity(doc2)
    
    def detect_language(self, text):
        """Simple language detection (assumes English for now)"""
        # In production, you'd use langdetect or similar
        return 'en'
    
    def get_sentence_embeddings(self, text):
        """Get sentence embeddings using spaCy"""
        doc = self.nlp(text)
        return doc.vector
    
    def extract_medical_terms(self, text):
        """
        Extract medical terms using custom patterns
        """
        medical_patterns = [
            r'\b(drug|medication|medicine|pill|tablet|capsule)\b',
            r'\b(dose|dosage|mg|mcg|gram|ml)\b',
            r'\b(side effect|adverse|reaction|allergy)\b',
            r'\b(interaction|contraindication|warning)\b',
            r'\b(pain|fever|infection|diabetes|pressure|cholesterol)\b'
        ]
        
        medical_terms = []
        text_lower = text.lower()
        
        for pattern in medical_patterns:
            matches = re.findall(pattern, text_lower)
            medical_terms.extend(matches)
        
        return list(set(medical_terms))
    
    def is_medical_query(self, text):
        """
        Check if the query is medical/drug related
        Returns boolean
        """
        medical_keywords = [
            'drug', 'medication', 'medicine', 'pill', 'tablet', 'capsule',
            'dose', 'dosage', 'mg', 'interaction', 'side effect', 'prescribe',
            'doctor', 'pharmacy', 'pharmacist', 'prescription', 'overdose',
            'allergy', 'reaction', 'contraindication', 'warning', 'caution'
        ]
        
        text_lower = text.lower()
        
        for keyword in medical_keywords:
            if keyword in text_lower:
                return True
        
        return False