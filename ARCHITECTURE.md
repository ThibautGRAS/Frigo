# Guide de réplication — Feuille de route R&D en cubes 3D

Ce document récapitule le **thème**, les **briques** et la **mécanique** de l'application
(`index.html`), pour pouvoir refaire un jour une application similaire sans archéologie.
Tout tient en fichiers HTML autonomes (aucun build), three.js r161 via CDN + import map.

**Fichiers**

| Fichier | Rôle |
|---|---|
| `index.html` | L'application : monolithe 3×4×5, tranches, fiches, liquides, présentation |
| `liquid_splash.html` | Démo fluide « réel » : MLS-MPM WebGPU 185 k particules dans un cube |
| `liquid_test.html` | Version WebGL de repli du fluide (SPH CPU + SSFR) |
| `donnees.json` / `generer_donnees.py` | Source des contenus |

La version applicative est dans `window.__APP_VERSION` (affichée par le loader via
`#loaderVer`) — **incrémentée à chaque lot de modifications, commit préfixé `vX.Y:`,
push sur `origin main`** (permet de vérifier le cache sur iPad/iPhone).

---

## 1. Thème visuel

**Fond clair institutionnel** (pas de dark mode) :

| Élément | Valeur |
|---|---|
| Fond page | `linear-gradient(175deg, #F2F6FC → #E6EEF8 → #D8E4F2 → #CDD9ED)` + voile radial blanc + micro-grille de points `rgba(60,100,180,.06)` + vignette |
| Encre | navy `#0B1F4E` (`--ink`), atténuée `#4A5F86`, effacée `#8496B5` |
| Accent | rouge CETIM `#EF3346` (`--red`) — réservé au stratégique |
| Bleu cube | `#3E7BD8` (GLASS), variante claire `#4C8BEC` (GLASS_S) |
| Typo | Montserrat (titres/étiquettes, `.sg`), Inter/system (corps) |
| Panneaux | verre dépoli blanc `rgba(255,255,255,.82)` + `backdrop-filter: blur(18px)` — **jamais sur des éléments au-dessus du canvas animé** (voir Pièges) |

Rendu : `WebGLRenderer` alpha, ACESFilmic exposure 1.15, fog `0xDDE8F4`,
EffectComposer avec cible MSAA 4× + UnrealBloom très discret (strength .18, threshold .9),
environnement PMREM généré d'un canvas dégradé bleu nuit + rectangles lumineux.
Lumières : ambiante blanche .85, key directionnelle `#CCDEFF`, rim bleue, « glint »
balayante animée, point light rouge de sélection (intensité 1.6 quand fiche ouverte).

---

## 2. Modèle de données

Grille conceptuelle **X × Y × Z = 3 axes × 4 leviers × 5 domaines** :

- `AXES` (A1 Sources & transferts, A2 Diagnostic & instrum., A3 Réduction & intégr.)
  et `LEVIERS` (L1 Essais–simulation, L2 IA, L3 Psychoacoustique, L4 Standardisation) :
  `{id, name, short, desc, dev[]}`.
- `DOMAINS` (D1…D5) : `{id, name, sub, obj, sys, moyen, solu, proj[]}` — les champs
  lexicaux (`obj/sys/moyen/solu`) servent à générer des descriptions croisées.
- `CELLS` : dictionnaire `"d-a-l" → {d,a,l, title, essential, trl, desc, links[], li[]}`.
  Un croisement absent = **cube fantôme** transparent (la grille reste lisible).
  `essential` = brique stratégique → rouge.

---

## 3. La scène : monolithe de glaçons

**Structure** : `root` (Group, rotation globale) → 5 `domainGroups` (translation Z
animée par tranche) → 60 cubes (`cellMeshes`, RoundedBox maison rayon 0.12,
`BOX=0.9`, pas `S=1.16`).

**Matériau « verre cristal »** (MeshPhysicalMaterial, présents uniquement) :

