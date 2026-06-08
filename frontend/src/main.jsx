import React from 'react';
import { createRoot } from 'react-dom/client';
import './styles/app.css';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const moisListe = [
  'Janvier','Février','Mars','Avril','Mai','Juin',
  'Juillet','Août','Septembre','Octobre','Novembre','Décembre'
];

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
  </>
}

function Saisie(){
  const [refs, setRefs] = React.useState({agences:[], produits:[], concepts:[]});
  const [agenceId, setAgenceId] = React.useState('');
  const [annee, setAnnee] = React.useState(new Date().getFullYear());
  const [mois, setMois] = React.useState(new Date().getMonth() + 1);
  const [revenus, setRevenus] = React.useState({});
  const [charges, setCharges] = React.useState({});
  React.useEffect(() => {
  setRevenus({});
  setCharges({});
  }, [agenceId, annee, mois]);
  React.useEffect(() => {
    fetch(API + '/api/referentiels')
      .then(r => r.json())
      .then(data => setRefs(data))
      .catch(() => alert("Erreur de chargement des référentiels"));
  }, []);

  const totalRevenus = Object.values(revenus).reduce((a,b)=>a + Number(b || 0), 0);
  const totalCharges = Object.values(charges).reduce((a,b)=>a + Number(b || 0), 0);
  const resultat = totalRevenus - totalCharges;
  function handleEnter(e){
  if(e.key === 'Enter'){
    e.preventDefault();

    const inputs = Array.from(
      document.querySelectorAll('input, select, button')
    );

    const index = inputs.indexOf(e.target);

    if(index >= 0 && inputs[index + 1]){
      inputs[index + 1].focus();
    }
  }
}
  function save(){
    if(!agenceId){
      alert("Veuillez sélectionner une agence");
      return;
    }

    const lignesRevenus = Object.entries(revenus)
      .filter(([_,v]) => Number(v) > 0)
      .map(([id,v]) => ({item_id:Number(id), montant_ttc:Number(v)}));

    const lignesCharges = Object.entries(charges)
      .filter(([_,v]) => Number(v) > 0)
      .map(([id,v]) => ({item_id:Number(id), montant_ttc:Number(v)}));

    Promise.all([
      fetch(API + '/api/revenus', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({agence_id:Number(agenceId), annee:Number(annee), mois:Number(mois), lignes:lignesRevenus})
      }),
      fetch(API + '/api/charges', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({agence_id:Number(agenceId), annee:Number(annee), mois:Number(mois), lignes:lignesCharges})
      })
    ])
    .then(() => alert("Données enregistrées avec succès"))
    .catch(() => alert("Erreur lors de l'enregistrement"));
  }

  return <>
    <section className="panel">
      <h2>Saisie des données</h2>

      <div style={{display:'grid', gridTemplateColumns:'repeat(3, 1fr)', gap:16, marginBottom:20}}>
        <label>Agence
          <select value={agenceId} onChange={e=>setAgenceId(e.target.value)}>
            <option value="">Sélectionner</option>
            {refs.agences.map(a => <option key={a.id} value={a.id}>{a.nom}</option>)}
          </select>
        </label>

        <label>Année
                <input
        type="number"
        value={annee}
        onChange={e=>setAnnee(e.target.value)}
        onKeyDown={handleEnter}
      />
        </label>

        <label>Mois
          <select value={mois} onChange={e=>setMois(e.target.value)}>
            {moisListe.map((m,i)=><option key={m} value={i+1}>{m}</option>)}
          </select>
        </label>
      </div>
    </section>

    <section className="panel">
      <h2>Revenus TTC</h2>
      {refs.produits.map(p =>
        <div key={p.id} style={{display:'grid', gridTemplateColumns:'1fr 200px', gap:12, marginBottom:10}}>
          <span>{p.nom}</span>
                <input
        type="number"
        placeholder="0,00"
        value={revenus[p.id] || ''}
        onChange={e=>setRevenus({...revenus, [p.id]:e.target.value})}
        onKeyDown={handleEnter}
      />
        </div>
      )}
    </section>

    <section className="panel">
      <h2>Charges TTC</h2>
      {refs.concepts.map(c =>
        <div key={c.id} style={{display:'grid', gridTemplateColumns:'1fr 200px', gap:12, marginBottom:10}}>
          <span>{c.nom}</span>
                <input
        type="number"
        placeholder="0,00"
        value={charges[c.id] || ''}
        onChange={e=>setCharges({...charges, [c.id]:e.target.value})}
        onKeyDown={handleEnter}
      />
        </div>
      )}
    </section>

    <section className="cards">
      <Card title="Revenus TTC" value={format(totalRevenus)} />
      <Card title="Charges TTC" value={format(totalCharges)} />
      <Card title="Résultat TTC" value={format(resultat)} accent />
      <Card title="Résultat HT" value={format(resultat * 0.80)} />
    </section>

    <button onClick={save} style={{padding:'14px 24px', fontWeight:'bold', marginTop:20}}>
      Enregistrer
    </button>
  </>
}

function EtatFinancier(){
  return <section className="panel">
    <h2>État financier par agence</h2>
    <p>Cette page sera connectée après la saisie réelle des données.</p>
  </section>
}

function EtatGlobal(){
  return <section className="panel">
    <h2>État global société</h2>
    <p>Cette page affichera le total consolidé de toutes les agences.</p>
  </section>
}

function Comparaison(){
  return <section className="panel">
    <h2>Comparaison</h2>
    <p>Comparaison entre deux périodes.</p>
  </section>
}

function Parametres(){
  return <section className="panel">
    <h2>Paramètres</h2>
    <p>Gestion des agences, produits, catégories et concepts.</p>
  </section>
}

function Card({title,value,accent}){
  return <div className={accent?'card accent':'card'}>
    <span>{title}</span>
    <strong>{value}</strong>
  </div>
}

function format(n){
  return Number(n || 0).toLocaleString('fr-FR', {
    minimumFractionDigits:2,
    maximumFractionDigits:2
  }) + ' DH';
}

createRoot(document.getElementById('root')).render(<App/>);
