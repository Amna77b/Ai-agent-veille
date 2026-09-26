import sys
from datetime import date
from app.agent import build_agent


def _save_report(secteur_label: str, rapport: str) -> str:
    filename = f"reports/veille_{secteur_label}_{date.today()}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Rapport de veille — {secteur_label} — {date.today()}\n\n{rapport}")
    print(f"Rapport généré : {filename}")
    return filename


def run_veille(secteur: str = "tech", envoyer_email: bool = False) -> str:
    agent = build_agent()

    consigne = (
        f"Récupère les nouveaux articles du secteur '{secteur}' avec l'outil "
        f"fetch_articles, puis rédige un rapport de veille structuré en français : "
        f"1) un résumé exécutif de 3 lignes des tendances du jour, "
        f"2) la liste des articles les plus pertinents avec un résumé d'une phrase chacun, "
        f"3) une section 'points d'attention' pour un consultant suivant ce secteur."
    )
    if envoyer_email:
        consigne += (
            " Une fois le rapport rédigé, envoie-le par email avec send_email_report "
            f"en utilisant comme sujet 'Veille {secteur} - {date.today()}'."
        )

    result = agent.invoke({"messages": [{"role": "user", "content": consigne}]})
    rapport = result["messages"][-1].content
    _save_report(secteur, rapport)
    return rapport


def run_veille_multi(secteurs: str = "tech,finance,energie", envoyer_email: bool = False) -> str:
    agent = build_agent()

    consigne = (
        f"Utilise fetch_articles_multi avec secteurs='{secteurs}' pour récupérer "
        f"les nouveaux articles de chaque secteur. Rédige un rapport COMPARATIF "
        f"structuré en français : 1) tendances communes entre secteurs, "
        f"2) spécificités par secteur, 3) implications pour un consultant "
        f"suivant ces marchés."
    )
    if envoyer_email:
        consigne += (
            " Une fois le rapport rédigé, envoie-le par email avec send_email_report "
            f"en utilisant comme sujet 'Veille multi-secteurs - {date.today()}'."
        )

    result = agent.invoke({"messages": [{"role": "user", "content": consigne}]})
    rapport = result["messages"][-1].content
    _save_report("multi", rapport)
    return rapport


if __name__ == "__main__":
    secteur = sys.argv[1] if len(sys.argv) > 1 else "tech"
    run_veille(secteur)