```js
color:#3E7BD8, roughness:.05, normalMap:iceNormal(.3), transparent, opacity:.94,
transmission:.9, ior:1.5, thickness:.55,
attenuationColor:#E6EFFA (quasi neutre!), attenuationDistance:3,
clearcoat:1, clearcoatRoughness:.04, envMapIntensity:1, emissive:#1E4296
```

- `iceNormal` : carte de normales procédurale (bosses radiales + fissures, Sobel sur
  canvas 256²) → distorsion réfractive « glaçon ».
- Pas de cages filaires ni cadre global : l'arête vient du biseau + clearcoat.
- Chaque présent porte 2 sprites additifs de **lueur interne** (`glow`, `glow2`)
  qui *reflètent la couleur du liquide* quand le cube en contient (lerp vers
  `uColor` ∝ remplissage, opacité +agitation).
- Étiquettes = sprites canvas (`makeAxisLabel` : id 68 px + nom 40 px) recto/verso,
  visibilité par face selon l'angle caméra. Tranche ouverte : mêmes intitulés,
  taille .29, quinconce A2 +0.88, leviers décalés à x = −(largeur/2 + 1.25).

---

## 4. Le liquide des cubes (0 particule — illusion shader)

Chaque cube présent contient une **boîte opaque** (`BoxGeometry` 0.78·BOX) en
`ShaderMaterial` DoubleSide :

- **Volume** : `discard` de tout fragment au-dessus d'un plan de surface ;
  les **faces arrière** visibles sous le plan = la surface du liquide
  (`gl_FrontFacing` distingue paroi/surface).
- **Plan horizontal monde** : normale `N = normalize(uWob.x, 1, uWob.y)` ;
  niveau `lvl=(uFill·2−1)·uHalfY` où `uHalfY` = demi-hauteur *monde* de la boîte
  tournée `(CB/2)(|e1|+|e5|+|e9|)` → tourner le cube fait bouger l'eau (gravité).
- **Vagues anti-moiré** : 2 sinusoïdes lentes + clapot, toutes sur des
  **directions obliques** ((.80,.60), (−.55,.83), (.30,−.95)) — jamais alignées
  aux axes, fréquences 14/11 (clapot 26/22). La normale de surface est le **vrai
  gradient** de la fonction de hauteur. Spéculaire pow 48.
- **Habillage** : paroi assombrie en profondeur + fresnel ; surface +16 % avec
  reflets soleil ; **ligne d'eau lumineuse** (smoothstep près de s=0) ; **écume**
  blanche ∝ agitation.

