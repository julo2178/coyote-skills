#!/usr/bin/env python3
"""
classify-csv.py — Classify a LinkedIn Connections CSV export against a user-provided career history.

Input:
    --csv CONNECTIONS.CSV    LinkedIn export (from Settings > Data Privacy > Get a copy of your data > Connections)
    --career CAREER.JSON     User's career history in JSON (see schema below)
    --output ENRICHED.CSV    Output enriched CSV with classification columns

Career JSON schema:
    [
      {
        "company": "Sky UK",
        "aliases": ["Sky", "Sky Group", "Sky Television"],
        "start_year": 2023,
        "end_year": 2026
      },
      ...
    ]

The script adds 4 columns to each row:
    - HowWeMet         — matched company from career history, or "Other"
    - Era              — bucket based on Connected On year
    - Status           — defaulted to "📋 To triage"
    - Strength         — defaulted to "🟡 Warm"

It does NOT classify Relationship type (Manager/Peer/etc.), Geo, or Priority — those require human judgement and must be set manually after import.

Usage:
    python classify-csv.py --csv connections.csv --career career.json --output enriched.csv
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path


def bucket_era(connected_on: str) -> str:
    """Bucket a 'Connected On' date string into an era."""
    if not connected_on:
        return "Unknown"
    # LinkedIn format is typically "DD MMM YYYY" or "MM/DD/YYYY"
    for fmt in ("%d %b %Y", "%m/%d/%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            dt = datetime.strptime(connected_on.strip(), fmt)
            year = dt.year
            break
        except ValueError:
            continue
    else:
        return "Unknown"

    if year < 2010:
        return "<2010"
    elif year < 2015:
        return "2010-2015"
    elif year < 2020:
        return "2015-2020"
    elif year < 2024:
        return "2020-2024"
    else:
        return "2024+"


def match_company(contact_company: str, career: list[dict]) -> str:
    """Match a contact's current company against career history (loose match)."""
    if not contact_company:
        return "Other"
    contact_lower = contact_company.lower().strip()
    for entry in career:
        canonical = entry["company"]
        candidates = [canonical] + entry.get("aliases", [])
        for candidate in candidates:
            if candidate.lower() in contact_lower or contact_lower in candidate.lower():
                return canonical
    return "Other"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--csv", required=True, help="Path to LinkedIn Connections.csv")
    parser.add_argument("--career", required=True, help="Path to career history JSON")
    parser.add_argument("--output", required=True, help="Path to write enriched CSV")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    career_path = Path(args.career)
    output_path = Path(args.output)

    if not csv_path.exists():
        print(f"Error: {csv_path} does not exist", file=sys.stderr)
        sys.exit(1)
    if not career_path.exists():
        print(f"Error: {career_path} does not exist", file=sys.stderr)
        sys.exit(1)

    with career_path.open() as f:
        career = json.load(f)

    # LinkedIn CSV often has a few header notes lines before the actual headers.
    # Find the line starting with "First Name" or similar.
    with csv_path.open(encoding="utf-8") as f:
        lines = f.readlines()

    header_idx = None
    for i, line in enumerate(lines):
        if line.lower().startswith("first name") or line.lower().startswith('"first name'):
            header_idx = i
            break

    if header_idx is None:
        print("Error: could not find header row starting with 'First Name'", file=sys.stderr)
        sys.exit(1)

    # Re-parse from the header row.
    csv_content = "".join(lines[header_idx:])
    from io import StringIO
    reader = csv.DictReader(StringIO(csv_content))

    # Detect column names (LinkedIn's exact field names vary slightly).
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
        print(f"Error: could not detect required columns. Found: {reader.fieldnames}", file=sys.stderr)
        sys.exit(1)

    enriched_rows = []
    counts = {"matched": 0, "other": 0, "total": 0}

    for row in reader:
        counts["total"] += 1
        first = row.get(field_map["first_name"], "")
        last = row.get(field_map["last_name"], "")
        company = row.get(field_map["company"], "")
        position = row.get(field_map["position"], "")
        url = row.get(field_map["url"], "")
        connected_on = row.get(field_map.get("connected_on", ""), "")
        email = row.get(field_map.get("email", ""), "")

        how_we_met = match_company(company, career)
        era = bucket_era(connected_on)

        if how_we_met != "Other":
            counts["matched"] += 1
        else:
            counts["other"] += 1

        enriched_rows.append({
            "Name": f"{first} {last}".strip(),
            "Current Role": position,
            "Current Company": company,
            "LinkedIn URL": url,
            "Email": email,
            "How we met": how_we_met,
            "Era": era,
            "Their role then": "",
            "Relationship type": "",
            "Strength": "🟡 Warm",
            "Geo": "Unknown",
            "Mutual connections": "",
            "Status": "📋 To triage",
            "Priority": "",
            "Last contact date": "",
            "DM sent date": "",
            "Notes": "",
            "Coach reviewed": "false",
            "Coach comment": "",
        })

    # Write enriched CSV.
    fieldnames = list(enriched_rows[0].keys()) if enriched_rows else []
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enriched_rows)

    print(f"\n✅ Classified {counts['total']} contacts")
    print(f"   Matched to career history:  {counts['matched']}")
    print(f"   Tagged 'Other':             {counts['other']}")
    print(f"\nOutput: {output_path}")
    print("\nNext steps:")
    print("  1. Import this CSV into your Notion / Airtable tracker")
    print("  2. Manually review 'Other' entries (some may be matches your career list missed)")
    print("  3. Set Relationship type, Strength, Priority, and Geo per contact")
    print("  4. Triage to set Status (To contact / Out of reach)")


if __name__ == "__main__":
    main()
