import os
import re
import nltk

# Force NLTK to use local project nltk_data folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NLTK_PATH = os.path.join(os.path.dirname(BASE_DIR), "nltk_data")

if NLTK_PATH not in nltk.data.path:
    nltk.data.path.append(NLTK_PATH)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load resources safely
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def preprocess_text(text: str) -> str:
    """Clean + tokenize + remove stopwords + lemmatize."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)

    tokens = text.split()
    tokens = [w for w in tokens if w not in stop_words]
    tokens = [lemmatizer.lemmatize(w) for w in tokens]

    return " ".join(tokens)
