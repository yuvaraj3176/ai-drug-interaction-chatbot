"""
Drug Database Handler - Query and manage drug information
Member 2 Implementation
"""

import sqlite3
import os

class DrugDatabase:
    def __init__(self, db_path='data/drug_chatbot.db'):
        """Initialize database connection"""
        self.db_path = db_path
        
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def search_drugs(self, query):
        """
        Search for drugs matching the query
        Returns list of matching drugs
        """
        if not query or len(query) < 2:
            return []
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Search by name or generic name
        cursor.execute("""
            SELECT id, name, generic_name, category 
            FROM drugs 
            WHERE name LIKE ? OR generic_name LIKE ?
            ORDER BY name
            LIMIT 10
        """, (f'%{query}%', f'%{query}%'))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'name': row[1],
                'generic_name': row[2],
                'category': row[3]
            })
        
        conn.close()
        return results
    
    def get_drug_info(self, drug_name):
        """
        Get complete information about a specific drug
        Returns dictionary with drug details
        """
        if not drug_name:
            return None
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM drugs WHERE name = ? OR generic_name = ?
        """, (drug_name, drug_name))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'generic_name': row[2],
                'category': row[3],
                'description': row[4],
                'side_effects': row[5],
                'contraindications': row[6],
                'dosage': row[7]
            }
        return None
    
    def get_drug_by_id(self, drug_id):
        """Get drug information by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM drugs WHERE id = ?", (drug_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'generic_name': row[2],
                'category': row[3],
                'description': row[4],
                'side_effects': row[5],
                'contraindications': row[6],
                'dosage': row[7]
            }
        return None
    
    def get_drug_id(self, drug_name):
        """Get drug ID by name"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM drugs WHERE name = ?", (drug_name,))
        row = cursor.fetchone()
        conn.close()
        
        return row[0] if row else None
    
    def get_all_drugs(self):
        """Get list of all drugs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, generic_name, category FROM drugs ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        
        return [{'name': row[0], 'generic': row[1], 'category': row[2]} for row in rows]
    
    def get_drugs_by_category(self, category):
        """Get drugs by category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, generic_name FROM drugs WHERE category = ? ORDER BY name", (category,))
        rows = cursor.fetchall()
        conn.close()
        
        return [{'name': row[0], 'generic': row[1]} for row in rows]
    
    def search_by_condition(self, condition_keyword):
        """
        Search drugs by medical condition they treat
        (searches in description field)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name, generic_name, category, description 
            FROM drugs 
            WHERE description LIKE ?
            LIMIT 10
        """, (f'%{condition_keyword}%',))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [{
            'name': row[0],
            'generic': row[1],
            'category': row[2],
            'description': row[3]
        } for row in rows]