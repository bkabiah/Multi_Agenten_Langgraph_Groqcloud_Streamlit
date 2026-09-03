import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialisiere den Client mit deinem Key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("🔍 Verfügbare Modelle für deinen Groq API-Key:\n")
models = client.models.list().data

# Filtere nur die relevanten LLMs heraus, damit die Liste übersichtlich bleibt
allowed_models = [m.id for m in models if "llama" in m.id or "gemma" in m.id or "mixtral" in m.id or "qwen" in m.id]

for model in sorted(allowed_models):
    print(f"✅ {model}")

if not allowed_models:
    print("❌ Keine Modelle gefunden. Bitte prüfe deinen GROQ_API_KEY in der .env Datei.")
