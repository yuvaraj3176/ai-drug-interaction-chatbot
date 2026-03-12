"""
Entity Extractor for Drug Names and Medical Terms
Member 2 Implementation
"""

import re
import spacy
from difflib import get_close_matches

class EntityExtractor:
    def __init__(self, drug_list=None):
        """Initialize entity extractor with NLP model"""
        self.nlp = spacy.load("en_core_web_sm")
        self.drug_list = drug_list or self._get_default_drug_list()
        self.common_misspellings = self._load_misspellings()
        
    def _get_default_drug_list(self):
        """Default list of common drugs"""
        return [
            'paracetamol', 'ibuprofen', 'aspirin', 'metformin', 'amoxicillin',
            'lisinopril', 'omeprazole', 'sertraline', 'simvastatin', 'warfarin',
            'atorvastatin', 'levothyroxine', 'amlodipine', 'metoprolol', 'albuterol',
            'gabapentin', 'hydrochlorothiazide', 'losartan', 'clopidogrel', 'prednisone'
        ]
    
    def _load_misspellings(self):
        """Common misspellings and abbreviations"""
        return {
            'paracetamol': ['paraceta mol', 'paracetomol', 'pcm', 'acetaminophen'],
            'ibuprofen': ['ibrufen', 'brufen', 'motrin', 'advil'],
            'aspirin': ['asprin', 'acetylsalicylic acid', 'asa'],
            'metformin': ['metformine', 'glucophage'],
            'amoxicillin': ['amoxcillin', 'amoxycillin', 'amoxil'],
            'warfarin': ['warfrin', 'coumadin']
        }
    
    def extract_drugs(self, text):
        """
        Extract drug names from text
        Returns list of drugs found
        """
        if not text:
            return []
        
        # Preprocess text
        text = text.lower().strip()
        drugs_found = []
        
        # Method 1: Direct matching from drug list
        direct_matches = self._direct_match(text)
        drugs_found.extend(direct_matches)
        
        # Method 2: Handle misspellings and abbreviations
        fuzzy_matches = self._fuzzy_match(text)
        for drug in fuzzy_matches:
            if drug not in drugs_found:
                drugs_found.append(drug)
        
        # Method 3: Use spaCy NER for medical entities
        spacy_matches = self._spacy_extract(text)
        for drug in spacy_matches:
            if drug not in drugs_found:
                drugs_found.append(drug)
        
        return drugs_found
    
    def _direct_match(self, text):
        """Direct string matching"""
        found = []
        words = text.split()
        
        for i in range(len(words)):
            # Check single words
            if words[i] in self.drug_list:
                found.append(words[i])
            
            # Check two-word combinations
            if i < len(words) - 1:
                two_words = f"{words[i]} {words[i+1]}"
                if two_words in self.drug_list:
                    found.append(two_words)
        
        return found
    
    def _fuzzy_match(self, text):
        """Fuzzy matching for misspellings"""
        found = []
        words = text.split()
        
        for word in words:
            # Check direct misspellings
            for correct, misspellings in self.common_misspellings.items():
                if word in misspellings and correct not in found:
                    found.append(correct)
            
            # Use difflib for close matches
            matches = get_close_matches(word, self.drug_list, cutoff=0.8)
            for match in matches:
                if match not in found:
                    found.append(match)
        
        return found
    
    def _spacy_extract(self, text):
        """Use spaCy for entity extraction"""
        doc = self.nlp(text)
        found = []
        
        # Look for entities tagged as drugs/medications
        for ent in doc.ents:
            if ent.label_ in ['DRUG', 'MEDICATION', 'CHEMICAL']:
                drug_name = ent.text.lower()
                # Check if it matches or is close to known drugs
                matches = get_close_matches(drug_name, self.drug_list, cutoff=0.7)
                if matches and matches[0] not in found:
                    found.append(matches[0])
        
        # Also look for noun chunks that might be drug names
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.lower()
            if len(chunk_text.split()) <= 2:  # Max 2 words
                matches = get_close_matches(chunk_text, self.drug_list, cutoff=0.7)
                if matches and matches[0] not in found:
                    found.append(matches[0])
        
        return found
    
    def extract_entities(self, text):
        """
        Extract all relevant entities from text
        Returns dictionary with different entity types
        """
        doc = self.nlp(text)
        entities = {
            'drugs': self.extract_drugs(text),
            'conditions': [],
            'symptoms': [],
            'numbers': [],
            'units': [],
            'negations': []
        }
        
        # Extract numerical entities (dosage amounts)
        for token in doc:
            if token.pos_ == 'NUM':
                entities['numbers'].append(token.text)
            
            # Look for units (mg, ml, etc.)
            if token.text.lower() in ['mg', 'ml', 'gram', 'tablet', 'capsule']:
                entities['units'].append(token.text)
            
            # Look for negations (not, no, avoid)
            if token.dep_ == 'neg' or token.text.lower() in ['no', 'not', 'never']:
                entities['negations'].append(token.text)
        
        return entities
    
    def get_drug_pairs(self, text):
        """
        Extract pairs of drugs for interaction checking
        Returns list of drug pairs found in text
        """
        drugs = self.extract_drugs(text)
        pairs = []
        
        if len(drugs) >= 2:
            # If multiple drugs, create pairs
            for i in range(len(drugs)):
                for j in range(i+1, len(drugs)):
                    pairs.append((drugs[i], drugs[j]))
        
        return pairs