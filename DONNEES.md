# Feuille de route R&D — Acoustique & Vibrations (CETIM)

> Fichier de référence structuré. Éditez librement le texte ci-dessous ; le bloc JSON en fin de fichier est la source réimportable par l'application.


## 1. Axes stratégiques (X)

### A1 — Sources & transferts

Comprendre, caractériser et hiérarchiser les excitations vibratoires, acoustiques et fluidiques ainsi que leurs voies de transfert, avec une attention portée aux systèmes électrifiés.


**Thèmes de développement :**
- Caractériser les sources solidiennes, fluidiques et acoustiques (calcul + essais)
- Valider les composants et renforcer la corrélation essais/simulations
- Relier sources, transferts et comportement global après intégration

### A2 — Diagnostic & instrumentation

Développer des moyens avancés de mesure, d'imagerie, de localisation et d'aide au diagnostic pour objectiver plus finement les phénomènes.


**Thèmes de développement :**
- Mesures multi-capteurs et instrumentation innovante (antennes, MEMS, PVDF, fibres)
- Imagerie acoustique et localisation de sources en milieu industriel
- Traitement, automatisation et IA ciblée pour l'aide au diagnostic

### A3 — Réduction & intégration

Concevoir, tester et évaluer des solutions de réduction adaptées aux nouvelles contraintes industrielles : isolateurs, composants passifs, silencieux, métamatériaux, intégrations compactes.


**Thèmes de développement :**
- Solutions passives : sélection, conception, dimensionnement et validation
- Démarches intégrées du diagnostic à la mise en œuvre
- Concepts exploratoires (métamatériaux, contrôle actif) avec go/no-go


## 2. Leviers transverses (Y)

### L1 — Essais–simulation & recalage

Mieux articuler expériences et modèles pour améliorer la compréhension des systèmes, la validation des hypothèses et la fiabilité des analyses.


**Thèmes de développement :**
- Articuler essais, modélisation et recalage sur les cas de l'équipe
- Validation croisée mesures / modèles
- Modèles simplifiés ou réduits pour accélérer l'analyse

### L2 — IA & automatisation

Mieux exploiter les données d'essais et de mesure : automatisation, traitement, aide à l'analyse et, lorsque pertinent, approches IA.


**Thèmes de développement :**
- Automatiser pré-traitement, analyse et extraction d'indicateurs
- Outils de tri, d'estimation et d'aide à l'analyse
- Accélérer l'analyse et fiabiliser la reproductibilité

### L3 — Psychoacoustique

Compléter les approches classiques par des évaluations perceptives et des indicateurs adaptés, lorsque la gêne ou la qualité perçue deviennent déterminantes.


**Thèmes de développement :**
- Exploiter les moyens d'écoute (salle jury, écoutes comparatives)
- Enrichir diagnostic et hiérarchisation par la perception
- Évaluer l'intérêt réel des solutions au-delà des niveaux énergétiques

### L4 — Standardisation & capitalisation

Renforcer robustesse, réutilisation et capitalisation par une meilleure structuration des données, scripts, méthodes et livrables.


**Thèmes de développement :**
- Harmoniser formats de données et structures de livrables
- Structurer scripts et chaînes d'analyse réutilisables
- Formaliser méthodes et cas de référence


## 3. Domaines scientifiques (Z)

### D1 — Hydroacoustique

_Pulsations · composants fluidiques_

- **Objet :** pulsations de pression
- **Systèmes :** circuits et composants fluidiques
- **Moyens :** mesures de pression dynamique embarquées
- **Solutions :** silencieux, résonateurs et composants passifs
- **Projets phares :** PSS H2FLU, LEDITH, Banc pulsations Senlis

### D2 — Machines tournantes

_Ordres · transmissions · équilibrage_

- **Objet :** ordres, harmoniques et balourds
- **Systèmes :** machines tournantes et transmissions
- **Moyens :** accélérométrie synchrone et voies codeur
- **Solutions :** équilibrage, découplage et amortissement ciblé
- **Projets phares :** PTT VIBRAC, TRANSMECA, Prestations diagnostic

### D3 — Bruit solidien

_Efforts bloqués · voies de transfert_

- **Objet :** efforts dynamiques et voies de transfert
- **Systèmes :** assemblages et structures industrielles
- **Moyens :** TPA, sous-structuration et efforts bloqués
- **Solutions :** plots, isolateurs et traitements structuraux
- **Projets phares :** PTT VIBRAC, PTT EPROM, Cas SNOP

### D4 — Imagerie acoustique

_Antennes · localisation · rayonné_

