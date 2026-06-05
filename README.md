# 3M CASH – Gestion Financière

Application web de gestion financière des agences.

## Stack
- Frontend: React + Vite
- Backend: FastAPI
- Base de données: PostgreSQL
- Déploiement: Railway

## Règle financière
L'utilisateur saisit le montant TTC. L'application calcule automatiquement:

HT = TTC × 0.80

## Lancement local

Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Données initiales
Après lancement du backend, appeler:

POST /api/init
