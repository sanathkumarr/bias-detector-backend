import spacy
import re
from textblob import TextBlob
from collections import Counter
from difflib import SequenceMatcher

# Load NLP Model
nlp = spacy.load("en_core_web_sm")

def calculate_sentiment(text):
    """Returns sentiment polarity (-1 to +1) and subjectivity (0 to 1)."""
    analysis = TextBlob(text)
    return analysis.sentiment.polarity, analysis.sentiment.subjectivity

def detect_emotional_language(text):
    """Detects emotional/sensational words."""
    emotional_words = {"outrage", "scandal", "horrific", "unprecedented", "disaster", "shocking"}
    words = set(re.findall(r'\b\w+\b', text.lower()))
    return len(words & emotional_words) / len(words) if words else 0

def compare_with_alternatives(original, alternatives):
    """Compares original article with alternative sources to check consistency."""
    original_doc = nlp(original)
    alt_texts = " ".join([alt["text"] for alt in alternatives])
    alt_doc = nlp(alt_texts)

    original_nouns = {token.lemma_ for token in original_doc if token.pos_ == "NOUN"}
    alt_nouns = {token.lemma_ for token in alt_doc if token.pos_ == "NOUN"}
    
    missing_info = original_nouns - alt_nouns  # Words present in original but missing in alternatives
    similarity = SequenceMatcher(None, original, alt_texts).ratio()
    
    return similarity, missing_info

def analyze_bias(original_text, alternative_articles):
    """Calculates bias percentage and highlights biased sections."""
    
    # 1. Sentiment Analysis
    polarity, subjectivity = calculate_sentiment(original_text)

    # 2. Emotional Language Detection
    emotional_score = detect_emotional_language(original_text)

    # 3. Comparison with Alternative Sources
    similarity_score, missing_terms = compare_with_alternatives(original_text, alternative_articles)

    # 4. Bias Score Calculation
    bias_score = ((1 - similarity_score) * 50) + (emotional_score * 30) + (subjectivity * 20)
    bias_score = round(min(100, max(0, bias_score)), 2)

    # 5. Highlight Biased Words
    biased_words = list(missing_terms) + list(re.findall(r'\b(?:outrage|scandal|shocking|disaster)\b', original_text, re.I))
    
    highlights = {word: "biased" for word in biased_words}

    return bias_score, highlights, None  # The rewritten text will be generated in Step 5
