"""
Main Flask Application for AI Drug Interaction Chatbot
Member 1 Implementation
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
import sqlite3
from datetime import timedelta
import json

# Import Member 2's modules (placeholders for now)
from backend.chatbot.intent_classifier import IntentClassifier
from backend.chatbot.entity_extractor import EntityExtractor
from backend.chatbot.response_generator import ResponseGenerator
from backend.database.drug_db import DrugDatabase
from backend.database.interaction_checker import InteractionChecker

def create_app():
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    
    # Configuration
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['DATABASE'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'drug_chatbot.db')
    
    # Initialize CORS
    CORS(app)
    
    # Ensure data directory exists
    os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data'), exist_ok=True)
    
    # Initialize database (Member 1's task)
    init_database(app)
    
    # Register routes
    register_routes(app)
    
    return app

def init_database(app):
    """Initialize SQLite database with drug information"""
    db_path = app.config['DATABASE']
    
    # Create tables if they don't exist
    conn = sqlite3.connect(db_path)
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
    
    print("✅ Database initialized successfully!")

def register_routes(app):
    """Register all application routes"""
    
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/chat')
    def chat():
        """Chat interface"""
        # Initialize session for chat history
        if 'chat_history' not in session:
            session['chat_history'] = []
        
        # Pass current datetime to template
        from datetime import datetime
        return render_template('chat.html', now=datetime.now())
    
    @app.route('/about')
    def about():
        """About page"""
        return render_template('about.html')
    
    @app.route('/api/chat', methods=['POST'])
    def chat_api():
        """API endpoint for chat messages"""
        try:
            data = request.json
            user_message = data.get('message', '')
            
            if not user_message:
                return jsonify({'error': 'No message provided'}), 400
            
            # Initialize session if needed
            if 'session_id' not in session:
                session['session_id'] = os.urandom(16).hex()
            
            # TODO: Member 2 will implement the actual NLP logic
            # For now, return a placeholder response
            response = {
                'message': user_message,
                'response': "🤖 I'm learning about drugs! This feature is being implemented by Member 2.",
                'intent': 'unknown',
                'drugs': [],
                'timestamp': str(datetime.now())
            }
            
            # Store in database (Member 1's task)
            store_chat_message(session['session_id'], user_message, response)
            
            return jsonify(response)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/drugs/search', methods=['GET'])
    def search_drugs():
        """Search for drugs in database"""
        query = request.args.get('q', '')
        if len(query) < 2:
            return jsonify([])
        
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, generic_name, category FROM drugs WHERE name LIKE ? OR generic_name LIKE ? LIMIT 10",
            (f'%{query}%', f'%{query}%')
        )
        results = [{'name': row[0], 'generic': row[1], 'category': row[2]} for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(results)
    
    @app.route('/api/drugs/<drug_name>')
    def get_drug_info(drug_name):
        """Get detailed information about a specific drug"""
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM drugs WHERE name = ?",
            (drug_name,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return jsonify({
                'id': row[0],
                'name': row[1],
                'generic': row[2],
                'category': row[3],
                'description': row[4],
                'side_effects': row[5],
                'contraindications': row[6],
                'dosage': row[7]
            })
        return jsonify({'error': 'Drug not found'}), 404
    
    @app.route('/api/history')
    def get_chat_history():
        """Get chat history for current session"""
        if 'session_id' not in session:
            return jsonify([])
        
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_message, bot_response, timestamp FROM chat_history WHERE session_id = ? ORDER BY timestamp DESC LIMIT 50",
            (session['session_id'],)
        )
        history = [{'user': row[0], 'bot': row[1], 'time': row[2]} for row in cursor.fetchall()]
        conn.close()
        
        return jsonify(history)

def store_chat_message(session_id, user_message, response_data):
    """Store chat message in database"""
    try:
        conn = sqlite3.connect(create_app().config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (session_id, user_message, bot_response, intent, drugs_mentioned) VALUES (?, ?, ?, ?, ?)",
            (session_id, user_message, response_data['response'], response_data.get('intent', ''), ','.join(response_data.get('drugs', [])))
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error storing chat: {e}")

# Import datetime for timestamp
from datetime import datetime