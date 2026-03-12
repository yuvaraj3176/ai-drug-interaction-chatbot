"""
Drug Interaction Checker - Check interactions between medications
Member 2 Implementation
"""

import sqlite3
from itertools import combinations

class InteractionChecker:
    def __init__(self, db_path='data/drug_chatbot.db'):
        """Initialize interaction checker"""
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def check_interaction(self, drug1_name, drug2_name):
        """
        Check interaction between two drugs by name
        Returns interaction details or None
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get drug IDs
        cursor.execute("SELECT id FROM drugs WHERE name = ?", (drug1_name,))
        drug1 = cursor.fetchone()
        
        cursor.execute("SELECT id FROM drugs WHERE name = ?", (drug2_name,))
        drug2 = cursor.fetchone()
        
        if not drug1 or not drug2:
            conn.close()
            return None
        
        # Check interaction in both orders
        cursor.execute("""
            SELECT i.*, d1.name as drug1_name, d2.name as drug2_name
            FROM interactions i
            JOIN drugs d1 ON i.drug1_id = d1.id
            JOIN drugs d2 ON i.drug2_id = d2.id
            WHERE (drug1_id = ? AND drug2_id = ?) OR (drug1_id = ? AND drug2_id = ?)
        """, (drug1[0], drug2[0], drug2[0], drug1[0]))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'drug1': row[7],  # drug1_name
                'drug2': row[8],  # drug2_name
                'severity': row[3],
                'description': row[4],
                'mechanism': row[5],
                'recommendation': row[6]
            }
        
        # No interaction found
        return {
            'drug1': drug1_name,
            'drug2': drug2_name,
            'severity': 'none',
            'description': f"No known interaction between {drug1_name} and {drug2_name}.",
            'recommendation': "These medications are generally safe to take together."
        }
    
    def check_multiple_drugs(self, drug_list):
        """
        Check interactions among multiple drugs
        Returns list of all interactions found
        """
        if len(drug_list) < 2:
            return []
        
        interactions = []
        
        # Check all pairs
        for drug1, drug2 in combinations(drug_list, 2):
            interaction = self.check_interaction(drug1, drug2)
            if interaction and interaction.get('severity') != 'none':
                interactions.append(interaction)
        
        return interactions
    
    def get_severe_interactions(self, drug_list):
        """Get only severe interactions from a drug list"""
        all_interactions = self.check_multiple_drugs(drug_list)
        return [i for i in all_interactions if i.get('severity') in ['severe', 'contraindicated']]
    
    def get_interaction_summary(self, drug_list):
        """
        Get a summary of all interactions for a drug list
        Returns dictionary with counts by severity
        """
        interactions = self.check_multiple_drugs(drug_list)
        
        summary = {
            'severe': 0,
            'moderate': 0,
            'mild': 0,
            'total': len(interactions),
            'details': interactions
        }
        
        for interaction in interactions:
            severity = interaction.get('severity', 'unknown')
            if severity in summary:
                summary[severity] += 1
        
        return summary
    
    def is_safe_combination(self, drug_list):
        """
        Check if a combination of drugs is safe
        Returns (bool, list of issues)
        """
        interactions = self.check_multiple_drugs(drug_list)
        severe_interactions = [i for i in interactions if i.get('severity') in ['severe', 'contraindicated']]
        
        if severe_interactions:
            return False, severe_interactions
        return True, interactions
    
    def get_drug_interactions(self, drug_name):
        """
        Get all known interactions for a specific drug
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get drug ID
        cursor.execute("SELECT id FROM drugs WHERE name = ?", (drug_name,))
        drug = cursor.fetchone()
        
        if not drug:
            conn.close()
            return []
        
        # Get all interactions involving this drug
        cursor.execute("""
            SELECT d1.name, d2.name, i.severity, i.description, i.recommendation
            FROM interactions i
            JOIN drugs d1 ON i.drug1_id = d1.id
            JOIN drugs d2 ON i.drug2_id = d2.id
            WHERE drug1_id = ? OR drug2_id = ?
        """, (drug[0], drug[0]))
        
        interactions = []
        for row in cursor.fetchall():
            # Determine which drug is the other one
            other_drug = row[1] if row[0] == drug_name else row[0]
            interactions.append({
                'drug': other_drug,
                'severity': row[2],
                'description': row[3],
                'recommendation': row[4]
            })
        
        conn.close()
        return interactions