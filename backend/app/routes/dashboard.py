from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import Revenu, Charge, Agence

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

@router.get("/comparaison")
def comparaison(
    annee_a: int,
    mois_a: int,
    annee_b: int,
    mois_b: int,
    agence_ids: str | None = None,
    db: Session = Depends(get_db)
):
    agences_query = db.query(Agence).order_by(Agence.nom)

    if agence_ids:
        ids = [int(x) for x in agence_ids.split(",") if x.strip()]
        agences_query = agences_query.filter(Agence.id.in_(ids))

    agences = agences_query.all()
    resultats = []

    for agence in agences:
        rev_a = db.query(func.coalesce(func.sum(Revenu.montant_ttc), 0)).filter(
            Revenu.agence_id == agence.id,
            Revenu.annee == annee_a,
            Revenu.mois == mois_a
        ).scalar()

        ch_a = db.query(func.coalesce(func.sum(Charge.montant_ttc), 0)).filter(
            Charge.agence_id == agence.id,
            Charge.annee == annee_a,
            Charge.mois == mois_a
        ).scalar()

        rev_b = db.query(func.coalesce(func.sum(Revenu.montant_ttc), 0)).filter(
            Revenu.agence_id == agence.id,
            Revenu.annee == annee_b,
            Revenu.mois == mois_b
        ).scalar()

        ch_b = db.query(func.coalesce(func.sum(Charge.montant_ttc), 0)).filter(
            Charge.agence_id == agence.id,
            Charge.annee == annee_b,
            Charge.mois == mois_b
        ).scalar()

        periode_a = float(rev_a - ch_a)
        periode_b = float(rev_b - ch_b)
        variation = periode_b - periode_a

        if periode_a != 0:
            variation_pct = (variation / abs(periode_a)) * 100
        else:
            variation_pct = 100 if periode_b > 0 else 0

        resultats.append({
            "agence_id": agence.id,
            "agence": agence.nom,
            "periode_a": periode_a,
            "periode_b": periode_b,
            "variation": variation,
            "variation_pct": variation_pct
        })

    resultats.sort(key=lambda x: x["variation_pct"], reverse=True)

    return resultats
