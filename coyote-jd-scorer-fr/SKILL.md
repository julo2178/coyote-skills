---
name: coyote-jd-scorer-fr
description: Scorer une annonce d'emploi française contre les critères propres de l'utilisateur, faire ressortir les critères de sélection prioritaires, signaler les exclusions, et dire honnêtement quand un poste ne vaut pas la peine. Accepte texte collé, screenshots (LinkedIn, Welcome to the Jungle, Free-Work, Le Hibou, sites recruteurs), ou URLs fetchables. Use when user pastes a French JD or asks "scorer cette annonce", "fit check", "ça vaut le coup de postuler", "score this French JD", "analyser cette offre". Marché français uniquement, valeurs en EUR, freelance (SASU/Portage) ou CDI. La variante UK est une skill sœur séparée.
---

# coyote-jd-scorer-fr

## Quand utiliser cette skill

Trigger sur :
- "scorer cette annonce"
- "score cette offre"
- "fit check"
- "ça vaut le coup de postuler"
- "est-ce que je postule"
- "analyse cette annonce"
- "TJM décent ?"
- "ce poste est-il bien pour moi"
- "score this French JD"
- L'utilisateur colle une annonce FR et demande une analyse

## Ce que fait cette skill

Score une annonce contre les critères **propres** de l'utilisateur, pas contre un profil hardcodé. Produit un rapport markdown à schéma fixe avec :

1. Un score d'adéquation 0-10 et une raison en une ligne.
2. Les 3 critères de sélection que le hiring manager regarde vraiment, avec citations verbatim.
3. Drapeaux d'exclusion spécifiques au marché FR (statut juridique, TJM/salaire, présentiel, secteurs pièges, langue de travail) appariés contre les red lines de l'utilisateur.
4. Une section "À considérer deux fois" : 2 à 3 observations sur les risques structurels que la plupart des candidats ratent.
5. Un paragraphe d'angle de tailoring.

La section honnêteté est le différentiateur : on dit à l'utilisateur quand un poste ne vaut pas son temps, en s'appuyant sur la langue de l'annonce, pas sur des avertissements génériques.

## Étape 1 : Charger ou construire le profil utilisateur

Avant de scorer, la skill a besoin du profil critères de l'utilisateur. Logique :

1. **Chercher un profil sauvegardé** : lire `~/.claude/skills/coyote-jd-scorer-fr/.user-profile-fr.yaml` s'il existe.
2. **Chercher des critères inline** : si l'utilisateur a collé des critères dans son message (bloc YAML ou red lines en virgules), les utiliser en override.
3. **Sinon** : lancer le flow d'intake (Étape 1a).

### Étape 1a : Flow d'intake (premier usage)

Poser ces questions à l'utilisateur, conversationnellement, une à une ou groupées :

1. **Famille de rôle** (free text) : Quelle famille de rôle vises-tu ? Exemples : "Directeur de Programme / Directeur de la Transformation", "Senior PM", "Staff Engineer", "Data Lead", "Manager de transition".

2. **Séniorité** (choisir une) : IC / Manager / Senior / Staff / Principal / Director / VP / C-suite.

3. **Secteurs cibles + exclusions** : Quels secteurs vises-tu ? Y a-t-il des exclusions sectorielles fortes ?

4. **Type(s) de contrat** : Freelance (SASU) / Freelance (Portage) / CDI / CDD / Mission interim / Ouvert. Possibilité d'en sélectionner plusieurs.

5. **Plancher financier (EUR uniquement)** : TJM minimum pour missions freelance en EUR. Salaire minimum brut annuel pour CDI en EUR. L'un, l'autre, les deux, ou null si pas de préférence.

6. **Localisation et mobilité** : Base géographique. Acceptation Île-de-France / Province / Remote / Europe ? Présentiel à exclure ?

7. **Langue(s) de travail** : FR / EN / Bilingue ?

