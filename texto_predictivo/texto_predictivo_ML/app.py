import streamlit as st
import joblib
import os
st.write_stream(os.path)
# Cargar modelo y vectorizador
#model = joblib.load("modelo_predictivo.pkl")
#vectorizer = joblib.load("vectorizador.pkl")

st.title("🧠 Completador de Texto Predictivo (ML)")

entrada = st.text_input("Escribe el inicio de una palabra (ej: 'pa'):")

if entrada:
    # Generar features desde la entrada
    entrada_vect = vectorizer.transform([entrada])

    # Predecir probabilidades de todas las clases
    proba = model.predict_proba(entrada_vect)[0]

    # Obtener top 5 palabras más probables
    top_indices = proba.argsort()[-5:][::-1]
    top_palabras = [model.classes_[i] for i in top_indices]

    st.subheader("🔮 Sugerencias:")
    for palabra in top_palabras:
        st.write(f"- {palabra}")
