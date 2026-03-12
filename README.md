📄 AI-Powered Drug Interaction Chatbot - README.md
Copy and paste this directly into your README.md file:

markdown
# 🤖 AI-Powered Drug Interaction Chatbot

An intelligent chatbot system that uses Natural Language Processing (NLP) to check drug interactions, provide medication information, and alert users about potential adverse effects using drug databases.

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [API Endpoints](#-api-endpoints)
- [NLP Capabilities](#-nlp-capabilities)
- [Database Schema](#-database-schema)
- [Sample Interactions](#-sample-interactions)
- [Team Members](#-team-members)
- [Troubleshooting](#-troubleshooting)
- [Future Scope](#-future-scope)
- [License](#-license)

---

## 🎯 Overview

The **AI-Powered Drug Interaction Chatbot** helps users check potential interactions between medications using advanced NLP and a comprehensive drug database. It understands natural language queries and provides instant, accurate information about drug interactions, side effects, dosage, and contraindications.

### Why This Project?
- ❌ Patients often struggle to check drug interactions quickly
- ❌ Healthcare providers need quick reference tools
- ✅ Our chatbot provides instant, accurate drug information
- ✅ Uses NLP to understand natural language questions
- ✅ Helps prevent adverse drug reactions

---

## ✨ Features

### 🔐 Core Features
- **Natural Language Understanding**: Ask questions in plain English
- **Drug Interaction Checking**: Check interactions between multiple drugs
- **Severity Ratings**: mild, moderate, severe, contraindicated
- **Drug Information**: Get details about any medication
- **Side Effects**: List of common and serious side effects
- **Dosage Information**: Recommended dosage guidelines
- **Contraindications**: Who should avoid specific drugs

### 🤖 NLP Capabilities
- **Intent Classification**: Understands user intention (interaction check, drug info, side effects, etc.)
- **Entity Extraction**: Identifies drug names from natural language
- **Context Understanding**: Handles misspellings and abbreviations
- **Multi-drug Analysis**: Checks interactions among multiple medications

### 🎨 User Interface
- Clean, responsive chat interface
- Severity badges with color coding
- Typing indicators
- Suggestion chips for quick queries
- Mobile-friendly design
- Real-time responses

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Backend** | Python | 3.11 |
| **Web Framework** | Flask | 2.3.3 |
| **NLP** | spaCy, NLTK | 3.7.2, 3.8.1 |
| **ML/AI** | Transformers, PyTorch | 4.36.0, 2.1.0 |
| **Database** | SQLite | - |
| **Data Processing** | Pandas, NumPy | 2.0.3, 1.24.3 |
| **Frontend** | HTML, CSS, JavaScript | - |
| **Styling** | Bootstrap 5 | - |

---

## 📁 Project Structure
ai-drug-interaction-chatbot/
├── backend/
│ ├── init.py
│ ├── app.py # Main Flask application
│ ├── chatbot/
│ │ ├── init.py
│ │ ├── intent_classifier.py # NLP intent recognition
│ │ ├── entity_extractor.py # Drug name extraction
│ │ └── response_generator.py # Response generation
│ ├── database/
│ │ ├── init.py
│ │ ├── drug_db.py # Drug database queries
│ │ ├── interaction_checker.py # Interaction logic
│ │ └── sqlite_setup.py # Database initialization
│ ├── models/
│ │ ├── init.py
│ │ └── nlp_model.py # Core NLP model
│ └── utils/
│ ├── init.py
│ └── data_loader.py # External data loading
├── frontend/
│ ├── static/
│ │ ├── css/
│ │ │ └── style.css
│ │ └── js/
│ │ └── chat.js
│ └── templates/
│ ├── base.html
│ ├── index.html
│ ├── chat.html
│ └── about.html
├── data/
│ ├── drug_chatbot.db # SQLite database
│ ├── drug_database.csv # Sample drug data
│ └── interactions.csv # Sample interactions
├── requirements.txt
├── .gitignore
├── README.md
└── run.py

text

---

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- Git
- pip package manager

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-drug-interaction-chatbot.git
   cd ai-drug-interaction-chatbot
Create virtual environment

bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
Install dependencies

bash
pip install --upgrade pip
pip install -r requirements.txt
Download spaCy model

bash
python -m spacy download en_core_web_sm
Initialize database

bash
python -c "from backend.database.sqlite_setup import initialize_database; initialize_database()"
Run the application

bash
python run.py
Open in browser

text
http://localhost:5000
📖 Usage Guide
Starting the Chat
Open the application in your browser

Click on "Chat" in the navigation bar

Type your question in natural language

Sample Queries to Try
Category	Example Questions
Interaction Check	"Can I take Paracetamol with Ibuprofen?"
"Is it safe to take Warfarin and Aspirin together?"
"Does Metformin interact with Lisinopril?"
Drug Information	"Tell me about Metformin"
"What is Amoxicillin used for?"
"Information on Warfarin"
Side Effects	"Side effects of Aspirin"
"What are the side effects of Ibuprofen?"
"Does Paracetamol cause any side effects?"
Dosage	"How much Metformin should I take?"
"Dosage of Amoxicillin"
"What is the correct dose for Ibuprofen?"
Contraindications	"Who should not take Warfarin?"
"When to avoid Aspirin?"
Understanding Responses
🚫 SEVERE: Dangerous combination, avoid completely

⚠️ MODERATE: Caution advised, monitor closely

📌 MILD: Minor interaction, usually safe

✅ NONE: No known interaction

🔌 API Endpoints
Endpoint	Method	Description
/	GET	Home page
/chat	GET	Chat interface
/about	GET	About page
/api/chat	POST	Send message to chatbot
/api/drugs/search?q={query}	GET	Search for drugs
/api/drugs/{drug_name}	GET	Get drug information
/api/history	GET	Get chat history
API Request Example
bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Can I take Paracetamol with Ibuprofen?"}'
API Response Example
json
{
  "message": "Can I take Paracetamol with Ibuprofen?",
  "response": "⚠️ MODERATE INTERACTION: Paracetamol and Ibuprofen may interact. Increased risk of kidney damage when taken together long-term.",
  "intent": "interaction_check",
  "confidence": 0.85,
  "drugs": ["paracetamol", "ibuprofen"],
  "interaction": {
    "severity": "moderate",
    "description": "Increased risk of kidney damage when taken together long-term",
    "recommendation": "Maintain 6-hour gap between doses"
  }
}
🧠 NLP Capabilities
Intent Classification
The system can identify 8 different intents:

interaction_check - Checking drug interactions

drug_info - Requesting drug information

side_effects - Asking about side effects

dosage - Inquiring about dosage

contraindications - Checking contraindications

greeting - Greeting the bot

thanks - Expressing gratitude

farewell - Ending conversation

Entity Extraction
Extracts drug names from natural language

Handles misspellings (e.g., "paracetomol" → "paracetamol")

Recognizes abbreviations (e.g., "NSAID", "BP")

Identifies multiple drugs in a single query

Confidence Scoring
High confidence (>0.8): Direct match

Medium confidence (0.5-0.8): Fuzzy match

Low confidence (<0.5): Fallback to unknown

💾 Database Schema
Drugs Table
sql
CREATE TABLE drugs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    generic_name TEXT,
    category TEXT,
    description TEXT,
    side_effects TEXT,
    contraindications TEXT,
    dosage_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Interactions Table
sql
CREATE TABLE interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drug1_id INTEGER,
    drug2_id INTEGER,
    severity TEXT CHECK(severity IN ('mild', 'moderate', 'severe', 'contraindicated')),
    description TEXT,
    mechanism TEXT,
    recommendation TEXT,
    FOREIGN KEY (drug1_id) REFERENCES drugs(id),
    FOREIGN KEY (drug2_id) REFERENCES drugs(id)
);
Chat History Table
sql
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    user_message TEXT,
    bot_response TEXT,
    intent TEXT,
    drugs_mentioned TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
📊 Sample Drug Data
The database includes 10 sample drugs with interactions:

Drug Name	Generic Name	Category
Paracetamol	Acetaminophen	Pain Relief
Ibuprofen	NSAID	Pain Relief
Aspirin	Acetylsalicylic acid	Pain Relief
Metformin	Glucophage	Diabetes
Amoxicillin	Penicillin	Antibiotic
Lisinopril	ACE Inhibitor	Blood Pressure
Omeprazole	Proton Pump Inhibitor	Acid Reflux
Sertraline	SSRI	Antidepressant
Simvastatin	Statin	Cholesterol
Warfarin	Anticoagulant	Blood Thinner
🎯 Sample Interactions
Drug 1	Drug 2	Severity	Description
Paracetamol	Ibuprofen	Moderate	Increased kidney risk
Aspirin	Ibuprofen	Moderate	Stomach bleeding risk
Warfarin	Aspirin	Severe	Increased bleeding risk
Metformin	Lisinopril	Mild	Blood sugar effects
Amoxicillin	Warfarin	Moderate	Altered INR
Sertraline	Ibuprofen	Moderate	Bleeding risk
👥 Team Members
Member 1 (Backend & Infrastructure)
GitHub repository setup

Flask application structure

Database design and initialization

HTML templates and routing

Session management

CSV data storage

Member 2 (NLP & Intelligence)
Intent classification system

Entity extraction from text

Response generation logic

Drug interaction checking

NLP model integration

Chat UI enhancements

API endpoints for chat

🔧 Troubleshooting
Problem	Solution
Module not found	Run pip install -r requirements.txt
spaCy model missing	Run python -m spacy download en_core_web_sm
Database not initialized	Run database setup script
Port 5000 in use	Change port in run.py
Chat not responding	Check Flask server is running
Drugs not found	Ensure database has data
NLP errors	Verify spaCy installation
Common Fixes
bash
# Reinstall all packages
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Reset database
del data\drug_chatbot.db
python -c "from backend.database.sqlite_setup import initialize_database; initialize_database()"

# Restart Flask
# Press Ctrl+C and run again
python run.py
🚀 Future Scope
Web Deployment - Deploy on PythonAnywhere/Heroku

Mobile App - React Native / Flutter app

Voice Interface - Speech-to-text integration

Image Recognition - Identify pills from photos

Real Drug APIs - Integrate with FDA/DrugBank APIs

Multi-language Support - Spanish, French, etc.

User Accounts - Save chat history per user

Email Reports - Send interaction reports

Doctor Consultation - Connect to healthcare providers

Emergency Alerts - Flag severe interactions

📝 Requirements.txt
txt
Flask==2.3.3
Flask-CORS==4.0.0
Flask-Session==0.5.0
spacy==3.7.2
nltk==3.8.1
transformers==4.36.0
torch==2.1.0
pandas==2.0.3
numpy==1.24.3
SQLAlchemy==2.0.23
scikit-learn==1.3.2
python-dotenv==1.0.0
requests==2.31.0
⚠️ Disclaimer
IMPORTANT: This chatbot is for informational and educational purposes only. It should not replace professional medical advice. Always consult a healthcare provider or pharmacist before taking any medication or changing your medication routine.
