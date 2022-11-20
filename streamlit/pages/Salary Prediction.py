import streamlit as st
import numpy as np
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, f1_score, roc_auc_score
from sklearn.feature_extraction.text import TfidfVectorizer

import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from sklearn.naive_bayes import MultinomialNB
from PIL import Image

ctp_logo = Image.open("images/ctp icon.png")
st.set_page_config(
    page_icon=ctp_logo,
    layout="wide"
)

df=pd.read_csv('data/DS_DA_BS.csv')

#Clean salary column: we only want yearly salaries
for ind in df.index:
    if re.search("Hour|-1",df['Salary Estimate'][ind]):
        df.drop([ind],inplace=True)

#Clean null value
df.replace(['-1'], [np.nan], inplace=True)
df.replace(['-1.0'], [np.nan], inplace=True)
df.replace([-1], [np.nan], inplace=True)

# Lowercase all words
def make_lower(a_string):
    return a_string.lower()
# Remove all punctuation
def remove_punctuation(a_string):
    a_string = re.sub(r'[^\w\s]','',a_string)
    return a_string
def remove_stopwords(a_string):
    # Break the sentence down into a list of words
    words = word_tokenize(a_string)
    # Make a list to append valid words into
    valid_words = []

    # Loop through all the words
    for word in words:
        # Check if word is not in stopwords
        if word not in stopwords:
            # If word not in stopwords, append to our valid_words
            valid_words.append(word)

    # Join the list of words together into a string
    a_string = ' '.join(valid_words)
    return a_string

def text_pipeline(input_string):
    input_string = make_lower(input_string)
    input_string = remove_punctuation(input_string)
    return input_string

df['Job Description']=df['Job Description'].apply(text_pipeline)
x=df['Job Description'].values
y=df['role'].values

X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42)
# Save the raw text for later just incase
X_train_text = X_train
X_test_text = X_test

# Initialize our vectorizer
vectorizer = TfidfVectorizer()
# This makes your vocab matrix
vectorizer.fit(X_train)
# This transforms your documents into vectors.
X_train = vectorizer.transform(X_train)
X_test = vectorizer.transform(X_test)

model = MultinomialNB(alpha=.05)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)

new_text= st.text_area('Enter the Job Description:', 'analyzes large data sets to identify effective ways of boosting organizational efficiency')
st.write('Entered job description:', new_text)

new_text = text_pipeline(new_text)
new_text_vectorized = vectorizer.transform([new_text])
model.predict(new_text_vectorized)
# Print the predicted probabilies for each class
pp = model.predict_proba(new_text_vectorized)
    # Print probabilities for that predicition
for class_name, percentage in zip(model.classes_, pp.round(3)[0]):
    st.write(class_name,":",percentage )