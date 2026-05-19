# Network Reactivation — Claude Skill

A system for reconnecting with dormant warm relationships in a way that builds long-term capital instead of burning it.

## What's in the box

```
network-reactivation/
├── SKILL.md                          The main skill file (Claude reads this)
├── templates/
│   └── dm-templates.md              5 archetypes × EN+FR + reply-handling
├── references/
│   ├── notion-template.md           Database schema and recommended views
│   └── anti-patterns.md             What kills warm DMs, with examples
└── scripts/
    ├── classify-csv.py              Bulk-classify a LinkedIn CSV export
    └── career.example.json          Example career history for the classifier
```

## How to install

### Option 1 — Install in Claude.ai or Claude Code

1. Download the `.skill` file (zipped folder of this repo)
2. Upload to Claude.ai (Settings → Skills) or place in your Claude Code skills directory
3. Trigger by saying anything like "help me reconnect with my old network", "I want to reactivate my LinkedIn contacts", or "draft a DM to an ex-manager I haven't spoken to in 5 years"

### Option 2 — Use the methodology directly

The skill is fully readable. Open `SKILL.md` and follow the 7-phase workflow even without Claude. The templates and anti-patterns work standalone.

## The core principle

**Reconnect first. Intent comes later.**

Every opener is purely relational. Zero mention of jobs, projects, products, or asks. The relationship is re-established before anything else is ever raised. This is what separates this approach from spammy reach-out templates.

## The 5 archetypes

People relate to you differently based on the original power dynamic:

1. **Ex-manager** — respectful, anchored in a specific moment they led or taught
2. **Ex-peer** — warm, equal footing, shared trench memory
3. **Ex-direct-report** — care-driven, invest in them, not extract from them
4. **Ex-client** — non-transactional, prove no ask in opener
5. **Cross-functional / faded** — low-pressure, easy out built in

Templates for each in EN and FR, with reply-handling guidance per archetype.

## The 7-phase workflow

1. **Build the tracking infrastructure** (Notion, Airtable, or spreadsheet)
2. **Source the contact list** (LinkedIn CSV + brain-dump in parallel)
3. **Classify and triage** (script-assisted for breadth, manual for depth)
4. **Draft DMs using templates**
5. **Coach review loop** (this is non-optional)
6. **Send and track**
7. **Reply handling** (where most reconnection campaigns die)

Full detail in `SKILL.md`.

## The CSV classifier

`scripts/classify-csv.py` takes a LinkedIn Connections.csv export and your career history (in JSON), and produces an enriched CSV ready to import into Notion or Airtable. It auto-classifies "How we met" against your past employers and buckets contacts into eras based on connection date.

```bash
python scripts/classify-csv.py \
  --csv connections.csv \
  --career my-career.json \
  --output enriched.csv
```

Manual review still required: relationship type, geo, priority, and strength all need human judgement.

## Credits

Built by Julien Amar (Coyote Consulting) in April 2026. Methodology informed by working with Sandy Cohen on a structured LinkedIn reactivation campaign for a senior interim mission search.

## License

Use it, share it, fork it. No warranty. If you build on top, a mention in your post is appreciated but not required.
