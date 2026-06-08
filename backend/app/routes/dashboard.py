from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import Revenu, Charge

router = APIRouter(tags=["dashboard"])

@router.get("/dashboard/global")
def dashboard_global(annee: int, mois: int | None = None, db: Session = Depends(get_db)):
    rq = db.query(func.coalesce(func.sum(Revenu.montant_ttc),0), func.coalesce(func.sum(Revenu.montant_ht),0)).filter(Revenu.annee==annee)
    cq = db.query(func.coalesce(func.sum(Charge.montant_ttc),0), func.coalesce(func.sum(Charge.montant_ht),0)).filter(Charge.annee==annee)
    if mois:
        rq = rq.filter(Revenu.mois==mois); cq = cq.filter(Charge.mois==mois)
    rev_ttc, rev_ht = rq.one(); ch_ttc, ch_ht = cq.one()
    return {"revenus_ttc": float(rev_ttc), "revenus_ht": float(rev_ht), "charges_ttc": float(ch_ttc), "charges_ht": float(ch_ht), "net_ttc": float(rev_ttc-ch_ttc), "net_ht": float(rev_ht-ch_ht)}

@router.get("/dashboard/agence")
def dashboard_agence(
    agence_id: int,
    annee: int,
    mois: int | None = None,
    db: Session = Depends(get_db)
):
    rq = db.query(
        func.coalesce(func.sum(Revenu.montant_ttc), 0),
        func.coalesce(func.sum(Revenu.montant_ht), 0)
    ).filter(
        Revenu.agence_id == agence_id,
        Revenu.annee == annee
    )

    cq = db.query(
        func.coalesce(func.sum(Charge.montant_ttc), 0),
        func.coalesce(func.sum(Charge.montant_ht), 0)
    ).filter(
        Charge.agence_id == agence_id,
        Charge.annee == annee
    )

    if mois:
        rq = rq.filter(Revenu.mois == mois)
        cq = cq.filter(Charge.mois == mois)

    rev_ttc, rev_ht = rq.one()
    ch_ttc, ch_ht = cq.one()

    return {
        "revenus_ttc": float(rev_ttc),
        "revenus_ht": float(rev_ht),
        "charges_ttc": float(ch_ttc),
        "charges_ht": float(ch_ht),
        "net_ttc": float(rev_ttc - ch_ttc),
        "net_ht": float(rev_ht - ch_ht)
    }