**Ressort de ballottement** (par cube — jamais à l'unisson) :

```
consigne  d = clamp(−(rotV+gyro)·9) + accelTranche·(axeZ monde)·0.008 [+ bercement rouges]
intégr.   wv += (d − wob)·k·dt ;  wv ·= exp(−dp·visc·dt) ;  wob += wv·dt
k = 23+rand·10   dp = rouges .55–.93 / bleus 1.0–1.5   visc globale = 3
```

- **Rouges = sujets vivants** : bercement continu (2 sinus lents déphasés ±4°),
  plancher d'agitation qui respire (.09–.16), surge aléatoire toutes les 4–10 s
  (agit ≥ .30–.45), premier tirage aléatoire ⇒ désynchronisés.
- **Agitation (`uAgit`)** : max(vitesse rotation − .03)·16, |accel tranche|·.014,
  pulses rouges — retombée `exp(−1.9 t)`. Elle amplifie vagues, clapot, écume,
  ligne d'eau, spéculaire.
- **Remplissage** : cible = niveau aléatoire (.28–.74) si domaine ouvert, 0 sinon ;
  montée ~1 s, **vidange 3× plus rapide** (`dt·1.8`).
- Couleurs : `#E8354A` (essentielles) / `#2F80E8` — la teinte du cube, jamais un
  mélange.

**Couplage au déploiement** : à chaque frame, vitesse & accélération du glissement
de chaque tranche (dérivées lissées de `anim.z`) → projetées sur l'axe Z monde
(`e8,e10` de `root.matrixWorld`) → consigne du ressort. Trajet fixe (1250 ms easeIO)
⇒ une tranche qui vient de loin accélère plus ⇒ ballotte plus. Gain `.008`.

---

## 5. Interactions & caméra

- **Drag** : rotation directe (`dx·0.005`), **vitesse d'inertie mesurée par frame**
  pendant le drag (EMA .35/.65 des deltas réels) → relâchement sans à-coup ;
  décroissance ·0.94. Oscillation de repos re-synchronisée en permanence
  (sinon saut à la reprise).
- **Gyroscope (iPhone/iPad)** : permission au premier toucher ; beta/gamma →
  offsets cibles clampés ±.12/±.15 rad autour d'un **neutre auto-adaptatif**
  (baseline low-pass .004) ; appliqués en deltas lissés ; leurs vitesses
  alimentent le slosh comme la souris.
- **Caméra** : fov 26, distance 10–30 (molette/pincer), cible
  `camTgt=(0, CTY=0.5, 0)` — cible rehaussée = cube plus bas à l'écran, noms
  d'axes dégagés. Fiche ouverte : décalage **horizontal** (PC, facteur .34) ou
  **vertical** (téléphone portrait, tiroir bas) de scène, lissés.
- **Tranches** : `openSlice(di)` → tranche à `z = front + OUT(3.4)`, résidu
  reculé à −1.35, recadrage `camTgt.x=−1.75`, **fiche domaine à droite dans tous
  les cas** (PC ; pas sur ≤760 px), remplissage des liquides.
  `closeSliceNow()` : **séquencé** — 1) `openDom=−1` ⇒ vidange rapide + retour
  couleurs, 2) après 460 ms seulement, rangement des groupes (annulé si réouvert).
