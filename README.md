# Agent IA Autonome — Veille Sectorielle

Agent IA qui surveille automatiquement l'actualité d'un secteur, sélectionne
et résume les articles pertinents, et génère un rapport de veille structuré
— sans intervention humaine à chaque étape.

## Stack
- LangGraph (orchestration de l'agent, pattern ReAct)
- Groq API (LLM Llama 3.1, gratuit, inférence très rapide)
- feedparser (lecture de flux RSS)

## Pourquoi un agent, pas un chatbot
Un chatbot répond à une question. Un agent reçoit un objectif et décide
lui-même des étapes et outils nécessaires pour l'atteindre, de façon
répétée et autonome (ici : aller chercher les articles, les filtrer,
les synthétiser).

## Lancer le projet
```bash
pip install -r requirements.txt
cp .env.example .env  
python -m app.main tech
```

## Automatisation
Le script peut être planifié (Tâches planifiées Windows / cron Linux)
pour générer un rapport quotidien automatiquement.