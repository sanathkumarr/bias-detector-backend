import spacy
import re
from difflib import Differ

# Load NLP Model
nlp = spacy.load("en_core_web_sm")

# List of emotional/bias-inducing words to replace
BIAS_WORDS = {
    "outrage": "concern",
    "scandal": "controversy",
    "shocking": "unexpected",
    "horrific": "serious",
    "disaster": "crisis",
    "unprecedented": "significant",
    "dangerous": "risky"
}

def replace_biased_words(text):
    """Replaces biased words with neutral alternatives."""
    words = text.split()
    for i, word in enumerate(words):
        clean_word = re.sub(r'[^\w\s]', '', word).lower()
        if clean_word in BIAS_WORDS:
            words[i] = BIAS_WORDS[clean_word]
    return " ".join(words)

def integrate_missing_context(original_text, alternative_articles):
    """Integrates missing context from alternative sources."""
    original_doc = nlp(original_text)
    alt_texts = " ".join([alt["text"] for alt in alternative_articles])
    alt_doc = nlp(alt_texts)

    original_nouns = {token.lemma_ for token in original_doc if token.pos_ == "NOUN"}
    alt_nouns = {token.lemma_ for token in alt_doc if token.pos_ == "NOUN"}

    missing_terms = alt_nouns - original_nouns

    for term in missing_terms:
        if term in alt_texts:
            context_sentence = next((sent.text for sent in alt_doc.sents if term in sent.text), None)
            if context_sentence:
                original_text += " " + context_sentence

    return original_text

def generate_redlined_version(original, rewritten):
    """Creates a redline version showing differences between original and rewritten text."""
    differ = Differ()
    diff = list(differ.compare(original.split(), rewritten.split()))
    
    redlined_text = " ".join(["**" + word[2:] + "**" if word.startswith("- ") else word[2:] for word in diff if word[:2] in ("- ", "+ ")])
    return redlined_text

def rewrite_text(original_text, alternative_articles):
    """Main function to rewrite biased text into a neutral version."""
    # Step 1: Replace biased words
    neutral_text = replace_biased_words(original_text)

    # Step 2: Integrate missing context
    rewritten_text = integrate_missing_context(neutral_text, alternative_articles)

    # Step 3: Generate redline changes
    redlined_text = generate_redlined_version(original_text, rewritten_text)

    return rewritten_text, redlined_text
