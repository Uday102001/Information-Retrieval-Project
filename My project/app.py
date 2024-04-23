import os
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify, render_template
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from scipy import spatial
import nltk

app = Flask(__name__)

nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Load crawled documents
documents = []
for filename in os.listdir("crawled_pages"):
    if filename.endswith(".html"):
        with open(os.path.join("crawled_pages", filename), "r", encoding="utf-8") as file:
            documents.append(file.read())

# Indexing
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(documents)
document_index = {idx: filename for idx, filename in enumerate(os.listdir("crawled_pages"))}

# Optional: Query spelling correction/suggestion using NLTK
def suggest_spelling_correction(query):
    corrected_query = []
    for word in word_tokenize(query):
        suggestions = wordnet.synsets(word)
        if not suggestions:
            corrected_word = max(wordnet.synsets(word.lower()), key=lambda x: x.path_similarity(wordnet.synsets(word.lower())[0]))
            corrected_query.append(corrected_word)
        else:
            corrected_query.append(word)
    return " ".join(corrected_query)

# Optional: Query expansion using WordNet
def expand_query(query):
    expanded_query = []
    for word in word_tokenize(query):
        expanded_query.append(word)
        synonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
        expanded_query.extend(synonyms)
    return " ".join(expanded_query)

# Preprocessing
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    preprocessed_text = []
    for word, tag in pos_tags:
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_word = lemmatizer.lemmatize(word, pos)
        if lemmatized_word.lower() not in stop_words:
            preprocessed_text.append(lemmatized_word.lower())
    return ' '.join(preprocessed_text)

# Process queries
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        
        # Optional: Query spelling correction/suggestion
        corrected_query = suggest_spelling_correction(query)
        
        # Optional: Query expansion
        expanded_query = expand_query(corrected_query)
        
        # Preprocess query
        preprocessed_query = preprocess_text(expanded_query)
        
        # Transform query to TF-IDF representation
        query_vector = vectorizer.transform([preprocessed_query])
        
        # Calculate cosine similarity between query and documents
        similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
        
        # Get top K ranked results
        top_k_results_indices = np.argsort(similarity_scores)[-5:][::-1]  # Get top 5 results
        top_k_results = [(document_index[idx], similarity_scores[idx]) for idx in top_k_results_indices]
        
        return render_template('index.html', results=top_k_results, query=query)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