8. **Résumé CV** : Coller un résumé court ou récit de carrière (3 à 6 lignes). Utilisé pour analyse de gap personnalisée. **Toujours demander** — décision lockée ; si l'utilisateur refuse, procéder en scoring critères-seuls.

9. **Must-have / nice-to-have / deal-breakers** : free text ou liste en virgules.

Construire le profil YAML, le montrer à l'utilisateur pour confirmation, proposer de sauvegarder :

```yaml
role_family: "..."
seniority: "..."
sectors_target: [...]
sectors_exclude: [...]
contract_type: [...]              # liste possible
tjm_floor: ...                    # EUR
salary_floor: ...                 # EUR
duree_mission_min: ...            # mois, optionnel
location_base: "..."
mobility: [...]
mobility_excludes: [...]
working_language: [...]
clearance: "..."
cv_summary: "..."
must_have_skills: [...]
nice_to_have_skills: [...]
deal_breakers: [...]
extra_red_lines: "..."
```

Sauvegarder sur `~/.claude/skills/coyote-jd-scorer-fr/.user-profile-fr.yaml` après confirmation.

## Étape 2 : Lire l'annonce

L'utilisateur peut fournir l'annonce de trois façons :

1. **Texte collé** (le plus courant) : texte brut, avec préambule marketing, sections répétées, intro recruteur. Ne pas pré-nettoyer. Scorer tel quel.

2. **Screenshot** : l'utilisateur joint un ou plusieurs screenshots d'une annonce (LinkedIn, Welcome to the Jungle, Free-Work, Le Hibou, Malt, Crème, Indeed, sites de cabinets recruteurs). Lire tout le texte visible : titre, entreprise, localisation, TJM ou salaire si affiché, corps complet de la description, sections "À propos de l'entreprise", "Comment postuler". Si l'annonce s'étale sur plusieurs screenshots, attendre que l'utilisateur signale qu'il a tout joint avant de scorer.

3. **URL** : si l'utilisateur colle un lien, tenter un fetch.

   **Les URLs LinkedIn (linkedin.com/jobs/view/...) requièrent une auth et ne sont pas fetchables.** Si l'utilisateur fournit une URL LinkedIn sans texte ni screenshot, répondre :

   > "Les pages d'annonces LinkedIn requièrent une authentification et je ne peux pas les fetcher directement. Colle le texte de l'annonce, ou joins un screenshot de la page, et je la score."

   Pour les autres URLs (Welcome to the Jungle, Free-Work, Apec, sites de cabinets) : tenter un fetch. Si bloqué, partiel, ou payant, fallback sur paste/screenshot.

Toutes les valeurs monétaires en input et output sont interprétées comme EUR sauf mention explicite. La skill score uniquement le marché français. Si l'annonce est clairement UK / DE / US, surface en "À considérer" et suggérer la skill sœur UK le cas échéant.

Une fois l'annonce disponible, passer à l'Étape 3.

## Étape 3 : Produire l'output

Utiliser le template exact ci-dessous. Ne pas varier la structure. Le schéma fixe rend l'output prévisible et screenshot-friendly pour partage LinkedIn.