- **Objet :** cartographies et rayonnement acoustique
- **Systèmes :** machines en environnement industriel réel
- **Moyens :** antennes, réseaux MEMS et capteurs non intrusifs
- **Solutions :** traitement d'antenne et hiérarchisation de sources
- **Projets phares :** Outils ISO 3744 AR, Antennerie 3D, PSS INSTRUM

### D5 — Systèmes électrifiés

_Tonal · HF · e-mobility_

- **Objet :** composantes tonales et haute fréquence
- **Systèmes :** chaînes de traction et auxiliaires électrifiés
- **Moyens :** essais e-mobility multiphysiques
- **Solutions :** découplage et absorption adaptés aux excitations HF
- **Projets phares :** Labo commun CREM, VACOUVE, PTT COMPELEC


## 4. Matrice domaine × axe × levier

Pour chaque domaine, briques retenues (● essentielle, ○ secondaire) :

### D1 — Hydroacoustique

| | A1 | A2 | A3 |
|---|---|---|---|
| **L1** | ● | ○ | ● |
| **L2** | · | · | ○ |
| **L3** | · | · | ● |
| **L4** | ● | ○ | · |

### D2 — Machines tournantes

| | A1 | A2 | A3 |
|---|---|---|---|
| **L1** | ● | ○ | ● |
| **L2** | ○ | ● | ○ |
| **L3** | · | · | · |
| **L4** | · | ● | · |

### D3 — Bruit solidien

| | A1 | A2 | A3 |
|---|---|---|---|
| **L1** | ● | ● | ● |
| **L2** | · | ○ | · |
| **L3** | · | · | ○ |
| **L4** | ● | ○ | · |

### D4 — Imagerie acoustique

| | A1 | A2 | A3 |
|---|---|---|---|
| **L1** | ○ | ● | ○ |
| **L2** | · | ● | · |
| **L3** | · | ● | · |
| **L4** | ○ | ● | · |

### D5 — Systèmes électrifiés

| | A1 | A2 | A3 |
|---|---|---|---|
| **L1** | ● | · | ● |
| **L2** | · | ● | · |
| **L3** | · | ● | ○ |
| **L4** | ● | ○ | · |


---

## Source machine (ne pas éditer à la main de préférence)

