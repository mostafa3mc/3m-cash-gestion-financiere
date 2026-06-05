from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import Agence, Produit, CategorieCharge, ConceptCharge

router = APIRouter(tags=["setup"])
AGENCES = ["AGDAL","TEMARA","DCHEIRA","INZEGANE1","INZEGANE2","ASSAKA","KAWAKIBI","AWREER","FARABI","OKBA","TIKIOUINE","MOKAWAMA"]
PRODUITS = ["CASH EXPRESS","WESTERN UNION","Portail TNS","TAP TAP Send","Wafacash","TRANSFAST","SendWave","WorldRemitZepz","RIA","MONEYGRAM","Remitly","JIBI","FAWATIR","WAFA ASSURANCE","Compte Support","SWISSREMIT","I- Transfer","CashMinute","Monty","HSSAB BIKHIR","PAY CASH","Floussy recharge","Floussy Vente"]
CONCEPTS = {"Locaux":["Loyer"], "Services":["Internet","Eau","Electricité","Femme de Ménage","Produits de Ménage","Gardien"], "Personnel":["Masse salariale","CNSS"], "Transport":["Taxi","Déplacements"], "Fournitures":["Papier A4","Toner","Produits bureautiques"], "Fiscalité":["Taxes"]}

def get_or_create(db, model, **kwargs):
    obj = db.query(model).filter_by(**kwargs).first()
    if obj: return obj
    obj = model(**kwargs); db.add(obj); db.flush(); return obj

@router.post("/init")
def init_data(db: Session = Depends(get_db)):
    for nom in AGENCES: get_or_create(db, Agence, nom=nom)
    for nom in PRODUITS: get_or_create(db, Produit, nom=nom)
    for cat, concepts in CONCEPTS.items():
        c = get_or_create(db, CategorieCharge, nom=cat)
        for nom in concepts:
            if not db.query(ConceptCharge).filter_by(categorie_id=c.id, nom=nom).first():
                db.add(ConceptCharge(categorie_id=c.id, nom=nom))
    db.commit()
    return {"message":"Données initiales créées"}

@router.get("/referentiels")
def referentiels(db: Session = Depends(get_db)):
    return {
        "agences": db.query(Agence).order_by(Agence.nom).all(),
        "produits": db.query(Produit).order_by(Produit.nom).all(),
        "categories": db.query(CategorieCharge).order_by(CategorieCharge.nom).all(),
        "concepts": db.query(ConceptCharge).order_by(ConceptCharge.nom).all(),
    }
