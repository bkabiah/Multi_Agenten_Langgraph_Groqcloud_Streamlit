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
## 🏗 Systemarchitektur

Dieses System folgt einem modularen, ereignisgesteuerten Multi-Agenten-Design. Der LangGraph-Router klassifiziert die Nutzeranfrage und leitet sie gezielt an den passenden Spezialisten weiter.

```mermaid
flowchart TD
    %% Styles für professionelle Optik
    classDef ui fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000
    classDef router fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef agent fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef external fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000
    classDef db fill:#ffebee,stroke:#b71c1c,stroke-width:2px,color:#000

    %% UI Layer
    UI[Streamlit UI Nutzer-Interface]:::ui

    %% Orchestration Layer
    Router[Intent Router Klassifiziert Anfrage]:::router
    
    subgraph Agents [Spezialisierte KI-Agenten]
        ResAgent[Research Agent Web Analyse]:::agent
        RecAgent[Recommendation Agent Produkt-Matching]:::agent
        SupAgent[Support Agent Versand und Retouren]:::agent
        InvAgent[Inventory Agent Lagerbestands-Check]:::agent
    end

    %% External Services Layer
    subgraph External [Externe Dienste und Daten]
        Groq[Groq Cloud Qwen Modelle]:::external
        Tavily[Tavily API Live Web Search]:::external
        Supabase[(Supabase PostgreSQL DB)]:::db
        LangSmith[LangSmith Observability]:::external
    end

    %% Verbindungen
    UI -->|1. Nutzeranfrage| Router
    Router -->|intent: research| ResAgent
    Router -->|intent: recommendation| RecAgent
    Router -->|intent: support| SupAgent
    Router -->|intent: inventory| InvAgent

    ResAgent -->|2. Suchanfrage| Tavily
    ResAgent -->|3. LLM Inference| Groq
    RecAgent -->|3. LLM Inference| Groq
    SupAgent -->|3. LLM Inference| Groq
    InvAgent -->|3. LLM Inference| Groq
    
    RecAgent -->|4. SQL Abfragen| Supabase
    InvAgent -->|4. SQL Abfragen| Supabase

    %% Observability
    Agents -.->|5. Automatisches Tracing| LangSmith

    %% Rückgabe an UI
    ResAgent -->|6. Strukturierte Antwort| UI
    RecAgent -->|6. Strukturierte Antwort| UI
    SupAgent -->|6. Strukturierte Antwort| UI
    InvAgent -->|6. Strukturierte Antwort| UI


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
