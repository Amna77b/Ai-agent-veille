from datetime import date
from app.agent import build_agent

def run_veille(secteur: str = "tech"):
    agent = build_agent()

    consigne = (
        f"Récupère les derniers articles du secteur '{secteur}' avec l'outil "
        f"fetch_articles, puis rédige un rapport de veille structuré en français : "
        f"1) un résumé exécutif de 3 lignes des tendances du jour, "
        f"2) la liste des articles les plus pertinents avec un résumé d'une phrase chacun, "
        f"3) une section 'points d'attention' pour un consultant suivant ce secteur."
    )

    result = agent.invoke({"messages": [{"role": "user", "content": consigne}]})
    rapport = result["messages"][-1].content

    filename = f"reports/veille_{secteur}_{date.today()}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Rapport de veille — {secteur} — {date.today()}\n\n{rapport}")

    print(f"Rapport généré : {filename}")
    return rapport

import sys
from app.main import run_veille

if __name__ == "__main__":
    secteur = sys.argv[1] if len(sys.argv) > 1 else "tech"
    run_veille(secteur)