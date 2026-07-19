#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generer_donnees.py — Génère DONNEES.md (lisible) et donnees.json (pour l'app)
à partir d'une source structurée : soit un JSON déjà extrait, soit un PDF.

USAGE
-----
  # À partir du JSON de référence (export courant de l'app) :
  python3 generer_donnees.py --json donnees_export.json

  # À partir d'un PDF (extraction heuristique, à relire ensuite) :
  python3 generer_donnees.py --pdf FEUILLE_DE_ROUTE.pdf

  # Choisir les fichiers de sortie :
  python3 generer_donnees.py --json donnees_export.json --md DONNEES.md --out donnees.json

Le MD produit est structuré par AXES, LEVIERS, DOMAINES, puis la matrice
domaine × axe × levier (briques essentielles / secondaires). Il sert de
référence humaine ET de source réimportable (le bloc JSON est inclus en fin).
"""
import argparse, json, sys, re, os

# ─────────────────────────── Extraction PDF ───────────────────────────
def extraire_pdf(path):
    """Extraction heuristique depuis un PDF de feuille de route.
    Renvoie un dict partiel {AXES, LEVIERS, DOMAINS, STRATEGIC, SECONDARY}.
    L'extraction automatique d'un PDF libre est imparfaite : le résultat
    est un SQUELETTE à relire et compléter à la main dans le MD."""
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            sys.exit("Installez pypdf : pip install pypdf --break-system-packages")
    reader = PdfReader(path)
    texte = "\n".join((p.extract_text() or "") for p in reader.pages)

    def cherche(motifs):
        for m in motifs:
            r = re.search(m, texte, re.I)
            if r:
                return r.group(1).strip()
        return ""

    # Repère les intitulés d'axes / leviers / domaines par mots-clés usuels.
    axes = re.findall(r'\bA([123])\b[\s:.\-]+([^\n]{4,60})', texte)
    leviers = re.findall(r'\bL([1234])\b[\s:.\-]+([^\n]{4,60})', texte)
    domaines = re.findall(r'\bD([12345])\b[\s:.\-]+([^\n]{4,60})', texte)

    def dedup(pairs, prefix):
        vus = {}
        for num, lib in pairs:
            k = f"{prefix}{num}"
            if k not in vus:
                vus[k] = re.sub(r'\s+', ' ', lib).strip(' .:-')
        return vus

    A = dedup(axes, "A"); L = dedup(leviers, "L"); D = dedup(domaines, "D")

    skel = {
        "AXES":    [{"id": f"A{i}", "name": A.get(f"A{i}", f"Axe {i}"),
                     "short": f"Axe {i}", "desc": "", "dev": []} for i in (1, 2, 3)],
        "LEVIERS": [{"id": f"L{i}", "name": L.get(f"L{i}", f"Levier {i}"),
                     "desc": "", "dev": []} for i in (1, 2, 3, 4)],
        "DOMAINS": [{"id": f"D{i}", "name": D.get(f"D{i}", f"Domaine {i}"),
                     "sub": "", "obj": "", "sys": "", "moyen": "", "solu": "",
                     "proj": []} for i in (1, 2, 3, 4, 5)],
        "STRATEGIC": {}, "SECONDARY": {},
        "_note": "SQUELETTE extrait du PDF — à compléter (desc, dev, vocabulaire, "
                 "briques essentielles/secondaires) dans DONNEES.md puis réimporter."
    }
    return skel

# ─────────────────────────── Génération MD ───────────────────────────
def bloc_liste(items):
    return "\n".join(f"- {x}" for x in items) if items else "- _(à compléter)_"

def generer_md(d):
    A, L, D = d["AXES"], d["LEVIERS"], d["DOMAINS"]
    STR, SEC = d.get("STRATEGIC", {}), d.get("SECONDARY", {})
    out = []
    out.append("# Feuille de route R&D — Acoustique & Vibrations (CETIM)\n")
    out.append("> Fichier de référence structuré. Éditez librement le texte ci-dessous ; "
               "le bloc JSON en fin de fichier est la source réimportable par l'application.\n")
    out.append("\n## 1. Axes stratégiques (X)\n")
    for a in A:
        out.append(f"### {a['id']} — {a.get('name','')}")
        if a.get("desc"): out.append(f"\n{a['desc']}\n")
        out.append("\n**Thèmes de développement :**")
        out.append(bloc_liste(a.get("dev", [])))
        out.append("")
    out.append("\n## 2. Leviers transverses (Y)\n")
    for l in L:
        out.append(f"### {l['id']} — {l.get('name','')}")
        if l.get("desc"): out.append(f"\n{l['desc']}\n")
        out.append("\n**Thèmes de développement :**")
        out.append(bloc_liste(l.get("dev", [])))
        out.append("")
    out.append("\n## 3. Domaines scientifiques (Z)\n")
    for dom in D:
        out.append(f"### {dom['id']} — {dom.get('name','')}")
        if dom.get("sub"): out.append(f"\n_{dom['sub']}_\n")
        champs = [("Objet", dom.get("obj")), ("Systèmes", dom.get("sys")),
                  ("Moyens", dom.get("moyen")), ("Solutions", dom.get("solu"))]
        for lib, val in champs:
            if val: out.append(f"- **{lib} :** {val}")
        if dom.get("proj"):
            out.append(f"- **Projets phares :** {', '.join(dom['proj'])}")
        out.append("")
    # Matrice
    out.append("\n## 4. Matrice domaine × axe × levier\n")
    out.append("Pour chaque domaine, briques retenues (● essentielle, ○ secondaire) :\n")
    for dom in D:
        did = dom["id"]
        out.append(f"### {did} — {dom.get('name','')}")
        ess = set(STR.get(did, [])); sec = set(SEC.get(did, []))
        if not ess and not sec:
            out.append("_(aucune brique renseignée)_\n"); continue
        out.append("\n| | " + " | ".join(a["id"] for a in A) + " |")
        out.append("|---|" + "---|" * len(A))
        for l in L:
            row = [f"**{l['id']}**"]
            for a in A:
                k = f"{a['id']}-{l['id']}"
                row.append("●" if k in ess else ("○" if k in sec else "·"))
            out.append("| " + " | ".join(row) + " |")
        out.append("")
    # Bloc JSON réimportable
    out.append("\n---\n\n## Source machine (ne pas éditer à la main de préférence)\n")
    out.append("```json")
    out.append(json.dumps({k: d[k] for k in
               ("AXES", "LEVIERS", "DOMAINS", "STRATEGIC", "SECONDARY") if k in d},
               ensure_ascii=False, indent=1))
    out.append("```")
    return "\n".join(out) + "\n"

# ─────────────────────────── Main ───────────────────────────
def main():
    ap = argparse.ArgumentParser(description="Génère DONNEES.md et donnees.json")
    ap.add_argument("--json", help="Source JSON déjà structurée")
    ap.add_argument("--pdf", help="Source PDF (extraction heuristique)")
    ap.add_argument("--md", default="DONNEES.md", help="Fichier Markdown de sortie")
    ap.add_argument("--out", default="donnees.json", help="Fichier JSON de sortie")
    args = ap.parse_args()

    if args.json:
        d = json.load(open(args.json, encoding="utf-8"))
    elif args.pdf:
        d = extraire_pdf(args.pdf)
        print("⚠ Extraction PDF = squelette. Relisez et complétez DONNEES.md, "
              "puis réimportez avec --json.")
    else:
        ap.error("Fournir --json ou --pdf")

    # Normalise : garde uniquement les clés attendues pour le JSON app
    cle_app = {k: d[k] for k in
               ("AXES", "LEVIERS", "DOMAINS", "STRATEGIC", "SECONDARY") if k in d}
    open(args.out, "w", encoding="utf-8").write(
        json.dumps(cle_app, ensure_ascii=False, indent=1))
    open(args.md, "w", encoding="utf-8").write(generer_md(d))
    print(f"✓ Écrit {args.md} et {args.out}")

if __name__ == "__main__":
    main()
