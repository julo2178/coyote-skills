#!/usr/bin/env python3
"""
classify-csv.py : classe un export CSV de relations LinkedIn contre votre historique de carriere.

Entrees :
    --csv CONNECTIONS.CSV    Export LinkedIn (Preferences > Confidentialite des donnees >
                             Obtenir une copie de vos donnees > Relations)
    --career PARCOURS.JSON   Votre historique de carriere en JSON (schema ci-dessous)
    --output ENRICHI.CSV     Le CSV enrichi a produire

Schema du JSON de parcours :
    [
      {
        "company": "Nom de l'employeur",
        "aliases": ["Variante 1", "Variante 2"],
        "start_year": 2015,
        "end_year": 2019
      },
      ...
    ]

Le script ajoute a chaque ligne :
    - Ou on s'est connus   : l'employeur reconnu dans votre parcours, sinon "Autre"
    - Epoque               : tranche deduite de la date de mise en relation
    - Statut               : "📋 A trier" par defaut
    - Force du lien        : "🟡 Tiede" par defaut

Il ne classe PAS le type de relation, la geo ni la priorite : cela releve du jugement
humain et se remplit a la main apres import.

Utilisation :
    python classify-csv.py --csv connections.csv --career mon-parcours.json --output enrichi.csv
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from io import StringIO
from pathlib import Path


def bucket_era(connected_on: str) -> str:
    """Range une date de mise en relation dans une tranche d'epoque."""
    if not connected_on:
        return "Inconnu"
    # LinkedIn exporte generalement en "DD MMM YYYY" ou "MM/DD/YYYY".
    for fmt in ("%d %b %Y", "%m/%d/%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            dt = datetime.strptime(connected_on.strip(), fmt)
            year = dt.year
            break
        except ValueError:
            continue
    else:
        return "Inconnu"

    if year < 2010:
        return "Avant 2010"
    elif year < 2015:
        return "2010-2015"
    elif year < 2020:
        return "2015-2020"
    elif year < 2024:
        return "2020-2024"
    else:
        return "2024+"


def match_company(contact_company, career):
    """Rapproche l'employeur du contact de votre parcours (correspondance souple)."""
    if not contact_company:
        return "Autre"
    contact_lower = contact_company.lower().strip()
    for entry in career:
        canonical = entry["company"]
        candidates = [canonical] + entry.get("aliases", [])
        for candidate in candidates:
            if candidate.lower() in contact_lower or contact_lower in candidate.lower():
                return canonical
    return "Autre"


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--csv", required=True, help="Chemin du fichier Connections.csv de LinkedIn")
    parser.add_argument("--career", required=True, help="Chemin du JSON d'historique de carriere")
    parser.add_argument("--output", required=True, help="Chemin du CSV enrichi a ecrire")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    career_path = Path(args.career)
    output_path = Path(args.output)

    if not csv_path.exists():
        print(f"Erreur : {csv_path} est introuvable", file=sys.stderr)
        sys.exit(1)
    if not career_path.exists():
        print(f"Erreur : {career_path} est introuvable", file=sys.stderr)
        sys.exit(1)

    with career_path.open(encoding="utf-8") as f:
        career = json.load(f)

    # Le CSV LinkedIn commence souvent par quelques lignes de preambule avant les vrais
    # en-tetes. On cherche la ligne qui demarre par "First Name".
    with csv_path.open(encoding="utf-8") as f:
        lines = f.readlines()

    header_idx = None
    for i, line in enumerate(lines):
        if line.lower().startswith("first name") or line.lower().startswith('"first name'):
            header_idx = i
            break

    if header_idx is None:
        print("Erreur : ligne d'en-tete commencant par 'First Name' introuvable", file=sys.stderr)
        sys.exit(1)

    csv_content = "".join(lines[header_idx:])
    reader = csv.DictReader(StringIO(csv_content))

    # Les noms de colonnes exacts de LinkedIn varient legerement selon les exports.
    field_map = {}
    for col in reader.fieldnames or []:
        col_lower = col.lower().strip()
        if "first" in col_lower and "name" in col_lower:
            field_map["first_name"] = col
        elif "last" in col_lower and "name" in col_lower:
            field_map["last_name"] = col
        elif "url" in col_lower:
            field_map["url"] = col
        elif "company" in col_lower:
            field_map["company"] = col
        elif "position" in col_lower or "title" in col_lower:
            field_map["position"] = col
        elif "connected" in col_lower:
            field_map["connected_on"] = col
        elif "email" in col_lower:
            field_map["email"] = col

    if "first_name" not in field_map or "company" not in field_map:
        print(
            f"Erreur : colonnes obligatoires non detectees. Trouve : {reader.fieldnames}",
            file=sys.stderr,
        )
        sys.exit(1)

    enriched_rows = []
    counts = {"matched": 0, "other": 0, "total": 0}

    for row in reader:
        counts["total"] += 1
        first = row.get(field_map["first_name"], "")
        last = row.get(field_map["last_name"], "")
        company = row.get(field_map["company"], "")
        position = row.get(field_map.get("position", ""), "")
        url = row.get(field_map.get("url", ""), "")
        connected_on = row.get(field_map.get("connected_on", ""), "")
        email = row.get(field_map.get("email", ""), "")

        how_we_met = match_company(company, career)
        era = bucket_era(connected_on)

        if how_we_met != "Autre":
            counts["matched"] += 1
        else:
            counts["other"] += 1

        enriched_rows.append({
            "Nom": f"{first} {last}".strip(),
            "Poste actuel": position,
            "Entreprise actuelle": company,
            "URL LinkedIn": url,
            "Email": email,
            "Ou on s'est connus": how_we_met,
            "Epoque": era,
            "Son poste a l'epoque": "",
            "Type de relation": "",
            "Force du lien": "🟡 Tiede",
            "Geo": "Inconnu",
            "Relations communes": "",
            "Statut": "📋 A trier",
            "Priorite": "",
            "Dernier contact": "",
            "Date d'envoi": "",
            "Ancrage memoire": "",
            "Notes": "",
            "Relu par le coach": "false",
            "Commentaire du coach": "",
        })

    if not enriched_rows:
        print("Aucun contact trouve dans le CSV. Rien a ecrire.", file=sys.stderr)
        sys.exit(1)

    fieldnames = list(enriched_rows[0].keys())
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enriched_rows)

    print(f"\n✅ {counts['total']} contacts classes")
    print(f"   Rattaches a votre parcours : {counts['matched']}")
    print(f"   Marques 'Autre'            : {counts['other']}")
    print(f"\nFichier produit : {output_path}")
    print("\nEtapes suivantes :")
    print("  1. Importer ce CSV dans votre suivi Notion ou Airtable")
    print("  2. Repasser les entrees 'Autre' a la main (votre liste de parcours en rate toujours)")
    print("  3. Renseigner Type de relation, Force du lien, Priorite et Geo pour chaque contact")
    print("  4. Trier pour fixer le Statut (A contacter / Hors d'atteinte)")
    print("  5. Noter l'Ancrage memoire pendant le tri, tant que le souvenir est frais")


if __name__ == "__main__":
    main()
