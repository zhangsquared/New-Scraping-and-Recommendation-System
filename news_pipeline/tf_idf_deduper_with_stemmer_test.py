import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()
translator = str.maketrans('','',string.punctuation)

def stem_tokens(tokens, stemmer):
  stemmed = []
  for item in tokens:
    stemmed.append(stemmer.stem(item))
  return stemmed

def tokenize(text):
  tokens = nltk.word_tokenize(text)
  stems = stem_tokens(tokens, stemmer)
  return stems

def process_document(documents):
  """case-insensitive, remove puctuation"""
  rtn = []
  for doc in documents:
    no_punctuation = doc.lower().translate(translator)
    rtn.append(no_punctuation)
  return rtn

doc0 = "I like apple. I like orange too"
doc1 = "I like apples. I like oranges"
doc2 = "I love apple. I hate doctors"
doc3 = "An apple a day keeps the doctor away"
doc4 = "Never compare an apple to an orange"


######### without stemmer ##########
documents = [doc1, doc2, doc3, doc4]

tfidf = TfidfVectorizer().fit_transform(documents)
pairwise_sim = tfidf * tfidf.T

print(pairwise_sim.A)


######### with stemmer ##########
documents = [doc0, doc1, doc2, doc3, doc4]
print(documents)
processed_document = process_document(documents)
print(processed_document)

tfidf = TfidfVectorizer(tokenizer = tokenize)
tfs = tfidf.fit_transform(processed_document)
pairwise_sim = tfs * tfs.T

print(pairwise_sim.A)