```json
{
 "AXES": [
  {
   "id": "A1",
   "short": "Axe 1",
   "name": "Sources & transferts",
   "glyph": "≋",
   "desc": "Comprendre, caractériser et hiérarchiser les excitations vibratoires, acoustiques et fluidiques ainsi que leurs voies de transfert, avec une attention portée aux systèmes électrifiés.",
   "dev": [
    "Caractériser les sources solidiennes, fluidiques et acoustiques (calcul + essais)",
    "Valider les composants et renforcer la corrélation essais/simulations",
    "Relier sources, transferts et comportement global après intégration"
   ]
  },
  {
   "id": "A2",
   "short": "Axe 2",
   "name": "Diagnostic & instrumentation",
   "glyph": "⌖",
   "desc": "Développer des moyens avancés de mesure, d'imagerie, de localisation et d'aide au diagnostic pour objectiver plus finement les phénomènes.",
   "dev": [
    "Mesures multi-capteurs et instrumentation innovante (antennes, MEMS, PVDF, fibres)",
    "Imagerie acoustique et localisation de sources en milieu industriel",
    "Traitement, automatisation et IA ciblée pour l'aide au diagnostic"
   ]
  },
  {
   "id": "A3",
   "short": "Axe 3",
   "name": "Réduction & intégration",
   "glyph": "▣",
   "desc": "Concevoir, tester et évaluer des solutions de réduction adaptées aux nouvelles contraintes industrielles : isolateurs, composants passifs, silencieux, métamatériaux, intégrations compactes.",
   "dev": [
    "Solutions passives : sélection, conception, dimensionnement et validation",
    "Démarches intégrées du diagnostic à la mise en œuvre",
    "Concepts exploratoires (métamatériaux, contrôle actif) avec go/no-go"
   ]
  }
 ],
 "LEVIERS": [
  {
   "id": "L1",
   "name": "Essais–simulation & recalage",
   "desc": "Mieux articuler expériences et modèles pour améliorer la compréhension des systèmes, la validation des hypothèses et la fiabilité des analyses.",
   "dev": [
    "Articuler essais, modélisation et recalage sur les cas de l'équipe",
    "Validation croisée mesures / modèles",
    "Modèles simplifiés ou réduits pour accélérer l'analyse"
   ]
  },
  {
   "id": "L2",
   "name": "IA & automatisation",
   "desc": "Mieux exploiter les données d'essais et de mesure : automatisation, traitement, aide à l'analyse et, lorsque pertinent, approches IA.",
   "dev": [
    "Automatiser pré-traitement, analyse et extraction d'indicateurs",
    "Outils de tri, d'estimation et d'aide à l'analyse",
    "Accélérer l'analyse et fiabiliser la reproductibilité"
   ]
  },
  {
   "id": "L3",
   "name": "Psychoacoustique",
   "desc": "Compléter les approches classiques par des évaluations perceptives et des indicateurs adaptés, lorsque la gêne ou la qualité perçue deviennent déterminantes.",
   "dev": [
    "Exploiter les moyens d'écoute (salle jury, écoutes comparatives)",
    "Enrichir diagnostic et hiérarchisation par la perception",
    "Évaluer l'intérêt réel des solutions au-delà des niveaux énergétiques"
   ]
  },
  {
   "id": "L4",
   "name": "Standardisation & capitalisation",
   "desc": "Renforcer robustesse, réutilisation et capitalisation par une meilleure structuration des données, scripts, méthodes et livrables.",
   "dev": [
    "Harmoniser formats de données et structures de livrables",
    "Structurer scripts et chaînes d'analyse réutilisables",
    "Formaliser méthodes et cas de référence"
   ]
  }
 ],
 "DOMAINS": [
  {
   "id": "D1",
   "name": "Hydroacoustique",
   "sub": "Pulsations · composants fluidiques",
   "obj": "pulsations de pression",
   "sys": "circuits et composants fluidiques",
   "moyen": "mesures de pression dynamique embarquées",
   "solu": "silencieux, résonateurs et composants passifs",
   "proj": [
    "PSS H2FLU",
    "LEDITH",
    "Banc pulsations Senlis"
   ]
  },
  {
   "id": "D2",
   "name": "Machines tournantes",
   "sub": "Ordres · transmissions · équilibrage",
   "obj": "ordres, harmoniques et balourds",
   "sys": "machines tournantes et transmissions",
   "moyen": "accélérométrie synchrone et voies codeur",
   "solu": "équilibrage, découplage et amortissement ciblé",
   "proj": [
    "PTT VIBRAC",
    "TRANSMECA",
    "Prestations diagnostic"
   ]
  },
  {
   "id": "D3",
   "name": "Bruit solidien",
   "sub": "Efforts bloqués · voies de transfert",
   "obj": "efforts dynamiques et voies de transfert",
   "sys": "assemblages et structures industrielles",
   "moyen": "TPA, sous-structuration et efforts bloqués",
   "solu": "plots, isolateurs et traitements structuraux",
   "proj": [
    "PTT VIBRAC",
    "PTT EPROM",
    "Cas SNOP"
   ]
  },
  {
   "id": "D4",
   "name": "Imagerie acoustique",
   "sub": "Antennes · localisation · rayonné",
   "obj": "cartographies et rayonnement acoustique",
   "sys": "machines en environnement industriel réel",
   "moyen": "antennes, réseaux MEMS et capteurs non intrusifs",
   "solu": "traitement d'antenne et hiérarchisation de sources",
   "proj": [
    "Outils ISO 3744 AR",
    "Antennerie 3D",
    "PSS INSTRUM"
   ]
  },
  {
   "id": "D5",
   "name": "Systèmes électrifiés",
   "sub": "Tonal · HF · e-mobility",
   "obj": "composantes tonales et haute fréquence",
   "sys": "chaînes de traction et auxiliaires électrifiés",
   "moyen": "essais e-mobility multiphysiques",
   "solu": "découplage et absorption adaptés aux excitations HF",
   "proj": [
    "Labo commun CREM",
    "VACOUVE",
    "PTT COMPELEC"
   ]
  }
 ],
 "STRATEGIC": {
  "D1": [
   "A1-L1",
   "A1-L4",
   "A3-L1",
   "A3-L3"
  ],
  "D2": [
   "A1-L1",
   "A2-L2",
   "A2-L4",
   "A3-L1"
  ],
  "D3": [
   "A1-L1",
   "A1-L4",
   "A2-L1",
   "A3-L1"
  ],
  "D4": [
   "A2-L1",
   "A2-L2",
   "A2-L3",
   "A2-L4"
  ],
  "D5": [
   "A1-L1",
   "A1-L4",
   "A2-L2",
   "A2-L3",
   "A3-L1"
  ]
 },
 "SECONDARY": {
  "D1": [
   "A2-L1",
   "A2-L4",
   "A3-L2"
  ],
  "D2": [
   "A1-L2",
   "A2-L1",
   "A3-L2"
  ],
  "D3": [
   "A2-L2",
   "A2-L4",
   "A3-L3"
  ],
  "D4": [
   "A1-L1",
   "A1-L4",
   "A3-L1"
  ],
  "D5": [
   "A2-L4",
   "A3-L3"
  ]
 }
}
```
