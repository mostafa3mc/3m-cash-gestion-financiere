from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .core.database import Base

class Agence(Base):
    __tablename__ = "agences"
    id = Column(Integer, primary_key=True)
    nom = Column(String, unique=True, nullable=False)
    ville = Column(String, nullable=True)
    actif = Column(Boolean, default=True)

class Produit(Base):
    __tablename__ = "produits"
    id = Column(Integer, primary_key=True)
    nom = Column(String, unique=True, nullable=False)
    actif = Column(Boolean, default=True)

class CategorieCharge(Base):
    __tablename__ = "categories_charges"
    id = Column(Integer, primary_key=True)
    nom = Column(String, unique=True, nullable=False)
    actif = Column(Boolean, default=True)

class ConceptCharge(Base):
    __tablename__ = "concepts_charges"
    id = Column(Integer, primary_key=True)
    categorie_id = Column(Integer, ForeignKey("categories_charges.id"), nullable=False)
    nom = Column(String, nullable=False)
    actif = Column(Boolean, default=True)
    categorie = relationship("CategorieCharge")
    __table_args__ = (UniqueConstraint("categorie_id", "nom", name="uq_concept_categorie"),)

class Revenu(Base):
    __tablename__ = "revenus"
    id = Column(Integer, primary_key=True)
    agence_id = Column(Integer, ForeignKey("agences.id"), nullable=False)
    produit_id = Column(Integer, ForeignKey("produits.id"), nullable=False)
    annee = Column(Integer, nullable=False)
    mois = Column(Integer, nullable=False)
    montant_ttc = Column(Numeric(14, 2), default=0)
    montant_ht = Column(Numeric(14, 2), default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    __table_args__ = (UniqueConstraint("agence_id", "produit_id", "annee", "mois", name="uq_revenu_mensuel"),)

class Charge(Base):
    __tablename__ = "charges"
    id = Column(Integer, primary_key=True)
    agence_id = Column(Integer, ForeignKey("agences.id"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts_charges.id"), nullable=False)
    annee = Column(Integer, nullable=False)
    mois = Column(Integer, nullable=False)
    montant_ttc = Column(Numeric(14, 2), default=0)
    montant_ht = Column(Numeric(14, 2), default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    __table_args__ = (UniqueConstraint("agence_id", "concept_id", "annee", "mois", name="uq_charge_mensuelle"),)

class ClotureMensuelle(Base):
    __tablename__ = "clotures_mensuelles"
    id = Column(Integer, primary_key=True)
    agence_id = Column(Integer, ForeignKey("agences.id"), nullable=False)
    annee = Column(Integer, nullable=False)
    mois = Column(Integer, nullable=False)
    cloture = Column(Boolean, default=False)
    __table_args__ = (UniqueConstraint("agence_id", "annee", "mois", name="uq_cloture"),)
