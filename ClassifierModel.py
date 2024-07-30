import pandas as pd
import numpy as np
from numpy import random
#import gensim
import nltk

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.linear_model import SGDClassifier
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import re
from bs4 import BeautifulSoup
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
import joblib
from imblearn.over_sampling import RandomOverSampler

def clean_text(text):
    """
        text: a string
        
        return: modified initial string
    """
    REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
    BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
    STOPWORDS = set(stopwords.words('english'))
    text = str(text)
    text = BeautifulSoup(text, "lxml").text # HTML decoding
    text = text.lower() # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # delete stopwords from text
    return text



df = pd.read_csv('/home/jfrans/Hackathon/Forensics/SEFACED_Email_Forensic_Dataset.csv')
df = df[pd.notnull(df['Class_Label'])]
#print(df.head(10))
#print(df['Text'].apply(lambda x: len(str(x).split(' '))).sum())

my_tags = ['Normal', 'Suspicious', 'Fraudulent', 'Harrasment']
nltk.download("stopwords")

df['Text'] = df['Text'].apply(clean_text)
df['Text'].apply(lambda x: len(str(x).split(' '))).sum()

#test-train split
X = df.Text
print(type(X))
X = X.values.reshape(-1, 1)
y = df.Class_Label
oversampler = RandomOverSampler(random_state=42)
X_resampled, y_resampled = oversampler.fit_resample(X, y)
X_resampled, y_resampled = pd.Series(X_resampled.ravel()), pd.Series(y_resampled.ravel())
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.3, random_state = 42)

#hinge was changed to perceptron
sgd = Pipeline([('vect', CountVectorizer()),
                ('tfidf', TfidfTransformer()),
                ('clf', SGDClassifier(loss='perceptron', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)),
               ])

sgd.fit(X_train, y_train)
sgd_save = "trained_model.joblib"
joblib.dump(sgd, sgd_save)
print("Model saved to: ", sgd_save)

y_pred = sgd.predict(X_test)
print('accuracy %s' % accuracy_score(y_pred, y_test))
print(classification_report(y_test, y_pred,target_names=my_tags))
