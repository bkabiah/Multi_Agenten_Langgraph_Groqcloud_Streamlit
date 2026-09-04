# 🦶 Barfußschuh AI Agents (E-Commerce 2026)

Ein produktionsreifes Multi-Agenten-System für den E-Commerce, entwickelt für den deutschen Markt. Dieses Projekt demonstriert die Orchestrierung spezialisierter KI-Agenten zur Automatisierung von Research, Sales, Support und Supply-Chain-Management.

## 🏗 Architektur & Tech Stack

- **Orchestrierung:** [LangGraph](https://langchain-ai.github.io/langgraph/) (Stateful Multi-Agent Routing)
- **LLM Provider:** [Groq Cloud](https://groq.com/) (Llama 3.3 70B für extrem niedrige Latenz)
- **Datenvalidierung:** Pydantic V2 (Strikte Typisierung für Enterprise-Integration)
- **Datenbank & Vektor-Store:** Supabase (PostgreSQL)
- **Observability:** LangSmith (Tracing & Debugging)
- **Evaluation:** DeepEval (LLM-as-a-Judge Testing)
- **Web Search:** Tavily API (Live-Recherche)
- **UI:** Streamlit

## 🤖 Die Agenten

1. **Research Agent:** Durchsucht das Live-Web nach Trends, Wettbewerbern und Preisen für Barfußschuhe (Fokus 2026).
2. **Recommendation Agent:** Analysiert Kundenanforderungen via Pydantic-Struktur und matcht sie mit dem Supabase-Inventory.
3. **Support Agent:** Beantwortet FAQs zu Versand (DHL), Retouren und Produkteigenschaften.
4. **Inventory Agent:** Überwacht den Lagerbestand und generiert Out-of-Stock-Alerts.

## 🚀 Setup & Installation

```bash
# Repository klonen
git clone <repo-url>
cd barefoot-ai-agents

# Environment setzen
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# .env Datei konfigurieren (siehe .env.example)
cp .env.example .env

# Streamlit UI starten
streamlit run src/ui/app.py