- **Tweens maison** (`tw`) : un seul tween par objet (le nouveau remplace
  l'ancien) — transitions continues quand on enchaîne les domaines.

---

## 6. États de mise en avant (`setTargets`)

Cibles par cube (`tgt`) lissées dans la boucle : `opacity, emissiveI, scale, edge,
red, glow, info, dense`.

- **`red`** = bascule de TEINTE (verre/émissif/lueur lerpés vers le rouge) ;
  **`dense`** = bascule d'OPACITÉ (transmission → ~.16) — **séparés** : un bleu
  sélectionné devient bleu franc, pas violacé.
- **Règle anti-violet** : la teinte ne fait JAMAIS de moyenne bleu↔rouge — un cube
  estompé garde `red` entier, seules opacité/lueur baissent.
- Sélection de cellule : sélection dense+brillante (envMap +.55, clearcoat +.3,
  lampe rouge 1.6), liées à 68 %, autres à 10 %.
- Sélection axe/levier : **tous** les cubes associés en rouge (pas que les
  essentielles), les autres fantômes.
- Tranche ouverte : essentielles rouges denses, secondaires bleues translucides,
  transmission maintenue haute (réduction ·.25 seulement) pour voir le liquide.

---

## 7. Mode Présentation

Ouverture sobre : recul caméra + balayage ±0.4 rad (PAS de 360°). Puis :
axes (fiche + tous les cubes rouges) → leviers → **domaines réellement déployés**
(openSlice, liquides, 5.4 s chacun) → rangement final. Interruptible par tout
pointerdown / bouton. Timers via `pWait` (annulés par `stopPres`).

---

## 8. Adaptations par appareil & performance

| Aspect | PC | iPad | iPhone (<560 px) |
|---|---|---|---|
| Aide / gestes | vocabulaire souris, **aucun bandeau/toast** | tactile + toast | tactile + toast |
| Fiche | panneau droit 430 px + décalage H | idem | **tiroir bas 46 vh** + recadrage V + rail estompé (`body.cardopen`) |
| Fiche domaine auto | oui | oui | non (vue dégagée) |
| Rail | vertical gauche, **sans backdrop-filter** | pilules bas | pilules bas |
| liquid_splash | grille 60³ (185 k ptcl), filtre 40, thickness pleine res | 40³, filtre 24, ½ res | 34³ |

Garde-fous : boucle mesure les fps (EMA) ; si <34 après 6 s →
`PERF.degraded` : transmission coupée (verre simple) + verre allégé sur tranche
ouverte pour garder les liquides visibles. `liquid_splash` a sa résolution
dynamique (plafond de pixels ·0.72 si <42 fps).

---

## 9. `liquid_splash.html` en bref (fluide à particules)

Portage WebGPU de « Splash » (matsuoka-601, MIT) :
- **Sim MLS-MPM** : 5 kernels (clearGrid → p2g_1 → p2g_2 → updateGrid → g2p),
  atomics en virgule fixe (×1e7), stiffness 50, restDensity 3, viscosité .3
  + amortissement grille .995, dt .22 ×2 sous-pas, gravité tournée en repère cube.
- **Rendu SSFR** : depth billboards → narrow-range filter (2×1D + 2D) →
  thickness (+blur gaussien) → composite : normales depth, Beer-Lambert,
  Fresnel, cubemap procédurale, réfraction du fond par point de sortie.
- Habillage : cavité 86 % avec fond de verre épais, cœur lumineux, arêtes rubans,
  thèmes clair/sombre, gyro. Params : `?g=`, `?theme=dark`, `?pal=0..3`, `?kick=1`.

---

## 10. Pièges rencontrés (à ne pas repayer)

1. **`backdrop-filter` sur des boutons au-dessus d'un canvas animé** → repaints
   coûteux, clics saccadés. Rail sans flou + `transition` limitée aux couleurs.
2. **Transmission three.js** : les objets transparents ne sont PAS dans le buffer
   de transmission (on voit le fond à travers un cube, pas ses voisins
   transparents) ; les objets opaques y sont (le liquide se voit à travers son
   verre ✔). Passer de `transmission>0` à `0` recompile le shader → garder un
   plancher (.05) pour animer.
3. **`attenuationColor` teinte TOUT le transmis** : bleutée + liquide rouge =
   violet. La garder quasi neutre, la couleur vient de `material.color`.
4. **Mélanges de teinte** : tout lerp partiel bleu↔rouge fabrique du violet —
   n'atténuer que l'intensité, jamais la teinte.
5. **Moiré des vagues procédurales** : des sinus alignés aux axes + spéculaire
   étroit = quadrillage scintillant. Directions obliques, fréquences basses,
   normale = vrai gradient, spéculaire large.
6. **Inertie de drag** : reprendre la vitesse du dernier événement souris ≠
   vitesse réelle par frame → à-coup au relâchement. Mesurer le delta de rotation
   par frame pendant le drag.
7. **Deux tweens sur le même objet** = lutte silencieuse ; dédupliquer par objet.
8. **iOS** : gyroscope = `DeviceOrientationEvent.requestPermission()` dans un
   geste utilisateur obligatoire.

## 11. Outillage de dev (sans node sur le poste)

Test/erreurs/captures via Chrome headless :

```
chrome --headless=new [--enable-unsafe-webgpu --use-angle=d3d11]
  --enable-logging=stderr --v=0 --virtual-time-budget=12000
  --screenshot=out.png "file:///…/index.html?dom=1"
```

`INFO:CONSOLE` remonte erreurs WGSL/JS. Limite : les pages CDN+WebGL gèlent la
capture en plein boot (rendu logiciel) — fiable pour les erreurs et le premier
rendu, pas pour les états animés finaux (vérifier sur machine réelle).
Deep-links de test : `index.html?dom=N`, `liquid_splash.html?kick=1&pal=2`.
