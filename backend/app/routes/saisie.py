from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import Agence, Produit, ConceptCharge, Revenu, Charge, ClotureMensuelle
from ..schemas import SaisieRevenus, SaisieCharges

router = APIRouter(tags=["saisie"])
TVA_FACTOR = Decimal("0.80")

def ensure_open(db, agence_id, annee, mois):
    c = db.query(ClotureMensuelle).filter_by(
        agence_id=agence_id,
        annee=annee,
        mois=mois,
        cloture=True
    ).first()
    if c:
        raise HTTPException(403, "Ce mois est clôturé")

@router.get("/agences")
def get_agences(db: Session = Depends(get_db)):
    return db.query(Agence).filter_by(actif=True).order_by(Agence.nom).all()

@router.get("/produits")
def get_produits(db: Session = Depends(get_db)):
    return db.query(Produit).filter_by(actif=True).order_by(Produit.nom).all()

@router.get("/concepts")
def get_concepts(db: Session = Depends(get_db)):
    return db.query(ConceptCharge).filter_by(actif=True).order_by(ConceptCharge.nom).all()

@router.post("/revenus")
def save_revenus(payload: SaisieRevenus, db: Session = Depends(get_db)):
    ensure_open(db, payload.agence_id, payload.annee, payload.mois)

    for ligne in payload.lignes:
        ht = ligne.montant_ttc * TVA_FACTOR
        obj = db.query(Revenu).filter_by(
            agence_id=payload.agence_id,
            produit_id=ligne.item_id,
            annee=payload.annee,
            mois=payload.mois
        ).first()

        if obj:
            obj.montant_ttc = ligne.montant_ttc
            obj.montant_ht = ht
        else:
            db.add(Revenu(
                agence_id=payload.agence_id,
                produit_id=ligne.item_id,
                annee=payload.annee,
                mois=payload.mois,
                montant_ttc=ligne.montant_ttc,
                montant_ht=ht
            ))

    db.commit()
    return {"message": "Revenus enregistrés"}

@router.post("/charges")
def save_charges(payload: SaisieCharges, db: Session = Depends(get_db)):
    ensure_open(db, payload.agence_id, payload.annee, payload.mois)

    for ligne in payload.lignes:
        ht = ligne.montant_ttc * TVA_FACTOR
        obj = db.query(Charge).filter_by(
            agence_id=payload.agence_id,
            concept_id=ligne.item_id,
            annee=payload.annee,
            mois=payload.mois
        ).first()

        if obj:
            obj.montant_ttc = ligne.montant_ttc
            obj.montant_ht = ht
        else:
            db.add(Charge(
                agence_id=payload.agence_id,
                concept_id=ligne.item_id,
                annee=payload.annee,
                mois=payload.mois,
                montant_ttc=ligne.montant_ttc,
                montant_ht=ht
            ))

    db.commit()
    return {"message": "Charges enregistrées"}
