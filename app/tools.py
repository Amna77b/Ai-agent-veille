import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import feedparser
from langchain_core.tools import tool

from app.memory import load_seen, save_seen

FEEDS = {
    "tech": "https://www.lemondeinformatique.fr/flux-rss/thematique/intelligence-artificielle/rss.xml",
    "finance": "https://www.lesechos.fr/rss/rss_finance-marches.xml",
    "energie": "https://www.actu-environnement.com/rss/energie.xml",
    "general": "https://www.lemonde.fr/rss/une.xml",
}


@tool
def fetch_articles(secteur: str, max_articles: int = 8) -> str:
    """Récupère les derniers articles non déjà traités pour un secteur donné
    (tech, finance, energie, ou general). Retourne une liste formatée
    titre + résumé + lien."""
    url = FEEDS.get(secteur.lower(), FEEDS["general"])
    feed = feedparser.parse(url)
    seen = load_seen()

    articles = []
    nouveaux_liens = []
    for entry in feed.entries:
        lien = entry.get("link", "")
        if lien in seen:
            continue

        titre = entry.get("title", "Sans titre")
        resume = entry.get("summary", "")[:300]
        articles.append(f"- {titre}\n  {resume}\n  Source : {lien}")
        nouveaux_liens.append(lien)

        if len(articles) >= max_articles:
            break

    seen.update(nouveaux_liens)
    save_seen(seen)

    return "\n\n".join(articles) if articles else "Aucun nouvel article depuis la dernière veille."


@tool
def fetch_articles_multi(secteurs: str, max_articles_par_secteur: int = 5) -> str:
    """Récupère les articles récents et non déjà traités pour plusieurs
    secteurs séparés par des virgules (ex: 'tech,finance,energie'),
    regroupés par secteur."""
    seen = load_seen()
    resultat = []
    nouveaux_liens = []

    for secteur in [s.strip() for s in secteurs.split(",")]:
        url = FEEDS.get(secteur.lower(), FEEDS["general"])
        feed = feedparser.parse(url)

        bloc = [f"## Secteur : {secteur.upper()}"]
        count = 0
        for entry in feed.entries:
            lien = entry.get("link", "")
            if lien in seen or count >= max_articles_par_secteur:
                continue
            titre = entry.get("title", "Sans titre")
            resume = entry.get("summary", "")[:300]
            bloc.append(f"- {titre}\n  {resume}\n  Source : {lien}")
            nouveaux_liens.append(lien)
            count += 1

        resultat.append("\n".join(bloc))

    seen.update(nouveaux_liens)
    save_seen(seen)
    return "\n\n".join(resultat)


@tool
def send_email_report(sujet: str, contenu: str) -> str:
    """Envoie le rapport de veille par email au destinataire configuré
    dans les variables d'environnement."""
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_APP_PASSWORD")
    destinataire = os.getenv("EMAIL_TO")

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = destinataire
    msg["Subject"] = sujet
    msg.attach(MIMEText(contenu, "plain", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, destinataire, msg.as_string())

    return f"Email envoyé à {destinataire}."