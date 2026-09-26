from fastapi import FastAPI
from pydantic import BaseModel
from app.main import run_veille, run_veille_multi

app = FastAPI(title="Agent de Veille IA")


class VeilleRequest(BaseModel):
    secteur: str = "tech"
    envoyer_email: bool = False


class VeilleMultiRequest(BaseModel):
    secteurs: str = "tech,finance,energie"
    envoyer_email: bool = False


@app.post("/veille")
def veille(req: VeilleRequest):
    rapport = run_veille(req.secteur, req.envoyer_email)
    return {"secteur": req.secteur, "rapport": rapport}


@app.post("/veille-multi")
def veille_multi(req: VeilleMultiRequest):
    rapport = run_veille_multi(req.secteurs, req.envoyer_email)
    return {"secteurs": req.secteurs, "rapport": rapport}


@app.get("/")
def health():
    return {"status": "ok"}