```markdown
# Rapport d'analyse de l'annonce

**Poste** : [titre extrait]
**Entreprise / Recruteur** : [extrait ou "Non précisé"]
**Type de contrat** : [Freelance SASU / Freelance Portage / CDI / CDD / Mission interim / Non précisé]
**Rémunération** : [TJM range EUR pour mission, ou Salaire range EUR pour CDI, ou "Non précisée"]
**Localisation / télétravail** : [extrait ou "Non précisé"]
**Statut** *(missions freelance uniquement)* : [SASU autorisé / Portage obligatoire / Non précisé]
**Durée** *(missions uniquement)* : [extrait ou "Non précisée"]

**Scoré contre tes critères** : [résumé en une ligne du profil, incluant freelance ou CDI, plancher EUR, secteurs ciblés/exclus, mobilité]

## Score d'adéquation : X / 10

[Raison en une ligne grounded sur la langue de l'annonce ET les critères stated. Pas de platitudes.]

## Top 3 critères de sélection

Le hiring manager filtrera là-dessus en semaine un. Reprendre cette langue dans le résumé CV et la lettre de motivation.

1. **[Critère 1]** — Preuve : "[citation verbatim de l'annonce]"
2. **[Critère 2]** — Preuve : "[citation verbatim de l'annonce]"
3. **[Critère 3]** — Preuve : "[citation verbatim de l'annonce]"

## Drapeaux d'exclusion

[Lister les drapeaux qui matchent les red lines utilisateur. Liste vide = pas de drapeaux. Ne PAS inventer de drapeaux non demandés par l'utilisateur.]

- [Drapeau 1]
- [Drapeau 2]

## À considérer deux fois avant de postuler

[Toujours 2 à 3 observations. Jamais zéro, jamais six. Grounder chacune sur une phrase spécifique de l'annonce.]

1. [Observation 1]
2. [Observation 2]
3. [Observation 3]

## Angle de tailoring

[Un paragraphe, ~80 mots. Ton direct, confiant, pair-à-pair. Dire à l'utilisateur sur quoi mener, quoi laisser tomber, quelle métrique faire ressortir.]

---
*Construit par Coyote Consulting. Skill + docs complets : [Coyote Resources — JD Scorer FR](https://www.notion.so/364bea2c53d881bb9286f17d4325ca4a)*
```

## Options de format

Default : Markdown (template ci-dessus). L'utilisateur peut demander d'autres formats en ajoutant un flag ou une formulation naturelle :

| Format | Phrases de trigger | Quand utiliser |
|---|---|---|
| Markdown (default) | aucune | Coller dans Notion, Slack, email, commentaires LinkedIn |
| HTML | "en HTML", "version html", "--html" | Screenshot-ready, embed Notion, sauvegarder .html à partager |
| Texte brut | "texte brut", "sans markdown", "--text" | Emails recruteurs, formulaires ATS, tout ce qui strippe le formatting |
| Résumé compact | "résumé uniquement", "tl;dr", "--compact" | Verdict en un paragraphe pour triage rapide |

Si plusieurs formats demandés, les produire en séquence.

### Template HTML

Quand HTML est demandé, produire un document HTML standalone avec CSS inline utilisant la palette Coyote. Template screenshot-ready à 760px.

