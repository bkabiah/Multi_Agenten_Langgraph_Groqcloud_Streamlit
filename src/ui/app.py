import streamlit as st
import sys
import os

# Pfad für Imports anpassen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.agents.graph import app

st.set_page_config(page_title="Barfußschuh AI Agents | E-Commerce 2026", layout="wide")
st.title("🦶 Barfußschuh AI Command Center")
st.caption("Powered by LangGraph, Groq & Supabase")

tab1, tab2, tab3, tab4 = st.tabs(["🌐 Research", "🎯 Recommendation", "💬 Support", "📦 Inventory"])

with tab1:
    st.header("Markt- & Trend Research 2026")
    q1 = st.text_input("Was möchtest du recherchieren?", "Welche neuen Materialien für Barfußschuhe gibt es 2026?")
    if st.button("Recherche starten", key="b1"):
        with st.spinner("Durchsuche das Web..."):
            res = app.invoke({"user_input": q1})
            st.markdown(res["response"])

with tab2:
    st.header("KI-Kaufberatung")
    q2 = st.text_input("Was sind deine Anforderungen?", "Ich bin Läufer, suche etwas für breite Füße, Budget 150€.")
    if st.button("Empfehlung generieren", key="b2"):
        with st.spinner("Analysiere Anforderungen..."):
            res = app.invoke({"user_input": q2})
            st.success(res["response"])
            if res.get("data"):
                st.json(res["data"])

with tab3:
    st.header("Customer Support")
    q3 = st.text_input("Wie können wir helfen?", "Wie lange dauert der Versand nach München?")
    if st.button("Antwort erhalten", key="b3"):
        res = app.invoke({"user_input": q3})
        st.info(res["response"])

with tab4:
    st.header("Inventory & Supply Chain")
    if st.button("Bestände prüfen", key="b4"):
        res = app.invoke({"user_input": "Prüfe den Lagerbestand"})
        st.dataframe(res["data"])
