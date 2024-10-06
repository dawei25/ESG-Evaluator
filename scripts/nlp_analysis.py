import spacy
from transformers import pipeline
import pandas as pd
import psycopg2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import joblib
import os
from dotenv import load_dotenv

load_dotenv()

# Load pre-trained models
nlp = spacy.load("en_core_web_sm")
sentiment_analyzer = pipeline("sentiment-analysis")

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

# Extract ESG-related entities
def extract_esg_entities(text):
    doc = nlp(text)
    esg_entities = {
        "Environmental": [],
        "Social": [],
        "Governance": []
    }
    
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "EVENT"]:
            if any(keyword in ent.text.lower() for keyword in ["sustainability", "renewable", "emission"]):
                esg_entities["Environmental"].append(ent.text)
            elif any(keyword in ent.text.lower() for keyword in ["diversity", "inclusion", "community"]):
                esg_entities["Social"].append(ent.text)
            elif any(keyword in ent.text.lower() for keyword in ["board", "compliance", "ethics"]):
                esg_entities["Governance"].append(ent.text)
    
    return esg_entities

# Perform sentiment analysis
def analyze_sentiment(text):
    result = sentiment_analyzer(text[:512])[0]  # BERT models typically have a max length of 512 tokens
    return result['label'], result['score']

# Train ESG classifier
def train_esg_classifier(X, y):
    vectorizer = TfidfVectorizer(max_features=5000)
    X_vectorized = vectorizer.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)
    
    classifier = MultinomialNB()
    classifier.fit(X_train, y_train)
    
    accuracy = classifier.score(X_test, y_test)
    print(f"Classifier accuracy: {accuracy}")
    
    joblib.dump(vectorizer, 'esg_vectorizer.joblib')
    joblib.dump(classifier, 'esg_classifier.joblib')

# Classify ESG content
def classify_esg_content(text):
    vectorizer = joblib.load('esg_vectorizer.joblib')
    classifier = joblib.load('esg_classifier.joblib')
    
    X_vectorized = vectorizer.transform([text])
    prediction = classifier.predict(X_vectorized)
    
    return prediction[0]

# Calculate ESG score
def calculate_esg_score(entities, sentiment, classification):
    # This is a simplified scoring method. You may want to develop a more sophisticated algorithm.
    entity_score = sum(len(entities[category]) for category in entities) / 10  # Normalize to 0-1 range
    sentiment_score = 1 if sentiment[0] == 'POSITIVE' else 0
    classification_score = {'E': 0.33, 'S': 0.33, 'G': 0.33}.get(classification, 0)
    
    return (entity_score + sentiment_score + classification_score) / 3  # Average of all factors

# Process and score company data
def process_company_data(company_name):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Fetch all relevant data for the company
        cur.execute("""
            SELECT content FROM sec_filings sf
            JOIN companies c ON sf.company_cik = c.cik
            WHERE c.name = %s
            UNION ALL
            SELECT content FROM news_articles
            WHERE company_name = %s
            UNION ALL
            SELECT content FROM website_data wd
            JOIN companies c ON wd.url = c.website
            WHERE c.name = %s
        """, (company_name, company_name, company_name))
        
        all_content = cur.fetchall()
        
        esg_scores = []
        for content in all_content:
            entities = extract_esg_entities(content[0])
            sentiment = analyze_sentiment(content[0])
            classification = classify_esg_content(content[0])
            score = calculate_esg_score(entities, sentiment, classification)
            esg_scores.append(score)
        
        overall_score = sum(esg_scores) / len(esg_scores)
        
        # Update the company's ESG score in the database
        cur.execute("""
            UPDATE companies
            SET esg_score = %s, last_updated = NOW()
            WHERE name = %s
        """, (overall_score, company_name))
        
        conn.commit()
        
        return overall_score
    
    except Exception as e:
        conn.rollback()
        print(f"Error processing company data: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    # Example usage
    company_name = "Apple Inc."
    esg_score = process_company_data(company_name)
    print(f"ESG Score for {company_name}: {esg_score}")