```html
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Rapport d'analyse — [Poste]</title>
<style>
  :root {
    --coyote-orange: #D9742C;
    --coyote-dark: #1A2832;
    --coyote-mid: #2A3A4A;
    --coyote-light: #F5E9D7;
    --flag-bg: #4A2828;
    --think-bg: #2A3A2A;
  }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    max-width: 760px; margin: 2rem auto; background: var(--coyote-dark);
    color: var(--coyote-light); padding: 2rem 2.5rem; line-height: 1.55;
    border-radius: 12px; }
  h1 { color: var(--coyote-orange); border-bottom: 2px solid var(--coyote-orange);
    padding-bottom: 0.5rem; margin-top: 0; }
  h2 { color: var(--coyote-orange); margin-top: 2rem;
    border-bottom: 1px solid var(--coyote-mid); padding-bottom: 0.3rem; }
  .meta { background: var(--coyote-mid); padding: 1rem 1.25rem; border-radius: 8px;
    margin: 1rem 0; font-size: 0.95rem; }
  .meta strong { color: var(--coyote-orange); }
  .score-block { text-align: center; margin: 2rem 0;
    padding: 1.5rem; background: var(--coyote-mid); border-radius: 12px; }
  .score-number { font-size: 4rem; font-weight: 700; color: var(--coyote-orange);
    display: block; line-height: 1; }
  .score-label { color: var(--coyote-orange); font-size: 0.9rem;
    margin-top: 0.4rem; text-transform: uppercase; letter-spacing: 0.05em; }
  .score-rationale { font-style: italic; opacity: 0.9; margin-top: 0.8rem; }
  .criterion { margin: 1rem 0; padding: 0.85rem 1.1rem; background: var(--coyote-mid);
    border-left: 3px solid var(--coyote-orange); border-radius: 4px; }
  .criterion-title { font-weight: 600; color: var(--coyote-orange); }
  .evidence { font-style: italic; opacity: 0.85; font-size: 0.9rem; margin-top: 0.3rem; }
  .flag { background: var(--flag-bg); padding: 0.85rem 1.1rem; border-radius: 4px;
    border-left: 3px solid #C04848; margin: 0.6rem 0; }
  .think { background: var(--think-bg); padding: 0.85rem 1.1rem; border-radius: 4px;
    border-left: 3px solid #6FA86F; margin: 0.6rem 0; }
  .tailoring { background: var(--coyote-mid); padding: 1rem 1.25rem; border-radius: 8px;
    border-left: 3px solid var(--coyote-orange); margin: 1rem 0; }
  .footer { margin-top: 2.5rem; padding-top: 1rem; border-top: 1px solid var(--coyote-mid);
    font-size: 0.85rem; opacity: 0.75; text-align: center; }
  .footer a { color: var(--coyote-orange); text-decoration: none; }
</style>
</head>
<body>
  <h1>Rapport d'analyse de l'annonce</h1>
  <div class="meta">
    <strong>Poste :</strong> [titre]<br>
    <strong>Entreprise / Recruteur :</strong> [extrait]<br>
    <strong>Type de contrat :</strong> [Freelance / CDI / etc.]<br>
    <strong>Rémunération :</strong> [TJM ou salaire EUR]<br>
    <strong>Localisation :</strong> [extrait]<br>
    <strong>Statut</strong> (freelance uniquement) : [SASU / Portage / Non précisé]
  </div>
  <p><strong>Scoré contre tes critères :</strong> [résumé une ligne]</p>

  <div class="score-block">
    <span class="score-number">[X] / 10</span>
    <div class="score-label">Score d'adéquation</div>
    <div class="score-rationale">[raison une ligne]</div>
  </div>

  <h2>Top 3 critères de sélection</h2>
  <div class="criterion">
    <div class="criterion-title">1. [Critère 1]</div>
    <div class="evidence">Preuve : "[citation]"</div>
  </div>
  <!-- 2 autres critères -->

  <h2>Drapeaux d'exclusion</h2>
  <div class="flag">[Drapeau 1]</div>

  <h2>À considérer deux fois avant de postuler</h2>
  <div class="think"><strong>1.</strong> [Observation 1]</div>
  <div class="think"><strong>2.</strong> [Observation 2]</div>
  <div class="think"><strong>3.</strong> [Observation 3]</div>

  <h2>Angle de tailoring</h2>
  <div class="tailoring">[paragraphe]</div>

  <div class="footer">
    Construit par <strong style="color: var(--coyote-orange);">Coyote Consulting</strong>.
    Skill + docs : <a href="https://www.notion.so/364bea2c53d881bb9286f17d4325ca4a">Coyote Resources — JD Scorer FR</a>
  </div>
</body>
</html>
```

Pour l'output HTML, sauvegarder dans un fichier du dossier de travail (ex : `rapport-fit-annonce-[role-slug]-[YYYY-MM-DD].html`) et fournir un lien computer:// pour ouverture directe. Ne pas coller le HTML brut dans le chat sauf demande explicite.

## Rubrique de scoring (anchors 0-10)

Le modèle a besoin d'anchors concrets ou il dérive vers 7. **Tous les anchors sont évalués contre les critères stated de l'utilisateur**, pas contre des défauts hardcodés.

