CVR College of Engineering AI Chatbot — Python/Streamlit Version
=================================================================

SETUP INSTRUCTIONS
------------------
1. Make sure Python 3.8+ is installed.

2. Install dependencies:
   pip install -r requirements.txt

3. Run the app:
   streamlit run app.py

4. Open your browser to:
   http://localhost:8501

FILES
-----
app.py            — Main Streamlit application (UI + chat logic)
nlp_engine.py     — NLP engine: query normalisation, TF-IDF, cosine similarity
knowledge_base.py — Complete CVR knowledge base (all topics)
requirements.txt  — Python dependencies

FEATURES
--------
- 40+ knowledge topics covering admissions, fees, hostel, placements, faculty, labs, transport, etc.
- TF-IDF + cosine similarity search engine for accurate answers
- Query normalisation map: understands casual questions like "how much fee?"
- Clean professional UI with navy/gold theme matching CVR branding
- Collapsible sidebar with 8 question categories and 30+ quick question buttons
- Chat history within session
- Clear chat button

CONTACT
-------
CVR College of Engineering
www.cvr.ac.in | +91-9100100510 | Ibrahimpatnam, Rangareddy, Telangana - 501510
