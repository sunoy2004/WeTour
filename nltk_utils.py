import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from fuzzywuzzy import fuzz, process
import string

# Download required NLTK data (uncomment if needed)
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')

# Initialize stemmer and lemmatizer
stemmer = nltk.PorterStemmer()
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def tokenize(sentence):
    """
    Enhanced tokenization with preprocessing
    """
    # Convert to lowercase
    sentence = sentence.lower()
    
    # Remove punctuation
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize
    tokens = word_tokenize(sentence)
    
    # Remove stopwords
    tokens = [token for token in tokens if token not in stop_words]
    
    return tokens


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


def stem(word):
    """
    Enhanced stemming with lemmatization
    """
    # First lemmatize, then stem
    lemma = lemmatizer.lemmatize(word.lower(), get_wordnet_pos(word))
    return stemmer.stem(lemma)


def bag_of_words(tokenized_sentence, words):
    """
    Enhanced bag of words with fuzzy matching
    """
    # Stem each word
    sentence_words = [stem(word) for word in tokenized_sentence]
    
    # Initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    
    for idx, w in enumerate(words):
        # Exact match
        if w in sentence_words:
            bag[idx] = 1
        else:
            # Fuzzy matching for similar words
            match = process.extractOne(w, sentence_words, scorer=fuzz.token_sort_ratio)
            if match and match[1] > 80:  # 80% similarity threshold
                bag[idx] = match[1] / 100.0  # Use similarity score as weight
    
    return bag


def expand_synonyms(sentence):
    """
    Expand sentence with synonyms to improve matching
    """
    # This is a simplified implementation
    # In a production system, you might use WordNet or a more comprehensive synonym database
    synonyms = {
        'hello': ['hi', 'hey', 'greetings'],
        'bye': ['goodbye', 'farewell', 'see you'],
        'help': ['assist', 'support', 'aid'],
        'package': ['tour', 'trip', 'vacation', 'holiday'],
        'destination': ['place', 'location', 'spot'],
        'weather': ['climate', 'conditions'],
        'hotel': ['accommodation', 'lodging', 'stay'],
        'flight': ['airplane', 'plane', 'airline'],
        'train': ['railway', 'rail']
    }
    
    expanded_words = []
    for word in sentence.split():
        expanded_words.append(word)
        if word.lower() in synonyms:
            expanded_words.extend(synonyms[word.lower()])
    
    return ' '.join(expanded_words)