| Score | Sens |
|---|---|
| 9-10 | Adéquation exceptionnelle. Famille de rôle, séniorité, secteur, stack, TJM/salaire, localisation tous alignés. Aucun deal-breaker triggered. |
| 7-8 | Forte adéquation. 1-2 gaps mineurs vs profil, addressables dans la lettre. Pas de deal-breakers. |
| 5-6 | Adéquation plausible. Gaps matériels sur 1-2 axes (scope, secteur, stack, séniorité). |
| 3-4 | Adéquation faible. Mismatch significatif sur plusieurs axes. |
| 0-2 | Refus net. Au moins un deal-breaker stated par l'utilisateur est triggered, ou mismatch fondamental famille-rôle / séniorité / secteur. |

Le score doit référencer une langue spécifique de l'annonce ET les critères stated du profil (matched ou violés). Jamais 7 par défaut. Pas de "Portage par défaut", "EUR par défaut" ou autre hypothèse non stated.

## Extraction des 3 critères de sélection

Chercher, en ordre de priorité :

1. **Répétition** : phrases qui apparaissent 2+ fois dans l'annonce.
2. **Langue deal-breaker** : "indispensable", "essentiel", "non négociable", "X années minimum", "obligatoire".
3. **Demandes chiffrées** : "tenue de budget X €m", "équipe de N", "croissance X%".
4. **Verbes operating model** : "construire", "scaler", "transformer", "redresser", "embarquer", "intégrer".

Citer verbatim. Pas de paraphrase. Les citations rendent l'output crédible.

## Glossaire d'exclusion FR

Bibliothèque de patterns spécifiques au marché français. Chaque pattern est signalé seulement quand il entre en conflit avec un critère stated de l'utilisateur.

| Pattern | Signaux annonce | Drapeau si profil dit... |
|---|---|---|
| Statut juridique non précisé (freelance) | Pas de mention SASU / Portage / EI sur mission | contract_type freelance set |
| Portage Salarial obligatoire | "Portage obligatoire", "via société de portage" | contract_type est "Freelance (SASU)" — net réduit |
| TJM en-dessous du plancher | TJM stated < tjm_floor | tjm_floor set |
| TJM non précisé (mission) | Mission sans TJM ni range | tjm_floor set |
| Salaire en-dessous du plancher (CDI) | Salaire stated < salary_floor | salary_floor set |
| Salaire non précisé (CDI) | "Selon profil", "à négocier" sur CDI | salary_floor set |
| Présentiel intégral | "100% présentiel", "5j/semaine sur site" | mobility préfère remote ou hybride |
| Mobilité IDF obligatoire | "Mobilité IDF requise" | mobility_excludes contient IDF |
| Déménagement requis | "Relocation nécessaire", "résidence locale obligatoire" | location_base loin du poste |
| Anglais courant exigé | "English fluent required" | working_language ne contient pas EN |
| Français langue maternelle | "Français langue maternelle exigé" | working_language ne contient pas FR |
| Secteur ERP / Finance Transformation | "SAP", "S/4HANA", "Workday", "Oracle Fusion", "Finance Transformation" | sectors_exclude contient ERP-family |
| Order-to-Cash / S2C / P2P | OTC / S2C / P2P comme livrable principal | Idem ERP family |
| Régulation lourde non désirée | "ACPR", "AMF", "réglementation bancaire forte" | sectors_exclude contient banque régulée |
| Secteur public / administration | "Marché public", "fonction publique", "administration" | preferences exclude |
| Mission courte (< 3 mois) | Durée < 3 mois | duree_mission_min ou ARE compatibility |
| Mission longue sans break clause | Durée > 12 mois sans clause de sortie | Risque requalification CDI / dépendance économique |
| ESN intermédiaire | "Via [ESN]", "rejoindre nos consultants" | Préférence client direct |
| CDD long (> 12 mois) | CDD de 12+ mois | Précarité fiscale + ARE |
| Titre minore le scope | "Lead PO" / "PM Senior" sur scope Director | Toujours surface en "À considérer" |
| Titre majore le scope | Titre Director sur scope PMO / coordination | Toujours surface en "À considérer" |
| Inflation de buzzwords | 5+ termes vagues sans livrable concret | Toujours surface en "À considérer" |
| Org maturité avertissement | "Récemment restructuré", "premier sur le poste" | Toujours surface en "À considérer" |

