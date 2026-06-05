from pydantic import BaseModel
from decimal import Decimal

class AgenceCreate(BaseModel):
    nom: str
    ville: str | None = None

class ItemMontant(BaseModel):
    item_id: int
    montant_ttc: Decimal

class SaisieRevenus(BaseModel):
    agence_id: int
    annee: int
    mois: int
    lignes: list[ItemMontant]

class SaisieCharges(BaseModel):
    agence_id: int
    annee: int
    mois: int
    lignes: list[ItemMontant]
