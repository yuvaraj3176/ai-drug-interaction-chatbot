"""
SQLite Database Setup and Initialization
Member 1 Implementation
"""

import sqlite3
import csv
import os
import pandas as pd

class DatabaseSetup:
    def __init__(self, db_path='data/drug_chatbot.db'):
        self.db_path = db_path
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def create_tables(self):
        """Create all necessary tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Drugs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drugs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                generic_name TEXT,
                category TEXT,
                description TEXT,
                side_effects TEXT,
                contraindications TEXT,
                dosage_info TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Interactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                drug1_id INTEGER,
                drug2_id INTEGER,
                severity TEXT CHECK(severity IN ('mild', 'moderate', 'severe', 'contraindicated')),
                description TEXT,
                mechanism TEXT,
                recommendation TEXT,
                FOREIGN KEY (drug1_id) REFERENCES drugs(id),
                FOREIGN KEY (drug2_id) REFERENCES drugs(id)
            )
        ''')
        
        # Chat history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                user_message TEXT,
                bot_response TEXT,
                intent TEXT,
                drugs_mentioned TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Tables created successfully")
    
    def load_sample_drug_data(self):
        """Load sample drug data from CSV or create sample data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Sample drug data (in real project, this would come from CSV/API)
        sample_drugs = [
            ('Paracetamol', 'Acetaminophen', 'Pain Relief', 'Used for pain and fever relief', 'Nausea, rash', 'Liver disease', '500mg every 4-6 hours'),
            ('Ibuprofen', 'NSAID', 'Pain Relief', 'Anti-inflammatory pain reliever', 'Stomach upset, heartburn', 'Asthma, stomach ulcers', '200-400mg every 6-8 hours'),
            ('Aspirin', 'Acetylsalicylic acid', 'Pain Relief', 'Pain reliever and blood thinner', 'Stomach irritation, bleeding', 'Bleeding disorders, children under 12', '75-100mg daily'),
            ('Metformin', 'Glucophage', 'Diabetes', 'First-line medication for type 2 diabetes', 'Nausea, diarrhea', 'Kidney disease, alcoholism', '500mg twice daily'),
            ('Amoxicillin', 'Penicillin', 'Antibiotic', 'Treats bacterial infections', 'Diarrhea, rash', 'Penicillin allergy', '250-500mg three times daily'),
            ('Lisinopril', 'ACE Inhibitor', 'Blood Pressure', 'Treats high blood pressure', 'Cough, dizziness', 'Pregnancy, angioedema', '10mg daily'),
            ('Omeprazole', 'Proton Pump Inhibitor', 'Acid Reflux', 'Reduces stomach acid', 'Headache, nausea', 'Long-term use', '20mg daily'),
            ('Sertraline', 'SSRI', 'Antidepressant', 'Treats depression and anxiety', 'Nausea, insomnia', 'MAOI use', '50mg daily'),
            ('Simvastatin', 'Statin', 'Cholesterol', 'Lowers cholesterol', 'Muscle pain', 'Liver disease, pregnancy', '20mg daily'),
            ('Warfarin', 'Anticoagulant', 'Blood Thinner', 'Prevents blood clots', 'Bleeding, bruising', 'Pregnancy, bleeding disorders', '5mg daily')
        ]
        
        for drug in sample_drugs:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO drugs 
                    (name, generic_name, category, description, side_effects, contraindications, dosage_info) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', drug)
            except:
                pass
        
        conn.commit()
        
        # Sample interactions
        self.load_sample_interactions(cursor)
        
        conn.close()
        print("✅ Sample drug data loaded successfully")
    
    def load_sample_interactions(self, cursor):
        """Load sample drug interactions"""
        
        # Get drug IDs
        cursor.execute("SELECT id, name FROM drugs")
        drugs = {row[1]: row[0] for row in cursor.fetchall()}
        
        sample_interactions = [
            (drugs.get('Paracetamol'), drugs.get('Ibuprofen'), 'moderate', 
             'Increased risk of kidney damage when taken together long-term',
             'Both drugs metabolized in kidneys', 'Maintain 6-hour gap between doses'),
            
            (drugs.get('Aspirin'), drugs.get('Ibuprofen'), 'moderate',
             'Increased risk of stomach bleeding',
             'Both affect platelet function and stomach lining',
             'Avoid combination; use alternative pain reliever'),
            
            (drugs.get('Warfarin'), drugs.get('Aspirin'), 'severe',
             'Significantly increased bleeding risk',
             'Both are anticoagulants', 'Avoid combination unless prescribed by doctor'),
            
            (drugs.get('Metformin'), drugs.get('Lisinopril'), 'mild',
             'May affect blood sugar levels',
             'Both can affect glucose metabolism',
             'Monitor blood sugar regularly'),
            
            (drugs.get('Amoxicillin'), drugs.get('Warfarin'), 'moderate',
             'Increased bleeding risk',
             'Antibiotics can alter gut flora affecting vitamin K',
             'Monitor INR more frequently'),
            
            (drugs.get('Sertraline'), drugs.get('Ibuprofen'), 'moderate',
             'Increased risk of bleeding',
             'SSRI + NSAID combination affects platelet function',
             'Use with caution; monitor for bruising/bleeding'),
            
            (drugs.get('Simvastatin'), drugs.get('Amoxicillin'), 'mild',
             'No significant interaction expected',
             'Different metabolic pathways',
             'Generally safe to use together')
        ]
        
        for interaction in sample_interactions:
            if None not in interaction[:2]:  # Check both drugs exist
                try:
                    cursor.execute('''
                        INSERT OR IGNORE INTO interactions 
                        (drug1_id, drug2_id, severity, description, mechanism, recommendation) 
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', interaction)
                except:
                    pass
    
    def export_to_csv(self):
        """Export database to CSV files"""
        conn = self.get_connection()
        
        # Export drugs
        drugs_df = pd.read_sql_query("SELECT * FROM drugs", conn)
        drugs_df.to_csv('data/drug_database.csv', index=False)
        
        # Export interactions
        interactions_df = pd.read_sql_query("""
            SELECT d1.name as drug1, d2.name as drug2, i.severity, i.description, i.recommendation
            FROM interactions i
            JOIN drugs d1 ON i.drug1_id = d1.id
            JOIN drugs d2 ON i.drug2_id = d2.id
        """, conn)
        interactions_df.to_csv('data/interactions.csv', index=False)
        
        conn.close()
        print("✅ Database exported to CSV files")

def initialize_database():
    """Main function to initialize database"""
    setup = DatabaseSetup()
    setup.create_tables()
    setup.load_sample_drug_data()
    setup.export_to_csv()
    print("\n🎉 Database initialization complete!")
    return setup

if __name__ == "__main__":
    initialize_database()