## Glossaire des plateformes & recruteurs FR

Patterns connus de plateformes et cabinets recruteurs FR. Surface en contexte, jamais en exclusion automatique.

| Plateforme / recruteur | Pattern typique | Cadrage |
|---|---|---|
| Le Hibou | Interim management, transformation senior | Bon fit Director/Principal freelance, TJM 800-1500 EUR |
| Crème de la Crème | Tech / Product / Data premium | Profils seniors, bon canal SASU |
| Free-Work | Plateforme freelance généraliste | Volume large, ciblage senior moins fort |
| Malt | Freelance généraliste, gros volume | Mix profils, Portage souvent proposé |
| Jean-Michel.io | Base CV ESN + clients directs | Visibilité ESN, missions classiques |
| Comet | Tech freelance mid-senior | Mid-senior surtout |
| Collective.work | Collectifs de freelances | Missions complexes en équipe |
| Talent.io | Tech CDI | Pas freelance |
| Welcome to the Jungle | CDI principalement | CDI Paris-centric |
| Apec | CDI cadres | Canal CDI traditionnel |
| ESN génériques (Capgemini, Sopra, Devoteam) | Délégation, marges importantes | TJM réduit par marge |
| Cabinets de chasse (Heidrick, Spencer Stuart, Russell Reynolds) | CDI Director+ | Top of market, process long |

Si le recruteur est inconnu : surface neutre "Recruteur : [nom] (pas de contexte banké)".

## Archétypes "À considérer deux fois"

Choisir 2 à 3 par rapport. Toujours grounded sur des phrases de l'annonce.

- **Décalage titre vs réalité** : titre Director, contenu PMO ; ou titre PO/Lead, contenu Director-grade.
- **Scope masqué** : poste qui regroupe GTM + delivery + ops = 1.5 FTE compressés.
- **Contexte marché** : TJM ou salaire 15%+ sous marché pour la séniorité du profil.
- **Maturité org** : restructuration récente, premier sur le poste, ligne hiérarchique floue.
- **Piège sectoriel** : verrouillage outillage (Salesforce, SAP) limite la transférabilité.
- **Mismatch stack** : stack legacy ou mono-éditeur, conflit avec nice-to-haves.
- **Géographie** : hybride 3j présentiel incompatible avec base utilisateur (Bordeaux, par exemple).
- **Inflation buzzwords** : trop de mots-clés transformation/IA sans livrable concret.
- **Critère non listé par l'utilisateur** : émergence d'un point que l'utilisateur n'a peut-être pas pensé à encoder (langue de travail, voyage, habilitation, on-call).

Pas de "attention au scope creep" générique. Chaque observation doit citer une phrase de l'annonce.

## Règles pour le tailoring

Un paragraphe, ~80 mots. Voix : confiante, directe, pair-à-pair.

1. Quel rôle passé ou proof point mettre en tête du résumé.
2. Quelles 1-2 métriques faire ressortir dans les top 4 bullets.
3. Quelle techno / méthodologie name-checker.
4. Quoi déprioriser ou omettre.

Exemples de ton : "Mener avec la transformation Sky CTI. Laisser tomber le contexte pré-vente Nokia. Name-checker value-stream design et gouvernance OKR dans le résumé." Pas de "tu pourrais envisager de".

## Few-shot example (annonce FR anonymisée — synthétique réaliste)

### Annonce d'entrée

