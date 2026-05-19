# Coyote Skills

Free Claude Code skills built by [Coyote Consulting](https://www.notion.so/Hub-de-l-Agence-314bea2c53d880c9bb15d8482a48f5ea).

---

## Skills

### `coyote-jd-scorer-uk` — Score any UK JD against your own criteria

Scores a UK job description against criteria you set. Returns a 0-10 fit score, top 3 selection criteria with evidence quotes, UK-specific exclusion flags (IR35, day rate, clearance, sector traps), a "Think twice" honesty section, and a tailoring angle.

**[Full docs & Notion page](https://www.notion.so/364bea2c53d8812492c1cd5c1298d1c0)**

```bash
mkdir -p ~/.claude/skills/coyote-jd-scorer-uk && \
  curl -fsSL https://raw.githubusercontent.com/julo2178/coyote-skills/main/coyote-jd-scorer-uk/SKILL.md \
  -o ~/.claude/skills/coyote-jd-scorer-uk/SKILL.md
```

---

### `coyote-jd-scorer-fr` — Scorer toute annonce FR contre vos propres criteres

Meme logique que le scorer UK, avec le glossaire du marche francais: TJM, Portage Salarial, SASU / EI, plateformes Le Hibou / Creme de la Creme, langue de travail.

```bash
mkdir -p ~/.claude/skills/coyote-jd-scorer-fr && \
  curl -fsSL https://raw.githubusercontent.com/julo2178/coyote-skills/main/coyote-jd-scorer-fr/SKILL.md \
  -o ~/.claude/skills/coyote-jd-scorer-fr/SKILL.md
```

---

### `coyote-network-reactivation` — Reconnect with dormant contacts without burning goodwill

A system for running a structured reactivation campaign across your professional network. Triages your LinkedIn connections by relationship strength and career chapter, generates archetype-matched DM templates (ex-manager, ex-peer, ex-direct report, ex-client, cross-functional) in EN and FR, and walks you through a workflow that prioritises reconnecting first — before any ask.

Includes: SKILL.md, DM templates, anti-patterns guide, Notion tracker template, Python script to classify a LinkedIn CSV export.

```bash
mkdir -p ~/.claude/skills/coyote-network-reactivation && \
  curl -fsSL https://raw.githubusercontent.com/julo2178/coyote-skills/main/coyote-network-reactivation/SKILL.md \
  -o ~/.claude/skills/coyote-network-reactivation/SKILL.md
```

---

## Licence

MIT — free to use, fork, adapt.

## About

Coyote Consulting deploys AI tooling and operating-model design for transformation programmes. These skills are free public resources. If you want similar tooling running inside your hiring or transformation programme, get in touch.
