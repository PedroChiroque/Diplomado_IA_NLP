import streamlit as st
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


# Descargar recursos necesarios si no existen
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# **********************
import os
import sys

# Obtener el path absoluto del script actual
try:
    ruta_script = os.path.abspath(__file__)
except NameError:
    # __file__ puede no estar definido en ejecución interactiva (ej: Streamlit Cloud)
    ruta_script = os.path.abspath(sys.argv[0])


# **********************

# Function for text preprocessing
def preprocess_text(text):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove punctuation
    text = text.lower()  # Convert to lowercase
    text = text.split()  # Split into words
    ps = PorterStemmer()
    text = [ps.stem(word) for word in text if not word in set(stopwords.words('english'))]  # Remove stopwords and perform stemming
    text = ' '.join(text)
    return text

# View the path
st.write("Autor: Pedro Chiroque")
st.write("Version: 1.0")
#import os
#st.write("📂 Ruta actual:", os.getcwd())


# Load the vectorizer and models
# test use ./model/.....
# production use streamlit_sentiment/model/....


vectorizer = joblib.load('./streamlit_sentiment/model/tfidf_vectorizer.pkl')
svm_model = joblib.load('./streamlit_sentiment/model/svm_model.pkl')
nb_model = joblib.load('./streamlit_sentiment/model/naive_bayes_model.pkl')
lr_model = joblib.load('./streamlit_sentiment/model/logistic_regression_model.pkl')

# App title
st.title("Tweet Sentiment Analysis App")
st.write("Introduzca el texto que desea analizar para determinar el sentimiento:")

# User input text
input_text = st.text_area("Introduzca el texto aquí")

# Model selection
st.write("Selecciona el modelo para analizar el sentimiento:")
use_nb = st.checkbox('Naive Bayes')
use_svm = st.checkbox('SVM')
use_lr = st.checkbox('Logistic Regression')

if st.button("Analizar"):
    if not input_text:
        st.write("Por favor, introduzca el texto para su análisis.")
    elif not (use_nb or use_svm or use_lr):
        st.write("Seleccione al menos un modelo para analizar.")
    else:
        # Process the input text
        input_text_processed = preprocess_text(input_text)
        input_text_vect = vectorizer.transform([input_text_processed])

        st.write(f"**Ingrese el texto:** {input_text}")
        
        # Prediction using Naive Bayes
        if use_nb:
            nb_prediction = nb_model.predict(input_text_vect)[0]
            nb_prob = nb_model.predict_proba(input_text_vect)[0]
            st.write(f"**Naive Bayes Prediction:** {'Positive' if nb_prediction == 1 else 'Negative'} (Confidence: {nb_prob[nb_prediction]:.2f})")

        # Prediction using SVM
        if use_svm:
            svm_prediction = svm_model.predict(input_text_vect)[0]
            st.write(f"**SVM Prediction:** {'Positive' if svm_prediction == 1 else 'Negative'}")

        # Prediction using Logistic Regression
        if use_lr:
            lr_prediction = lr_model.predict(input_text_vect)[0]
            lr_prob = lr_model.predict_proba(input_text_vect)[0]
            st.write(f"**Logistic Regression Prediction:** {'Positive' if lr_prediction == 1 else 'Negative'} (Confidence: {lr_prob[lr_prediction]:.2f})")