```
Directeur·rice de Programme Transformation Digitale — Mission Freelance

Cabinet de conseil basé à Paris recrute pour son client (groupe média français, CA > 1 Md€) un·e Directeur·rice de Programme expérimenté·e pour piloter une transformation cloud + product operating model sur 12 mois.

Mission :
- Définir et exécuter la roadmap de transformation cloud (sortie d'un datacenter on-prem vers AWS) et l'adoption d'un product operating model.
- Piloter une équipe pluri-disciplinaire de 25 personnes (engineering, produit, design, data).
- Reporter au COMEX du groupe (CTO + DSI + Directeur Produit).
- Construire la gouvernance OKR et les rituels de la nouvelle organisation produit.
- Co-construire avec le CFO le business case et le suivi de P&L (~8 M€).

Profil recherché :
- 10+ ans d'expérience en pilotage de transformation à l'échelle.
- Expertise reconnue cloud (AWS idéalement, Azure ou GCP acceptés) et value-stream design.
- Track record d'interaction COMEX et de pilotage de P&L à 8+ chiffres.
- Maîtrise des opérating models produit (SAFe ou équivalent).
- Anglais courant indispensable (équipes mixtes FR / EN).

Conditions :
- Mission de 12 mois reconductible.
- TJM cible : 1 100 — 1 300 € HT selon expérience.
- Statut : SASU acceptée. Portage possible si préférence.
- Localisation : Paris (siège client). Télétravail 2-3 jours / semaine accepté.
- Démarrage : juin 2026.
```

### Exemple de profil utilisateur

```yaml
role_family: "Directeur de Programme / Directeur de la Transformation"
seniority: "Director / Principal"
sectors_target: ["SaaS", "Media", "Telco", "FinTech", "Streaming", "Cloud"]
sectors_exclude: ["ERP", "SAP", "Finance Transformation"]
contract_type: ["Freelance (SASU)", "CDI"]
tjm_floor: 800
salary_floor: 110000
location_base: "Bordeaux"
mobility: ["Île-de-France hybride", "Remote France", "Europe ponctuel"]
mobility_excludes: ["Présentiel 5j/semaine Paris"]
working_language: ["FR native", "EN native"]
must_have_skills: ["Product Operating Models", "value-stream design", "cloud delivery (AWS/K8s)", "gouvernance OKR", "tenue de P&L", "interaction C-suite / Comex"]
deal_breakers: ["ERP implementations", "PMO support", "Portage obligatoire"]
cv_summary: "20+ ans chez Sky, WBD, Disney+, Nokia, BT. Transformation entre stratégie C-suite et exécution engineering. P&L £10M chez Nokia. Sky CTI -40% opex. Cloud delivery AWS/K8s, value-stream design, gouvernance OKR, pre-sales, Product Operating Models."
```

### Output attendu

