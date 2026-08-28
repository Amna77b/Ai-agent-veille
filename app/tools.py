import feedparser
from langchain_core.tools import tool

# Quelques flux RSS publics par secteur — adapte selon ton besoin
FEEDS = {
    "tech": "https://www.lemondeinformatique.fr/flux-rss/thematique/intelligence-artificielle/rss.xml",
    "finance": "https://www.lesechos.fr/rss/rss_finance-marches.xml",
    "general": "https://www.lemonde.fr/rss/une.xml",
}

@tool
def fetch_articles(secteur: str, max_articles: int = 8) -> str:
    """Récupère les derniers articles d'actualité pour un secteur donné
    (tech, finance, ou general). Retourne une liste formatée titre + résumé + lien."""
    url = FEEDS.get(secteur.lower(), FEEDS["general"])
    feed = feedparser.parse(url)

    articles = []
    for entry in feed.entries[:max_articles]:
        titre = entry.get("title", "Sans titre")
        resume = entry.get("summary", "")[:300]
        lien = entry.get("link", "")
        articles.append(f"- {titre}\n  {resume}\n  Source : {lien}")

    return "\n\n".join(articles) if articles else "Aucun article trouvé."