import React from 'react';
import { createRoot } from 'react-dom/client';
import './styles/app.css';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App(){
  return <div className="app">
    <aside className="sidebar">
      <div className="brand"><div className="logo">3M</div><div><b>3M CASH</b><span>Gestion Financière</span></div></div>
      {['Tableau de bord','Saisie des données','État financier','État global société','Comparaison','Paramètres'].map(x=><div className="nav" key={x}>{x}</div>)}
    </aside>
    <main className="main">
      <header><h1>Tableau de bord</h1><button onClick={()=>fetch(API+'/api/init',{method:'POST'}).then(()=>alert('Données initiales créées'))}>Initialiser</button></header>
      <section className="cards">
        <Card title="Revenus TTC" value="0,00 DH" />
        <Card title="Charges TTC" value="0,00 DH" />
        <Card title="Résultat TTC" value="0,00 DH" accent />
        <Card title="Résultat HT" value="0,00 DH" />
      </section>
      <section className="panel"><h2>Saisie rapide</h2><p>Sélectionnez une agence, une année et un mois pour saisir les montants TTC. Le HT est calculé automatiquement: HT = TTC × 0,80.</p></section>
      <section className="panel"><h2>Comparaison</h2><p>Comparaison rapide: mois, trimestre, semestre, année. Comparaison personnalisée: deux périodes libres, toutes les agences ou agences sélectionnées, avec filtre par produit et Top Progression / Régression.</p></section>
    </main>
  </div>
}
function Card({title,value,accent}){return <div className={accent?'card accent':'card'}><span>{title}</span><strong>{value}</strong></div>}

createRoot(document.getElementById('root')).render(<App/>);