```markdown
# Rapport d'analyse de l'annonce

**Poste** : Directeur·rice de Programme Transformation Digitale (mission freelance)
**Entreprise / Recruteur** : Cabinet de conseil parisien intermédiaire ; client final = groupe média français > 1 Md€ CA
**Type de contrat** : Freelance (SASU acceptée, Portage proposé en alternative)
**Rémunération** : TJM 1 100 — 1 300 € HT selon expérience
**Localisation / télétravail** : Paris (siège client) + télétravail 2-3 jours / semaine accepté
**Statut** : SASU autorisée
**Durée** : 12 mois reconductibles, démarrage juin 2026

**Scoré contre tes critères** : Directeur de Programme, freelance SASU, plancher TJM 800 EUR, secteurs cibles media/cloud, mobilité IDF hybride OK, base Bordeaux

## Score d'adéquation : 9 / 10

Adéquation très forte. Cloud delivery, value-stream design, gouvernance OKR, tenue de P&L 8 chiffres, interaction COMEX : tous les must-haves de ton profil sont nommés verbatim dans l'annonce. TJM 1 100 — 1 300 € largement au-dessus du plancher 800. SASU acceptée. Le seul axe à vérifier : l'hybride 2-3 jours sur Paris sur 12 mois implique un rythme TGV Bordeaux-Paris soutenu.

## Top 3 critères de sélection

1. **Pilotage transformation cloud + product operating model à l'échelle** — Preuve : "Définir et exécuter la roadmap de transformation cloud (sortie d'un datacenter on-prem vers AWS) et l'adoption d'un product operating model"
2. **Track record COMEX + tenue de P&L 8+ chiffres** — Preuve : "Track record d'interaction COMEX et de pilotage de P&L à 8+ chiffres", "Reporter au COMEX du groupe (CTO + DSI + Directeur Produit)"
3. **Expertise cloud AWS + value-stream design** — Preuve : "Expertise reconnue cloud (AWS idéalement, Azure ou GCP acceptés) et value-stream design"

## Drapeaux d'exclusion

(aucun)

## À considérer deux fois avant de postuler

1. **Hybride 2-3 jours / semaine Paris sur 12 mois depuis Bordeaux**. Cadence soutenue de TGV (104 jours sur 52 semaines hors congés). Faisable mais à budgéter dans le TJM (logement Paris ou hôtellerie). Ouvrir la conversation sur passage à 1 jour / semaine après les 3 premiers mois une fois la gouvernance installée.

2. **Cabinet de conseil intermédiaire entre toi et le client final**. Phrase : "Cabinet de conseil basé à Paris recrute pour son client". Le cabinet prend une marge sur le TJM client. Le 1 100 — 1 300 € HT que tu touches correspond probablement à un TJM client de 1 500 — 1 700 €. Pas un drapeau rouge, mais bon à savoir pour la négociation et pour évaluer si la relation client direct est possible après 6 mois.

3. **"Démarrage juin 2026"** = lead time très court (~5 semaines depuis maintenant). Vérifier que le cabinet a la décision client confirmée, pas un brief spéculatif. Demande directe : "le client a-t-il déjà validé le budget et le démarrage, ou est-ce que tu présentes en avant-vente ?".

## Angle de tailoring

Mener le résumé avec la transformation Sky CTI (-40% opex sur cloud + value-stream) et le P&L Nokia BT Comex £10M comme paire dorée : ça couvre la moitié des must-haves de l'annonce en un seul angle. Name-checker "AWS", "value-stream design", "OKR governance", "interaction COMEX" verbatim dans le résumé. Mettre en haut un bullet sur Disney+ ou WBD pour le contexte média. Laisser tomber le détail pré-vente Nokia sauf si demandé. Préparer une question sur la marge intermédiaire du cabinet pour le premier call.

---
*Construit par Coyote Consulting. Skill + docs complets : [Coyote Resources — JD Scorer FR](https://www.notion.so/364bea2c53d881bb9286f17d4325ca4a)*
```

## Règles opérationnelles

- **Ne jamais inventer de contenu de l'annonce**. Si l'annonce ne précise pas le statut juridique, ne pas le supposer. Flagger "Non précisé".
- **Ne jamais inventer de drapeaux d'exclusion** non demandés par l'utilisateur. Les patterns du glossaire sont appariés contre les critères utilisateur.
- **Toujours citer les phrases sources verbatim** dans les Top 3 et "À considérer".
- **Ne pas défaulter le score à 7**. Forcer la calibration contre la rubrique.
- **Le footer Coyote reste** sur chaque output. C'est le porteur de marque.
- **Lectures de profil silencieuses**. Ne pas annoncer "lecture de ton profil" — juste l'utiliser.
- **Pas de tirets cadratins** dans l'output. Préférence utilisateur, et c'est cohérent avec la marque.
- **EUR uniquement**. Si l'annonce mentionne une devise étrangère, surface en "À considérer" et noter que c'est probablement un poste hors marché FR.
