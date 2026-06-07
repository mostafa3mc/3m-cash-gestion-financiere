import React from 'react';
import { createRoot } from 'react-dom/client';
import './styles/app.css';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App(){
const [page, setPage] = React.useState('Tableau de bord');
  const menu = [
    'Tableau de bord',
    'Saisie des données',
    'État financier',
    'État global société',
    'Comparaison',
    'Paramètres'
  ];

  return <div className="app">
    <aside className="sidebar">
      <div className="brand">
        <div className="logo">3M</div>
        <div><b>3M CASH</b><span>Gestion Financière</span></div>
      </div>

      {menu.map(x =>
        <div
          className={page === x ? 'nav active' : 'nav'}
          key={x}
          onClick={() => setPage(x)}
        >
          {x}
        </div>
      )}
    </aside>

    <main className="main">
      <header>
        <h1>{page}</h1>
        <button onClick={()=>fetch(API+'/api/init',{method:'POST'}).then(()=>alert('Données initiales créées'))}>
          Initialiser
        </button>
      </header>

      {page === 'Tableau de bord' && <Dashboard />}
      {page === 'Saisie des données' && <Saisie />}
      {page === 'État financier' && <EtatFinancier />}
      {page === 'État global société' && <EtatGlobal />}
      {page === 'Comparaison' && <Comparaison />}
      {page === 'Paramètres' && <Parametres />}
    </main>
  </div>
}

function Dashboard(){
  return <>
    <section className="cards">
      <Card title="Revenus TTC" value="0,00 DH" />
      <Card title="Charges TTC" value="0,00 DH" />
      <Card title="Résultat TTC" value="0,00 DH" accent />
      <Card title="Résultat HT" value="0,00 DH" />
    </section>
    <section className="panel">
      <h2>Saisie rapide</h2>
      <p>Sélectionnez une agence, une année et un mois pour saisir les montants TTC. Le HT est calculé automatiquement: HT = TTC × 0,80.</p>
    </section>
    <section className="panel">
      <h2>Comparaison</h2>
      <p>Comparaison rapide: mois, trimestre, semestre, année. Comparaison personnalisée: deux périodes libres, toutes les agences ou agences sélectionnées, avec filtre par produit et Top Progression / Régression.</p>
    </section>
  </>
}

function Saisie(){
  return <section className="panel">
    <h2>Saisie des données</h2>
    <p>Écran destiné à saisir les revenus et les charges TTC par agence, année et mois.</p>
  </section>
}

function EtatFinancier(){
  return <section className="panel">
    <h2>État financier par agence</h2>
    <p>Affichage de l’état financier détaillé d’une agence.</p>
  </section>
}

function EtatGlobal(){
  return <section className="panel">
    <h2>État global société</h2>
    <p>Affichage consolidé de toutes les agences.</p>
  </section>
}

function Comparaison(){
  return <section className="panel">
    <h2>Comparaison</h2>
    <p>Comparaison rapide ou personnalisée entre deux périodes, avec filtre par agence et par produit.</p>
  </section>
}

function Parametres(){
  return <section className="panel">
    <h2>Paramètres</h2>
    <p>Gestion des agences, produits, catégories, concepts et utilisateurs.</p>
  </section>
}

function Card({title,value,accent}){
  return <div className={accent?'card accent':'card'}>
    <span>{title}</span>
    <strong>{value}</strong>
  </div>
}

createRoot(document.getElementById('root')).render(<App/>);
