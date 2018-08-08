import logging
import news_cnn_model
import numpy as np
import os
import pandas as pd
import pickle
import shutil
import tensorflow as tf

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from os.path import join
from os.path import normpath
from sklearn import metrics

# logging
LOGGER_FORMAT = '%(asctime)s - %(message)s'
logging.basicConfig(format=LOGGER_FORMAT)
LOGGER = logging.getLogger('news_class_trainer')
LOGGER.setLevel(logging.DEBUG)

learn = tf.contrib.learn
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

REMOVE_PREVIOUS_MODEL = True

MODEL_OUTPUT_DIR = normpath(join(os.path.dirname(__file__), '../model/'))
DATA_SET_FILE = normpath(join(os.path.dirname(__file__), '../data/labeled_news.csv'))
VARS_FILE = normpath(join(os.path.dirname(__file__), '../model/vars'))
VOCAB_PROCESSOR_SAVE_FILE = normpath(join(os.path.dirname(__file__), '../model/vocab_procesor_save_file'))

MAX_DOCUMENT_LENGTH = 200
N_CLASSES = 8
TRAINING_DATA_SIZE = 400
# training parms, for this model, batch = all the data set
# for the same training data, we repeat STEPS times
STEPS = 200

def main(unused_argv):
  if REMOVE_PREVIOUS_MODEL:
    #remove old model
    shutil.rmtree(MODEL_OUTPUT_DIR)
    os.mkdir(MODEL_OUTPUT_DIR)
  
  #prepare trainning and testing data
  df = pd.read_csv(DATA_SET_FILE, header=None)
  # # random shuffle
  df.sample(frac=1)
  train_df = df[0:TRAINING_DATA_SIZE]
  test_df = df.drop(train_df.index)

  # 2 - news description, 0 - class
  x_train = train_df[2]
  x_test = test_df[2]
  y_train = train_df[0]
  y_test = test_df[0]

  # tokenize sentences
  x_train = [word_tokenize(s) for s in x_train.tolist()]
  x_test = [word_tokenize(s) for s in x_test.tolist()]

  # stemming words
  x_train = stemWords(x_train)
  x_test = stemWords(x_test)

  # process vocabulary
  vocab_processor = learn.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
  x_train = np.array(list(vocab_processor.fit_transform(x_train)))
  x_test = np.array(list(vocab_processor.transform(x_test)))

  n_words = len(vocab_processor.vocabulary_)
  LOGGER.debug('Total words: %d', n_words)

  # saving n_words and vocab_processor:
  # we need to use the same vocabulary processor
  # each word the same index
  # we also need to save n_words itself for news_cnn_model
  with open(VARS_FILE, 'wb') as f: # needs to be opened in binary mode
    pickle.dump(n_words, f)
  vocab_processor.save(VOCAB_PROCESSOR_SAVE_FILE)

  # build model
  classifier = learn.Estimator(
    model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words),
    model_dir=MODEL_OUTPUT_DIR
  )

  # train and predict
  classifier.fit(x_train, y_train, steps=STEPS)

  # evaluate model
  y_predicted = [
    p['class'] for p in classifier.predict(x_test, as_iterable=True)
  ]

  score = metrics.accuracy_score(y_test, y_predicted)
  LOGGER.info('Accuracy: {0:f}'.format(score))

def stemWords(sentences):
  norm_sentences = []
  for sentence in sentences:
    tokens = sentence
    stemmed_tokens = [stemmer.stem(t.lower()) for t in tokens if not t in stop_words]
    norm_sentence = ' '.join(stemmed_tokens)
    norm_sentences.append(norm_sentence)
  return norm_sentences


if __name__ == '__main__':
  tf.app.run(main=main)
