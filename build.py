# -*- coding: utf-8 -*-
"""Construit la page catalogue B2B en un seul fichier HTML autonome.

Pourquoi un fichier unique : le client doit pouvoir l'ouvrir depuis son
telephone sans que rien ne dependre d'un serveur. Tout est inline, aucune
requete externe, aucune police distante.

Le catalogue de demonstration est DETERMINISTE — il derive d'un hachage du nom
de la sous-famille. Deux constructions donnent exactement le meme fichier, donc
une difference dans le rendu vient d'un changement que j'ai fait, jamais du
generateur.
"""
import hashlib, html, json, sys
from data import ARBRE, FACETTES, MARQUES, MARQUE, ACCENT, ACCENT_D

SORTIE = sys.argv[1] if len(sys.argv) > 1 else 'index.html'


def graine(*parts):
    h = hashlib.sha1('|'.join(str(p) for p in parts).encode('utf-8')).digest()
    return int.from_bytes(h[:6], 'big')


def tirer(g, options):
    return options[g % len(options)]


# Conditionnements pour du consommable : on vend a la boite ou au carton.
CONDITS_CONSO = [
    ('Boîte de 100', 100, 'boîte'), ('Boîte de 50', 50, 'boîte'),
    ('Sachet de 25', 25, 'sachet'), ('Carton de 10', 10, 'carton'),
    ('Boîte de 200', 200, 'boîte'),
]
# Un lit medicalise ne se vend pas par boite de 200.
CONDITS_EQUIP = [('À l’unité', 1, 'unité'), ('Lot de 2', 2, 'lot')]

# Fourchette de prix UNITAIRE credible par rayon, en centimes. Sans elle le
# generateur sortait 7,38 EUR pour UN gant d'examen — un acheteur du secteur
# ferme la page a ce moment-la. La demo doit etre credible sur les ordres de
# grandeur, meme si les articles ne sont pas reels.
BANDES = {
    'epi':         (3,    250),      # gants, masques, blouses
    'soin':        (5,    400),      # pansements, compresses
    'injection':   (3,    180),      # seringues, aiguilles, catheters
    'diagnostic':  (900,  18000),    # tensiometres, stethoscopes, oxymetres
    'hygiene':     (80,   2500),     # antiseptiques, desinfectants
    'bloc':        (40,   3500),     # champs, kits de procedure
    'respi':       (60,   4000),     # oxygenotherapie, nebuliseurs
    'patient':     (15,   900),      # incontinence, sondage
    'mobilier':    (8000, 250000),   # tables, chariots, lits
    'mobilite':    (4000, 120000),   # fauteuils, deambulateurs
    'dechets':     (30,   2200),     # collecteurs, sacs
    'psy':         (150,  180000),   # du textile anti-dechirure au mobilier
    'medicament':  (40,   95000),    # du pilulier au refrigerateur medical
    'labo':        (5,    1500),     # tubes, contenants
}
SEUIL_EQUIP = 3000                   # au-dela de 30 EUR l'unite, on vend a l'unite


def produits():
    """Un catalogue de demonstration, deterministe, quatre articles par
       sous-famille. Le nombre est volontairement petit : la demo doit montrer
       la STRUCTURE, pas simuler un stock reel."""
    out = []
    for rayon, rslug, familles in ARBRE:
        for famille, fslug, sous in familles:
            for sf in sous:
                for i in range(4):
                    g = graine(rslug, fslug, sf, i)
                    marque = tirer(g, MARQUES)
                    lo, hi = BANDES[rslug]
                    base = lo + (g >> 7) % (hi - lo + 1)   # centimes
                    pu = base / 100.0
                    # le conditionnement suit le prix, pas le hasard
                    cond, par, mot = tirer(
                        g >> 3, CONDITS_EQUIP if base >= SEUIL_EQUIP else CONDITS_CONSO)
                    # Le prix a la caisse est plus avantageux que N fois le prix
                    # unitaire — c'est ce qui distingue le B2B du B2C. Mais une
                    # « caisse » de 1 ne peut pas etre moins chere que son propre
                    # article : sans ce garde-fou la fiche s'auto-contredisait.
                    remise = 1.0 if par == 1 else 0.88 - ((g >> 11) % 9) / 100.0
                    pcaisse = round(pu * par * remise, 2)
                    stock = ((g >> 13) % 5) != 0
                    ster = 'Stérile' if (g >> 17) % 2 else 'Non stérile'
                    latex = 'Contient du latex' if (g >> 19) % 7 == 0 else 'Sans latex'
                    usage = 'Réutilisable' if (g >> 23) % 8 == 0 else 'Usage unique'
                    conditio = ('À l’unité' if par == 1 else
                                'Carton' if mot == 'carton' else 'Boîte')
                    # un lit ne se decline pas en taille XL
                    equip = base >= SEUIL_EQUIP
                    taille = '—' if base >= SEUIL_EQUIP else \
                        tirer(g >> 29, ['XS', 'S', 'M', 'L', 'XL', '—'])
                    ref = '%s-%s-%03d' % (rslug[:3].upper(), fslug[:3].upper(),
                                          (g >> 31) % 1000)
                    out.append({
                        'ref': ref,
                        'nom': sf if taille == '—' else '%s — taille %s' % (sf, taille),
                        'marque': marque,
                        'rayon': rayon, 'rslug': rslug,
                        'famille': famille, 'fslug': fslug,
                        'sous': sf,
                        'cond': cond, 'par': par,
                        'pu': round(pu, 2), 'pcaisse': pcaisse,
                        'dispo': 'En stock' if stock else 'Sur commande',
                        'sterile': ster, 'latex': latex, 'usage': usage,
                        'conditio': conditio,
                        # paliers de quantite : la mecanique B2B qui manque
                        # a 90 % des boutiques
                        'paliers': [
                            {'q': 1,  'p': pcaisse},
                            {'q': 6,  'p': round(pcaisse * 0.95, 2)},
                            {'q': 24, 'p': round(pcaisse * 0.89, 2)},
                            {'q': 96, 'p': round(pcaisse * 0.82, 2)},
                        ],
                    })
    return out


CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{
  --ac:__AC__; --ac-d:__ACD__;
  --ink:#12181f; --ink2:#3c4854; --mut:#5f6b78;
  --line:#e2e7ec; --line2:#eef1f4; --bg:#ffffff; --bg2:#f7f9fb;
  --ok:#0d7a4a; --att:#8a5a12;
}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--ink);
  font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,
  "Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--ac);text-decoration:none}
a:hover{text-decoration:underline}

/* --- le bandeau de demo. Il reste : le catalogue n'est pas reel --- */
.demo{background:#12181f;color:#e8eef4;font-size:12.5px;padding:7px 16px;
  text-align:center;letter-spacing:.01em}
.demo b{color:#ffd479}

/* --- en-tete --- */
header{border-bottom:1px solid var(--line);position:sticky;top:0;background:#fff;z-index:20}
.hbar{display:flex;align-items:center;gap:18px;padding:12px 20px;max-width:1560px;margin:0 auto}
.logo{font-weight:800;font-size:20px;letter-spacing:-.02em;color:var(--ink);white-space:nowrap}
.logo span{color:var(--ac)}
.search{flex:1;display:flex;border:1.5px solid var(--line);border-radius:3px;overflow:hidden}
.search:focus-within{border-color:var(--ac)}
.search input{flex:1;border:0;padding:10px 13px;font:inherit;outline:0;min-width:0}
.search button{border:0;background:var(--ac);color:#fff;padding:0 18px;font:600 14px/1 inherit;cursor:pointer}
.hact{display:flex;align-items:center;gap:8px;white-space:nowrap}
.hbtn{border:1.5px solid var(--line);background:#fff;color:var(--ink);
  padding:9px 13px;border-radius:3px;font:600 13.5px/1 inherit;cursor:pointer}
.hbtn:hover{border-color:var(--ac);color:var(--ac)}
.hbtn-p{background:var(--ac);border-color:var(--ac);color:#fff}
.hbtn-p:hover{background:var(--ac-d);border-color:var(--ac-d);color:#fff}
.cptr{background:#fff;color:var(--ac);border-radius:2px;padding:1px 5px;
  font-weight:800;margin-left:6px;font-size:12px}

/* --- mise en page : colonne fixe + contenu --- */
.shell{display:grid;grid-template-columns:288px 1fr;gap:0;max-width:1560px;margin:0 auto}
aside{border-right:1px solid var(--line);padding:18px 0 60px;
  position:sticky;top:57px;align-self:start;max-height:calc(100vh - 57px);overflow-y:auto}
main{padding:18px 22px 70px;min-width:0}

/* --- L'ARBRE. La piece centrale. --- */
.tree-h{font:700 11.5px/1 inherit;letter-spacing:.13em;text-transform:uppercase;
  color:var(--mut);padding:0 18px 10px}
.tree{list-style:none;margin:0;padding:0}
.tree li{list-style:none}
.r-t{display:flex;align-items:center;gap:8px;width:100%;text-align:left;
  border:0;background:none;font:600 14px/1.35 inherit;color:var(--ink);
  padding:8px 18px;cursor:pointer}
.r-t:hover{background:var(--bg2);color:var(--ac)}
.r-t .ch{color:var(--mut);font-size:11px;width:9px;flex:0 0 9px;transition:transform .12s}
.r-t[aria-expanded="true"] .ch{transform:rotate(90deg)}
.r-t .n{margin-left:auto;color:var(--mut);font-weight:500;font-size:12px}
.f-l{list-style:none;margin:0;padding:0 0 6px}
.f-t{display:flex;align-items:center;gap:8px;width:100%;text-align:left;border:0;
  background:none;font:500 13.5px/1.35 inherit;color:var(--ink2);
  padding:6px 18px 6px 35px;cursor:pointer}
.f-t:hover{background:var(--bg2);color:var(--ac)}
.f-t .ch{color:var(--mut);font-size:10px;width:8px;flex:0 0 8px;transition:transform .12s}
.f-t[aria-expanded="true"] .ch{transform:rotate(90deg)}
.s-l{list-style:none;margin:0;padding:2px 0 6px}
.s-l a{display:block;padding:5px 18px 5px 52px;font-size:13px;color:var(--ink2)}
.s-l a:hover{background:var(--bg2);color:var(--ac);text-decoration:none}
.s-l a.on{color:var(--ac);font-weight:700;box-shadow:inset 3px 0 0 var(--ac);background:var(--bg2)}
[hidden]{display:none !important}

/* --- facettes --- */
.fac{border-top:1px solid var(--line);margin-top:16px;padding-top:14px}
.fac h4{font:700 11.5px/1 inherit;letter-spacing:.13em;text-transform:uppercase;
  color:var(--mut);margin:0 0 8px;padding:0 18px}
.fgrp{padding:0 18px 12px}
.fgrp>b{display:block;font-size:13px;margin-bottom:5px;font-weight:700}
.fgrp label{display:flex;align-items:center;gap:7px;font-size:13px;
  color:var(--ink2);padding:2.5px 0;cursor:pointer}
.fgrp input{margin:0;accent-color:var(--ac)}
.fgrp label span{margin-left:auto;color:var(--mut);font-size:11.5px}

/* --- fil d'ariane + barre d'outils --- */
.crumb{font-size:12.5px;color:var(--mut);margin-bottom:10px}
.crumb a{color:var(--mut)}
.crumb b{color:var(--ink)}
h1{font-size:23px;letter-spacing:-.02em;margin:0 0 4px;line-height:1.2}
.count{color:var(--mut);font-size:13.5px;margin-bottom:14px}
.tools{display:flex;flex-wrap:wrap;align-items:center;gap:10px;
  border-block:1px solid var(--line);padding:9px 0;margin-bottom:2px}
.tools select{border:1.5px solid var(--line);border-radius:3px;padding:6px 9px;font:inherit;font-size:13px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0}
.chip{display:inline-flex;align-items:center;gap:6px;background:var(--bg2);
  border:1px solid var(--line);border-radius:2px;padding:4px 8px;font-size:12.5px}
.chip button{border:0;background:none;cursor:pointer;color:var(--mut);font-size:14px;line-height:1;padding:0}
.chip button:hover{color:#b3261e}
.raz{border:0;background:none;color:var(--ac);font:600 12.5px inherit;cursor:pointer;padding:4px}

/* --- LES CARTES PRODUIT. Denses : c'est du B2B. --- */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(268px,1fr));
  gap:0;border-top:1px solid var(--line2);margin-top:14px}
.card{border-right:1px solid var(--line2);border-bottom:1px solid var(--line2);
  padding:15px 16px 14px;display:flex;flex-direction:column;gap:7px;background:#fff}
.card:hover{background:#fcfdfe}
.vign{height:104px;border:1px solid var(--line2);border-radius:2px;background:var(--bg2);
  display:flex;align-items:center;justify-content:center;color:#c4ced8;margin-bottom:3px}
.vign svg{width:40px;height:40px}
.ref{font:600 11.5px/1 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  color:var(--mut);letter-spacing:.03em}
.card h3{font-size:14px;font-weight:600;line-height:1.35;margin:0;color:var(--ink)}
.card h3 a{color:inherit}
.mq{font-size:12.5px;color:var(--mut)}
.prix{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;margin-top:2px}
.pc{font-size:20px;font-weight:800;letter-spacing:-.02em}
.pcu{font-size:12.5px;color:var(--mut)}
.cond{font-size:12.5px;color:var(--ink2)}
.paliers{border-top:1px dashed var(--line);padding-top:7px;margin-top:2px;
  font-size:12px;color:var(--ink2);display:flex;flex-wrap:wrap;gap:3px 12px}
.paliers b{font-weight:700;color:var(--ink)}
.dispo{font-size:12.5px;font-weight:600;display:flex;align-items:center;gap:6px}
.dispo::before{content:"";width:7px;height:7px;border-radius:50%;background:currentColor}
.d-ok{color:var(--ok)} .d-cmd{color:var(--att)}
.tags{display:flex;flex-wrap:wrap;gap:4px}
.tag{font-size:11px;border:1px solid var(--line);border-radius:2px;padding:1px 6px;color:var(--ink2)}
.add{display:flex;gap:6px;margin-top:auto;padding-top:9px}
.add input{width:62px;border:1.5px solid var(--line);border-radius:3px;padding:7px 8px;font:inherit;font-size:13px}
.add button{flex:1;border:1.5px solid var(--ac);background:var(--ac);color:#fff;
  border-radius:3px;padding:7px 10px;font:700 13px/1.2 inherit;cursor:pointer}
.add button:hover{background:var(--ac-d);border-color:var(--ac-d)}
.vide{padding:52px 10px;text-align:center;color:var(--mut);grid-column:1/-1}

/* --- commande rapide par reference --- */
.qo{border:1.5px solid var(--line);border-radius:3px;padding:14px 16px;margin:0 0 16px;background:var(--bg2)}
.qo h3{margin:0 0 3px;font-size:14.5px}
.qo p{margin:0 0 10px;font-size:12.5px;color:var(--mut)}
.qorow{display:flex;flex-wrap:wrap;gap:7px}
.qorow input{border:1.5px solid var(--line);border-radius:3px;padding:8px 10px;font:inherit;font-size:13px}
.qorow input.r{flex:1;min-width:150px;font-family:ui-monospace,Menlo,Consolas,monospace}
.qorow input.q{width:74px}
.qorow button{border:1.5px solid var(--ink);background:var(--ink);color:#fff;
  border-radius:3px;padding:8px 15px;font:700 13px inherit;cursor:pointer}
.qomsg{font-size:12.5px;margin-top:8px;min-height:17px}
.qomsg.ok{color:var(--ok)} .qomsg.ko{color:#b3261e}

/* --- panier / devis --- */
.pan{position:fixed;top:0;right:0;bottom:0;width:min(430px,100%);background:#fff;
  border-left:1px solid var(--line);box-shadow:-16px 0 40px rgba(18,24,31,.10);
  z-index:40;display:flex;flex-direction:column;transform:translateX(100%);
  transition:transform .18s ease}
.pan.on{transform:none}
.pan-h{display:flex;align-items:center;gap:10px;padding:15px 18px;border-bottom:1px solid var(--line)}
.pan-h h2{margin:0;font-size:16px}
.pan-h button{margin-left:auto;border:0;background:none;font-size:22px;line-height:1;
  cursor:pointer;color:var(--mut)}
.pan-b{flex:1;overflow-y:auto;padding:6px 18px}
.li{display:grid;grid-template-columns:1fr auto;gap:2px 12px;padding:12px 0;border-bottom:1px solid var(--line2)}
.li .n{font-size:13.5px;font-weight:600}
.li .r{font:11.5px ui-monospace,Menlo,Consolas,monospace;color:var(--mut)}
.li .q{font-size:12.5px;color:var(--ink2)}
.li .p{font-weight:700;text-align:right;white-space:nowrap}
.li .x{border:0;background:none;color:var(--mut);cursor:pointer;text-align:right;font-size:12px}
.li .x:hover{color:#b3261e}
.pan-f{border-top:1px solid var(--line);padding:15px 18px}
.tot{display:flex;justify-content:space-between;font-size:17px;font-weight:800;margin-bottom:4px}
.pan-f p{font-size:12px;color:var(--mut);margin:0 0 11px}
.pan-f button{width:100%;border:1.5px solid var(--ac);background:var(--ac);color:#fff;
  border-radius:3px;padding:12px;font:700 14px inherit;cursor:pointer}
.pan-f button.g{background:#fff;color:var(--ink);border-color:var(--line);margin-top:7px}
.voile{position:fixed;inset:0;background:rgba(18,24,31,.32);z-index:35;display:none}
.voile.on{display:block}

.burger{display:none}
@media (max-width:1000px){
  .shell{grid-template-columns:1fr}
  aside{position:fixed;top:0;bottom:0;left:0;width:300px;background:#fff;z-index:38;
    max-height:none;transform:translateX(-100%);transition:transform .18s ease;
    border-right:1px solid var(--line);padding-top:14px}
  aside.on{transform:none}
  .burger{display:inline-block}
  .hbar{flex-wrap:wrap}
  .search{order:3;flex-basis:100%}
}
@media (max-width:560px){
  .grid{grid-template-columns:1fr}
  .logo{font-size:17px}
}
""".replace('__AC__', ACCENT).replace('__ACD__', ACCENT_D)


JS = """
const P = PRODUITS, TREE = ARBRE;
const etat = {sous:null, famille:null, rayon:null, q:'', fac:{}, tri:'pertinence'};
const panier = [];
const $ = s => document.querySelector(s);
const eur = v => v.toFixed(2).replace('.', ',') + ' \\u20ac';

/* --- l'arbre : deplier/replier, et selectionner une sous-famille --- */
function basculer(btn){
  const ouvert = btn.getAttribute('aria-expanded') === 'true';
  btn.setAttribute('aria-expanded', ouvert ? 'false' : 'true');
  btn.nextElementSibling.hidden = ouvert;
}
document.addEventListener('click', e => {
  const t = e.target.closest('.r-t,.f-t');
  if (t) { basculer(t); return; }
  const a = e.target.closest('.s-l a');
  if (a) {
    e.preventDefault();
    document.querySelectorAll('.s-l a.on').forEach(x => x.classList.remove('on'));
    a.classList.add('on');
    etat.sous = a.dataset.sous; etat.famille = a.dataset.famille; etat.rayon = a.dataset.rayon;
    if (window.innerWidth <= 1000) { $('aside').classList.remove('on'); $('.voile').classList.remove('on'); }
    rendre();
  }
});

/* --- filtrage : categorie, recherche plein texte, facettes cumulees --- */
function filtrer(){
  const q = etat.q.trim().toLowerCase();
  return P.filter(p => {
    if (etat.sous && p.sous !== etat.sous) return false;
    if (!etat.sous && etat.famille && p.famille !== etat.famille) return false;
    if (!etat.sous && !etat.famille && etat.rayon && p.rayon !== etat.rayon) return false;
    if (q && !(p.nom + ' ' + p.marque + ' ' + p.ref + ' ' + p.famille).toLowerCase().includes(q)) return false;
    for (const [k, vals] of Object.entries(etat.fac)) {
      if (!vals.length) continue;
      const champ = k === 'conditio' ? p.conditio : k === 'sterile' ? p.sterile
                  : k === 'usage' ? p.usage : k === 'latex' ? p.latex
                  : k === 'dispo' ? p.dispo : p.marque;
      if (!vals.includes(champ)) return false;
    }
    return true;
  });
}

function trier(list){
  const l = list.slice();
  if (etat.tri === 'prix-c')  l.sort((a,b) => a.pcaisse - b.pcaisse);
  if (etat.tri === 'prix-d')  l.sort((a,b) => b.pcaisse - a.pcaisse);
  if (etat.tri === 'nom')     l.sort((a,b) => a.nom.localeCompare(b.nom, 'fr'));
  if (etat.tri === 'ref')     l.sort((a,b) => a.ref.localeCompare(b.ref));
  return l;
}

/* --- les facettes se recalculent SUR le resultat courant : une case qui
       ne menerait a rien n'est pas proposee --- */
function compter(cle, valeur, base){
  const champ = p => cle === 'conditio' ? p.conditio : cle === 'sterile' ? p.sterile
              : cle === 'usage' ? p.usage : cle === 'latex' ? p.latex
              : cle === 'dispo' ? p.dispo : p.marque;
  return base.filter(p => champ(p) === valeur).length;
}

function rendreFacettes(res){
  const box = $('#facettes');
  const html = FACETTES.map(([cle, titre, vals]) => {
    const liste = vals || MARQUES;
    const lignes = liste.map(v => {
      const n = compter(cle, v, res);
      const coche = (etat.fac[cle] || []).includes(v);
      if (!n && !coche) return '';
      return `<label><input type="checkbox" data-fac="${cle}" value="${v}"${coche ? ' checked' : ''}>`
           + `${v}<span>${n}</span></label>`;
    }).filter(Boolean).join('');
    if (!lignes) return '';
    return `<div class="fgrp"><b>${titre}</b>${lignes}</div>`;
  }).join('');
  box.innerHTML = html;
}

function chips(){
  const c = [];
  if (etat.rayon)  c.push(['rayon', etat.rayon]);
  if (etat.famille) c.push(['famille', etat.famille]);
  if (etat.sous)   c.push(['sous', etat.sous]);
  if (etat.q)      c.push(['q', '\\u00ab ' + etat.q + ' \\u00bb']);
  for (const [k, vals] of Object.entries(etat.fac))
    for (const v of vals) c.push(['fac:' + k + ':' + v, v]);
  $('#chips').innerHTML = c.length
    ? c.map(([k, l]) => `<span class="chip">${l}<button data-off="${k}" aria-label="retirer">\\u00d7</button></span>`).join('')
      + '<button class="raz" id="raz">Tout effacer</button>'
    : '';
}

function carte(p){
  const cls = p.dispo === 'En stock' ? 'd-ok' : 'd-cmd';
  const pal = p.paliers.map(t => `<span>${t.q}+ <b>${eur(t.p)}</b></span>`).join('');
  return `<article class="card">
    <div class="vign">${ICONE}</div>
    <div class="ref">${p.ref}</div>
    <h3><a href="#">${p.nom}</a></h3>
    <div class="mq">${p.marque}</div>
    <div class="prix"><span class="pc">${eur(p.pcaisse)}</span>
      <span class="pcu">${eur(p.pu)} / unit\\u00e9</span></div>
    <div class="cond">${p.cond}</div>
    <div class="paliers">${pal}</div>
    <div class="dispo ${cls}">${p.dispo}</div>
    <div class="tags"><span class="tag">${p.sterile}</span>
      <span class="tag">${p.usage}</span><span class="tag">${p.latex}</span></div>
    <div class="add"><input type="number" min="1" value="1" aria-label="Quantit\\u00e9" data-q="${p.ref}">
      <button data-add="${p.ref}">Ajouter</button></div>
  </article>`;
}

function rendre(){
  const res = trier(filtrer());
  $('#h1').textContent = etat.sous || etat.famille || etat.rayon || 'Tout le catalogue';
  $('#crumb').innerHTML = '<a href="#">Accueil</a> &rsaquo; '
    + (etat.rayon ? `<a href="#">${etat.rayon}</a> &rsaquo; ` : '')
    + (etat.famille ? `<a href="#">${etat.famille}</a> &rsaquo; ` : '')
    + `<b>${etat.sous || etat.famille || etat.rayon || 'Catalogue'}</b>`;
  $('#count').textContent = res.length + (res.length > 1 ? ' r\\u00e9f\\u00e9rences' : ' r\\u00e9f\\u00e9rence');
  $('#grid').innerHTML = res.length ? res.map(carte).join('')
    : '<p class="vide">Aucune r\\u00e9f\\u00e9rence ne correspond \\u00e0 ces crit\\u00e8res.</p>';
  rendreFacettes(filtrer0());
  chips();
}
/* le comptage des facettes ignore la facette elle-meme, sinon cocher une
   valeur ferait tomber toutes les autres a zero */
function filtrer0(){
  const sauv = etat.fac; etat.fac = {};
  const base = filtrer(); etat.fac = sauv; return base;
}

/* --- panier / devis --- */
/* Le prix qui s'applique reellement a une quantite. La fiche annonce
   « 6+ 95,72 EUR » : si le panier facture quand meme le prix de 1, l'acheteur
   le voit au premier coup d'oeil. Le palier est donc recalcule a chaque
   changement de quantite, pas fige au moment de l'ajout. */
function prixPalier(p, q){
  let t = p.paliers[0];
  for (const x of p.paliers) if (q >= x.q) t = x;
  return t;
}
function palierNom(l){
  const t = prixPalier(P.find(x => x.ref === l.ref), l.q);
  return t.q > 1 ? '  \u00b7 palier ' + t.q + '+' : '';
}
function ajouter(ref, q){
  const p = P.find(x => x.ref === ref); if (!p) return false;
  const l = panier.find(x => x.ref === ref);
  if (l) l.q += q; else panier.push({ref, nom: p.nom, q, pu: 0});
  majPanier(); return true;
}
function majPanier(){
  /* recalcul AVANT de sommer : un ajout peut faire franchir un palier a une
     ligne deja presente dans la demande */
  panier.forEach(l => { l.pu = prixPalier(P.find(x => x.ref === l.ref), l.q).p; });
  const n = panier.reduce((s, l) => s + l.q, 0);
  $('#cptr').textContent = n;
  $('#pan-b').innerHTML = panier.length ? panier.map(l => `<div class="li">
      <div><div class="n">${l.nom}</div><div class="r">${l.ref}</div>
      <div class="q">${l.q} \\u00d7 ${eur(l.pu)}${palierNom(l)}</div></div>
      <div><div class="p">${eur(l.q * l.pu)}</div>
      <button class="x" data-del="${l.ref}">Retirer</button></div></div>`).join('')
    : '<p class="vide">Votre demande est vide.</p>';
  $('#tot').textContent = eur(panier.reduce((s, l) => s + l.q * l.pu, 0));
}

document.addEventListener('click', e => {
  const a = e.target.closest('[data-add]');
  if (a) { const r = a.dataset.add;
    const q = Math.max(1, parseInt(document.querySelector(`[data-q="${r}"]`).value || '1', 10));
    ajouter(r, q); ouvrirPanier(true); return; }
  const d = e.target.closest('[data-del]');
  if (d) { const i = panier.findIndex(x => x.ref === d.dataset.del);
    if (i > -1) panier.splice(i, 1); majPanier(); return; }
  const off = e.target.closest('[data-off]');
  if (off) {
    const k = off.dataset.off;
    if (k === 'q') { etat.q = ''; $('#q').value = ''; }
    else if (k === 'sous') etat.sous = null;
    else if (k === 'famille') { etat.famille = null; etat.sous = null; }
    else if (k === 'rayon') { etat.rayon = null; etat.famille = null; etat.sous = null; }
    else { const [, cle, val] = k.split(':');
      etat.fac[cle] = (etat.fac[cle] || []).filter(v => v !== val); }
    document.querySelectorAll('.s-l a.on').forEach(x => x.classList.remove('on'));
    rendre(); return;
  }
  if (e.target.id === 'raz') {
    etat.sous = etat.famille = etat.rayon = null; etat.q = ''; etat.fac = {};
    $('#q').value = '';
    document.querySelectorAll('.s-l a.on').forEach(x => x.classList.remove('on'));
    rendre(); return;
  }
});

document.addEventListener('change', e => {
  const f = e.target.closest('[data-fac]');
  if (!f) return;
  const cle = f.dataset.fac;
  etat.fac[cle] = etat.fac[cle] || [];
  if (f.checked) etat.fac[cle].push(f.value);
  else etat.fac[cle] = etat.fac[cle].filter(v => v !== f.value);
  rendre();
});

$('#tri').addEventListener('change', e => { etat.tri = e.target.value; rendre(); });
$('#form').addEventListener('submit', e => { e.preventDefault(); etat.q = $('#q').value; rendre(); });

/* --- commande rapide par reference --- */
$('#qoform').addEventListener('submit', e => {
  e.preventDefault();
  const r = $('#qoref').value.trim().toUpperCase();
  const q = Math.max(1, parseInt($('#qoqte').value || '1', 10));
  const m = $('#qomsg');
  if (ajouter(r, q)) { m.className = 'qomsg ok'; m.textContent = q + ' \\u00d7 ' + r + ' ajout\\u00e9 \\u00e0 la demande.';
    $('#qoref').value = ''; ouvrirPanier(true); }
  else { m.className = 'qomsg ko'; m.textContent = 'R\\u00e9f\\u00e9rence ' + r + ' introuvable.'; }
});

function ouvrirPanier(on){
  $('.pan').classList.toggle('on', on); $('.voile').classList.toggle('on', on);
}
$('#voirpan').addEventListener('click', () => ouvrirPanier(true));
$('#ferme').addEventListener('click', () => ouvrirPanier(false));
$('.voile').addEventListener('click', () => { ouvrirPanier(false);
  $('aside').classList.remove('on'); $('.voile').classList.remove('on'); });
$('#burger').addEventListener('click', () => {
  $('aside').classList.add('on'); $('.voile').classList.add('on'); });

majPanier(); rendre();
"""

ICONE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="1.4"><rect x="3" y="7" width="18" height="13" rx="1.5"/>'
         '<path d="M8 7V5a2 2 0 012-2h4a2 2 0 012 2v2M3 12h18"/></svg>')


def arbre_html():
    o = ['<div class="tree-h">Catalogue</div>', '<ul class="tree">']
    for rayon, rslug, familles in ARBRE:
        n = sum(len(s) for _, _, s in familles) * 4
        o.append('<li><button class="r-t" aria-expanded="false">'
                 '<span class="ch">&#9656;</span>%s<span class="n">%d</span></button>'
                 % (html.escape(rayon), n))
        o.append('<ul class="f-l" hidden>')
        for famille, fslug, sous in familles:
            o.append('<li><button class="f-t" aria-expanded="false">'
                     '<span class="ch">&#9656;</span>%s</button>' % html.escape(famille))
            o.append('<ul class="s-l" hidden>')
            for sf in sous:
                o.append('<li><a href="#" data-sous="%s" data-famille="%s" data-rayon="%s">%s</a></li>'
                         % (html.escape(sf, True), html.escape(famille, True),
                            html.escape(rayon, True), html.escape(sf)))
            o.append('</ul></li>')
        o.append('</ul></li>')
    o.append('</ul>')
    return '\n'.join(o)


def page(prods):
    n_rayons = len(ARBRE)
    n_familles = sum(len(f) for _, _, f in ARBRE)
    n_sous = sum(len(s) for _, _, fam in ARBRE for _, _, s in fam)
    return """<!doctype html>
<html lang="fr"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(m)s — catalogue B2B matériel médical et hospitalier</title>
<meta name="robots" content="noindex,nofollow">
<style>%(css)s</style>
</head><body>

<div class="demo">Maquette de structure — l'arborescence est réelle
(<b>%(nr)d rayons, %(nf)d familles, %(ns)d sous-familles</b>), les articles et
les prix sont des <b>données de démonstration</b>. Le nom <b>%(m)s</b> est un
placeholder.</div>

<header><div class="hbar">
  <button class="hbtn burger" id="burger" aria-label="Catalogue">&#9776;</button>
  <div class="logo">8<span>MED</span></div>
  <form class="search" id="form" role="search">
    <input id="q" type="search" placeholder="Rechercher un produit, une marque ou une référence…"
           aria-label="Rechercher">
    <button type="submit">Rechercher</button>
  </form>
  <div class="hact">
    <button class="hbtn">Mon compte</button>
    <button class="hbtn hbtn-p" id="voirpan">Ma demande<span class="cptr" id="cptr">0</span></button>
  </div>
</div></header>

<div class="shell">
  <aside>
    %(arbre)s
    <div class="fac"><h4>Affiner</h4><div id="facettes"></div></div>
  </aside>

  <main>
    <nav class="crumb" id="crumb"></nav>
    <h1 id="h1"></h1>
    <div class="count" id="count"></div>

    <div class="qo">
      <h3>Commande rapide par référence</h3>
      <p>Pour l'acheteur qui sait déjà ce qu'il veut et ne veut pas naviguer.</p>
      <form class="qorow" id="qoform">
        <input class="r" id="qoref" placeholder="Référence, ex. EPI-GAN-042" aria-label="Référence">
        <input class="q" id="qoqte" type="number" min="1" value="1" aria-label="Quantité">
        <button type="submit">Ajouter</button>
      </form>
      <div class="qomsg" id="qomsg" role="status"></div>
    </div>

    <div class="tools">
      <label for="tri" style="font-size:13px;color:var(--mut)">Trier&nbsp;:</label>
      <select id="tri">
        <option value="pertinence">Pertinence</option>
        <option value="prix-c">Prix croissant</option>
        <option value="prix-d">Prix décroissant</option>
        <option value="nom">Désignation A→Z</option>
        <option value="ref">Référence</option>
      </select>
    </div>
    <div class="chips" id="chips"></div>
    <div class="grid" id="grid"></div>
  </main>
</div>

<div class="voile"></div>
<section class="pan" aria-label="Demande de devis">
  <div class="pan-h"><h2>Ma demande</h2><button id="ferme" aria-label="Fermer">&times;</button></div>
  <div class="pan-b" id="pan-b"></div>
  <div class="pan-f">
    <div class="tot"><span>Total HT</span><span id="tot">0,00 €</span></div>
    <p>Hors taxes et hors livraison. En B2B beaucoup d'acheteurs passent par un
       bon de commande : la demande part en devis, pas en paiement carte.</p>
    <button>Demander un devis</button>
    <button class="g">Continuer mes achats</button>
  </div>
</section>

<script>
const PRODUITS = %(prods)s;
const ARBRE = %(arbre_js)s;
const MARQUES = %(marques)s;
const FACETTES = %(facettes)s;
const ICONE = %(icone)s;
%(js)s
</script>
</body></html>""" % {
        'm': MARQUE, 'css': CSS, 'js': JS,
        'nr': n_rayons, 'nf': n_familles, 'ns': n_sous,
        'arbre': arbre_html(),
        'prods': json.dumps(prods, ensure_ascii=False),
        'arbre_js': json.dumps([[r, s, [[f, fs, ss] for f, fs, ss in fam]]
                                for r, s, fam in ARBRE], ensure_ascii=False),
        'marques': json.dumps(MARQUES, ensure_ascii=False),
        'facettes': json.dumps([[c, t, v] for c, t, v in FACETTES], ensure_ascii=False),
        'icone': json.dumps(ICONE),
    }


if __name__ == '__main__':
    prods = produits()
    with open(SORTIE, 'w', encoding='utf-8') as f:
        f.write(page(prods))
    nr = len(ARBRE)
    nf = sum(len(x) for _, _, x in ARBRE)
    ns = sum(len(s) for _, _, fam in ARBRE for _, _, s in fam)
    print('%d rayons, %d familles, %d sous-familles, %d references -> %s'
          % (nr, nf, ns, len(prods), SORTIE))
