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

### `coyote-network-reactivation` · Renouer avec vos contacts dormants sans brûler le lien

Un système pour mener une campagne structurée de réactivation sur votre réseau professionnel. Il trie vos relations LinkedIn par force du lien et par chapitre de carrière, produit des modèles de messages appariés à cinq archétypes (ancien manager, ancien pair, ancien collaborateur direct, ancien client, transverse) en FR et EN, et déroule une méthode qui reconnecte d'abord, avant toute demande.

Contenu : SKILL.md, les modèles de messages, le guide d'anti-patterns, le schéma du suivi Notion, et un script Python qui classe un export CSV LinkedIn contre votre parcours.

**Skill en français.** Les modèles de messages sont fournis dans les deux langues.

Installation en un fichier, depuis la dernière release :

```bash
curl -fsSL -o coyote-network-reactivation.skill \
  https://github.com/julo2178/coyote-skills/releases/latest/download/coyote-network-reactivation.skill
```

Sur Claude.ai, importez ce fichier dans Paramètres → Compétences. Pour Claude Code, dézippez-le dans votre répertoire de skills :

```bash
unzip coyote-network-reactivation.skill -d ~/.claude/skills/
```

---

## Licence

MIT — free to use, fork, adapt.

## About

Coyote Consulting deploys AI tooling and operating-model design for transformation programmes. These skills are free public resources. If you want similar tooling running inside your hiring or transformation programme, get in touch.
