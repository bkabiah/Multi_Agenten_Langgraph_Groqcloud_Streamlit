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
    %% --- Styles für professionelle Optik ---
    classDef ui fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000,font-weight:bold
    classDef router fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000,font-weight:bold
    classDef agent fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef external fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000
    classDef db fill:#ffebee,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef test fill:#fff9c4,stroke:#f57f17,stroke-width:2px,color:#000

    %% --- UI Layer ---
    UI[🖥️ Streamlit UI<br/>Nutzer-Interface]:::ui

    %% --- Orchestration Layer ---
    subgraph Core ["⚙️ LangGraph Orchestrierung (Python)"]
        direction TB
        Router[🔀 Intent Router<br/>Klassifiziert Anfrage]:::router
        
        subgraph Agents ["🤖 Spezialisierte KI-Agenten"]
            direction LR
            ResAgent[🔍 Research Agent<br/>Web & Trend Analyse]:::agent
            RecAgent[🎯 Recommendation Agent<br/>Produkt-Matching]:::agent
            SupAgent[💬 Support Agent<br/>Versand & Retouren]:::agent
            InvAgent[📦 Inventory Agent<br/>Lagerbestands-Check]:::agent
        end
    end

    %% --- External Services Layer ---
    subgraph External ["☁️ Externe Dienste & Daten"]
        Groq[⚡ Groq Cloud<br/>Qwen / Llama Modelle]:::external
        Tavily[🌐 Tavily API<br/>Live Web Search]:::external
        Supabase[(🗄️ Supabase<br/>PostgreSQL DB)]:::db
        LangSmith[📊 LangSmith<br/>Observability & Tracing]:::external
    end

    %% --- Testing Layer ---
    subgraph Testing ["🧪 Qualitätssicherung"]
        Pytest[✅ Pytest + DeepEval<br/>Deterministische Tests]:::test
    end

    %% --- Verbindungen ---
    UI -->|1. Nutzeranfrage| Router
    Router -->|"intent: research"| ResAgent
    Router -->|"intent: recommendation"| RecAgent
    Router -->|"intent: support"| SupAgent
    Router -->|"intent: inventory"| InvAgent

    ResAgent -->|2. Suchanfrage| Tavily
    ResAgent & RecAgent & SupAgent & InvAgent -->|3. LLM Inference &<br/>Strukturierte Outputs| Groq
    RecAgent & InvAgent -->|4. SQL Abfragen| Supabase

    %% Observability
    Core -.->|5. Automatisches Tracing| LangSmith
    
    %% Testing
    Testing -.->|Validiert| Core

    %% Rückgabe
    ResAgent & RecAgent & SupAgent & InvAgent -->|6. Strukturierte Antwort| UI
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
