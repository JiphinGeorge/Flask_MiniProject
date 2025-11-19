import os
import re
import nltk

# Ensure NLTK knows where data is
nltk.data.path.append("/usr/local/share/nltk_data")
nltk.data.path.append(os.path.expanduser("~/.nltk_data"))

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load stopwords + lemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def preprocess_text(text: str) -> str:
    # Lowercase
    text = text.lower()

    # Remove punctuation
    text = re.sub(r'[^a-z0-9\s]', ' ', text)

    # Tokenize
    tokens = text.split()

    # Remove stopwords
    tokens = [w for w in tokens if w not in stop_words]

    # Lemmatize
    tokens = [lemmatizer.lemmatize(w) for w in tokens]

    return " ".join(tokens)
