import sys
import os

# Fügt das Projekt-Root-Verzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.agents.graph import app
from dotenv import load_dotenv

# Lädt die .env Datei
load_dotenv()

def test_recommendation_agent_functional():
    """
    Testet die End-to-End Funktionalität des Recommendation Agents.
    Prüft, ob der Graph korrekt routet, die DB abfragt und eine sinnvolle Antwort generiert.
    """
    # 1. Simuliere User Input
    state = {"user_input": "Ich suche einen günstigen Barfußschuh für Frauen für den Alltag, unter 120 Euro."}
    
    # 2. Der LangGraph wird aufgerufen
    result = app.invoke(state)
    
    # 3. Assertions (Prüfungen)
    # Prüfen, ob der Graph überhaupt eine Antwort zurückgegeben hat
    assert "response" in result, "Der Graph hat kein 'response' Feld zurückgegeben."
    assert result["response"] is not None, "Die Antwort ist leer."
    assert len(result["response"]) > 30, "Die Antwort ist zu kurz, um eine Empfehlung zu sein."
    
    # 4. Inhaltliche Prüfung (Keyword-Check für Determinismus)
    response_lower = result["response"].lower()
    
    # Der Agent sollte "Frauen" oder "Damen" erkennen und erwähnen
    assert "frau" in response_lower or "damen" in response_lower, \
        f"Die Empfehlung passt nicht zur Zielgruppe. Antwort: {result['response']}"
    
    # Der Agent sollte einen Schuh aus der DB empfehlen (z.B. ZenWalk)
    assert "zenwalk" in response_lower or "barfuß" in response_lower, \
        f"Es wurde kein passender Barfußschuh empfohlen. Antwort: {result['response']}"
    
    # Erfolgreicher Abschluss
    print(f"\n✅ Agentenantwort war erfolgreich und valide: \n{result['response']}")


def test_support_agent_functional():
    """Testet den Support Agenten (Versand/Retoure)."""
    state = {"user_input": "Wie lange dauert der Versand nach Berlin und ist die Retoure kostenlos?"}
    result = app.invoke(state)
    
    assert "response" in result
    response_lower = result["response"].lower()
    
    # Der Support Agent sollte DHL/Versandzeit und kostenlose Retoure erwähnen
    assert "dhl" in response_lower or "tag" in response_lower, "Versandinfo fehlt."
    assert "kostenlos" in response_lower or "30" in response_lower, "Retoureninfo fehlt."
    
    print(f"\n✅ Support-Agent Antwort war erfolgreich: \n{result['response']}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
