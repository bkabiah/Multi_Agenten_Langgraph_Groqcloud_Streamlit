import os
from typing import TypedDict, Literal
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langchain_tavily import TavilySearch
from supabase import create_client, Client
from pydantic import BaseModel

# Lade Umgebungsvariablen sicherheitshalber auch hier
load_dotenv()

# --- Init Clients ---
# AKTUELLES, STABILES GROQ MODELL
#llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0, api_key=os.getenv("GROQ_API_KEY"))

# Ändere diese Zeile zu:
llm = ChatGroq(model="qwen/qwen3.8-27b", temperature=0, api_key=os.getenv("GROQ_API_KEY"))

search_tool = TavilySearch(max_results=3)
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# --- State Definition ---
class AgentState(TypedDict):
    user_input: str
    route: str
    response: str
    data: dict

# --- Pydantic Models für den Router ---
class RouteIntent(BaseModel):
    intent: Literal["research", "recommendation", "support", "inventory"]

# --- Agent Nodes ---

def research_agent(state: AgentState):
    prompt = f"""Du bist ein E-Commerce Produkt-Researcher. Suche nach den neuesten Trends für Barfußschuhe im Jahr 2026. 
    Fokus: Neue Materialien, Wettbewerber, Preisvergleiche. 
    Nutzeranfrage: {state['user_input']}"""
    
    search_results = search_tool.invoke(f"Barfußschuhe Trends 2026 Neuheiten Preise {state['user_input']}")
    
    response = llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content=f"Nutze diese Daten für deine Analyse: {search_results}")
    ])
    return {"response": response.content, "route": "research"}

def recommendation_agent(state: AgentState):
    db_products = supabase.table("products").select("*").execute().data
    
    prompt = f"""Du bist ein Barfußschuh-Experte. Analysiere die Kundenanforderung und empfehle exakt EINEN Schuh aus der Datenbank.
    Kundenanfrage: {state['user_input']}
    Verfügbare Produkte: {db_products}
    Antworte strukturiert."""
    
    # Hinweis: Für diesen Test nutzen wir einen einfachen Prompt, da with_structured_output manchmal bei bestimmten Modellen zickt.
    # In einer echten App würde man hier llm.with_structured_output() nutzen.
    response = llm.invoke([SystemMessage(content=prompt), HumanMessage(content=state['user_input'])])
    return {"response": response.content, "data": {"mock_recommendation": "ZenWalk Ultra"}, "route": "recommendation"}

def support_agent(state: AgentState):
    prompt = f"""Du bist der freundliche Customer Support für einen Barfußschuh-Shop in Deutschland.
    Beantworte folgende Frage zu Lieferung (DHL, 2-4 Tage), Retouren (30 Tage kostenlos) oder Produkten.
    Frage: {state['user_input']}"""
    
    response = llm.invoke([SystemMessage(content=prompt), HumanMessage(content=state['user_input'])])
    return {"response": response.content, "route": "support"}

def inventory_agent(state: AgentState):
    db_products = supabase.table("products").select("name, stock_quantity").execute().data
    
    alerts = []
    for p in db_products:
        level = "OK"
        if p["stock_quantity"] < 10: level = "CRITICAL"
        elif p["stock_quantity"] < 30: level = "LOW"
        alerts.append({"product_name": p["name"], "current_stock": p["stock_quantity"], "alert_level": level})
        
    return {"response": f"Inventar-Status: {alerts}", "data": alerts, "route": "inventory"}

# --- Router ---
def route_request(state: AgentState) -> Literal["research", "recommendation", "support", "inventory"]:
    prompt = f"Klassifiziere die Anfrage: '{state['user_input']}' in eines dieser Ziele: research (Trends/Web), recommendation (Kaufberatung), support (Versand/Retoure), inventory (Lagerbestand). Antworte NUR mit dem einen Wort."
    
    # Wir nutzen hier einen einfachen Aufruf, um Modell-Inkompatibilitäten mit structured_output zu umgehen
    response = llm.invoke([SystemMessage(content=prompt), HumanMessage(content=state['user_input'])])
    
    # Einfaches Parsing der Antwort
    intent = response.content.strip().lower()
    if "research" in intent: return "research"
    if "recommendation" in intent or "beratung" in intent: return "recommendation"
    if "support" in intent or "versand" in intent or "retoure" in intent: return "support"
    if "inventory" in intent or "lager" in intent: return "inventory"
    
    return "recommendation" # Fallback

# --- Graph Build ---
def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("research", research_agent)
    workflow.add_node("recommendation", recommendation_agent)
    workflow.add_node("support", support_agent)
    workflow.add_node("inventory", inventory_agent)
    
    workflow.set_conditional_entry_point(
        route_request,
        {
            "research": "research",
            "recommendation": "recommendation",
            "support": "support",
            "inventory": "inventory",
        }
    )
    
    workflow.add_edge("research", END)
    workflow.add_edge("recommendation", END)
    workflow.add_edge("support", END)
    workflow.add_edge("inventory", END)
    
    return workflow.compile()

app = build_graph()
