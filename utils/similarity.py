from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarities(input_text, doc_texts, doc_names, top_k=3):
    corpus = [input_text] + doc_texts
    vectorizer = TfidfVectorizer()

    try:
        tfidf = vectorizer.fit_transform(corpus)
    except ValueError:
        return [], []

    sims = cosine_similarity(tfidf[0], tfidf[1:])[0]

    similarities = []
    for i, score in enumerate(sims):
        similarities.append({
            'doc': doc_names[i],
            'score': float(score)
        })

    similarities_sorted = sorted(similarities, key=lambda x: x['score'], reverse=True)

    top_matches = []
    for item in similarities_sorted[:top_k]:
        idx = doc_names.index(item['doc'])
        top_matches.append({
            'index': idx,
            'score': item['score']
        })

    return similarities_sorted, top_matches

def highlight_matches(input_raw, doc_raw):
    input_words = set([w.lower() for w in input_raw.split() if len(w) > 2])
    doc_words = doc_raw.split()

    out = []
    for w in doc_words:
        clean = ''.join(c for c in w if c.isalnum()).lower()
        if clean in input_words:
            out.append(f"<mark>{w}</mark>")
        else:
            out.append(w)
    return " ".join(out)
