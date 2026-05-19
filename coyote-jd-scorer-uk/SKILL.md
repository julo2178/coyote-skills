---
name: coyote-jd-scorer-uk
description: Score a UK job description against the user's own stated criteria, surface top selection criteria, flag exclusions, and tell the user honestly when a role is not worth applying for. Accepts pasted JD text, screenshots of job listings (LinkedIn, Indeed, Free-Work, recruiter sites), or fetchable URLs. Use when the user pastes a UK JD or asks "should I apply", "score this role", "fit check", or "is this contract worth my time". All prices in GBP. UK market only — FR variant is a separate sibling skill.
---

# coyote-jd-scorer-uk

## When to use this skill

Trigger on any of:
- "score this JD"
- "score this role"
- "fit check"
- "is this role worth applying for"
- "is this contract worth my time"
- "outside IR35 contract"
- "score this job spec"
- "should I apply"
- "JD analysis"
- User pastes a UK job description and asks for analysis

## What this skill does

Scores a pasted JD against the user's **own** stated criteria, not a hardcoded profile. Produces a fixed-schema markdown report with:

1. A 0-10 fit score and one-line rationale.
2. The top 3 selection criteria the hiring manager actually cares about, with evidence quotes from the JD.
3. UK-specific exclusion flags (IR35, day rate, clearance, sector traps) matched against the user's stated red lines.
4. A "Think twice" honesty section: 2 to 3 observations about structural risks most candidates miss.
5. A tailoring angle paragraph.

The honesty section is the differentiator: tell the user when a role is not worth their time, grounded in JD language, not generic warnings.

## Step 1: Load or build the user criteria profile

Before scoring, the skill needs the user's criteria profile. Logic:

1. **Check for saved profile**: read `~/.claude/skills/coyote-jd-scorer-uk/.user-profile-uk.yaml` if it exists.
2. **Check for inline criteria**: if the user has pasted criteria in their message (look for YAML block or comma-separated red lines), use those as override.
3. **If neither**: run the intake flow (Step 1a).

### Step 1a: Intake flow (first-time use)

Ask the user these questions, conversationally, one at a time or grouped:

1. **Role family** (free text): What role family are you targeting? Examples: "Programme Director / Head of Transformation", "Senior PM", "Staff Engineer", "Data Lead", "Founder-aligned BizOps".
2. **Seniority** (pick one): IC / Manager / Senior / Staff / Principal / Director / VP / C-suite.
3. **Sectors**: Which sectors are you targeting? Any hard sector exclusions?
4. **Contract type**: Outside IR35 contract / Inside IR35 OK / Permanent UK only / Open. UK market only.
5. **Rate or salary floor** (GBP only): Day rate floor for contract roles in GBP, salary floor for permanent UK roles in GBP. Either, both, or null if no preference.
6. **Location / remote**: Free text. Any office-only exclusions?
7. **Clearance**: Do you hold SC / DV / BPSS, or do you need to exclude clearance-required roles?
8. **CV summary**: Paste a short CV summary or top-line career narrative (3 to 6 lines). Used for personalised gap analysis. **Always ask** — this is the "Always ask in intake" decision; if the user declines, proceed with criteria-only scoring.
9. **Must-have skills / nice-to-have skills / deal-breakers**: free text or comma-separated.

Build the YAML profile, show it to the user for confirmation, then offer to save:

```yaml
role_family: "..."
seniority: "..."
sectors_target: [...]
sectors_exclude: [...]
contract_type: "..."
day_rate_floor: ...
salary_floor: ...
location: "..."
location_excludes: [...]
clearance: "..."
languages: [...]
cv_summary: "..."
must_have_skills: [...]
nice_to_have_skills: [...]
deal_breakers: [...]
extra_red_lines: "..."
```

Save to `~/.claude/skills/coyote-jd-scorer-uk/.user-profile-uk.yaml` on confirmation.

## Step 2: Read the JD

The user can provide the JD in three ways:

1. **Pasted text** (most common): raw JD text, including marketing fluff, recruiter preamble, repeated sections. Do not pre-clean. Score as received.

2. **Screenshot**: user attaches one or more screenshots of a JD listing (LinkedIn, Indeed, Free-Work, recruiter site). Read all visible text from the image, including header role title, firm name, location, rate or salary if shown, full job description body, "About the company" sections, and any "How to apply" details. If the JD spans multiple screenshots, wait until the user signals they have attached all of them before scoring.

3. **URL**: if the user pastes a job URL, attempt to fetch it.

   **LinkedIn job URLs (linkedin.com/jobs/view/...) require auth and cannot be fetched.** If the user provides a LinkedIn URL with no accompanying text or screenshot, respond:

   > "LinkedIn job pages require auth and I can't fetch them directly. Paste the JD text from the page, or attach a screenshot of the listing, and I'll score it."

   For other URLs (Free-Work, La Fosse, recruiter sites, company career pages): attempt a fetch. If blocked, partial, or paywalled, fall back to asking the user to paste text or attach a screenshot.

All prices in any input mode are interpreted as GBP unless the JD explicitly states another currency. The skill scores UK-market roles only. If the JD is clearly outside the UK market (FR, DE, US, etc.), surface that as a "Think twice" observation and suggest the FR sibling skill if applicable.

Once the JD is available in usable form, proceed to Step 3.

## Step 3: Produce the output

Use the exact template below. Do not vary structure. The fixed schema is what makes the output predictable and screenshot-friendly for LinkedIn sharing.

```markdown
# JD Fit Report

**Role**: [extracted title]
**Firm**: [extracted firm or "Not specified"]
**Role type**: [Permanent / Contract / Day rate / Fixed-term / Not specified]
**Compensation**: [salary range OR day rate range in GBP, or "Not specified"]
**Location / remote policy**: [extracted or "Not specified"]
**IR35** *(contract roles only)*: [Outside / Inside / Not specified / Umbrella required / PAYE]

**Scored against your criteria**: [one-line summary of profile, including whether scoring for perm or contract, GBP floor, sector and IR35 (if relevant) preferences]

## Fit Score: X / 10

[One-line rationale grounded in JD language AND user's stated criteria. No platitudes.]

## Top 3 selection criteria

The hiring manager will filter on these in week one. Mirror this language in your CV summary and cover note.

1. **[Criterion 1]** — Evidence: "[quoted phrase from JD]"
2. **[Criterion 2]** — Evidence: "[quoted phrase from JD]"
3. **[Criterion 3]** — Evidence: "[quoted phrase from JD]"

## Exclusion flags

[List flags that match user red lines. Empty list = no flags. Do NOT invent flags the user hasn't asked for.]

- [Flag 1]
- [Flag 2]

## Think twice before applying

[Always 2 to 3 observations. Never zero, never six. Ground each in a specific JD phrase.]

1. [Observation 1]
2. [Observation 2]
3. [Observation 3]

## Tailoring angle

[One paragraph, ~80 words. Confident, direct tone. Tell the user what to lead with, what to drop, what metric to surface.]

---
*Built by Coyote Consulting. Full skill + docs: [Coyote Resources — JD Scorer UK](https://www.notion.so/364bea2c53d8812492c1cd5c1298d1c0)*
```

## Output format options

Default is Markdown (the template above). The user can request alternate formats by appending a flag or natural phrasing to their JD paste:

| Format | Trigger phrases | When to use |
|---|---|---|
| Markdown (default) | None | Copy-paste into Notion, Slack, email, LinkedIn comments |
| HTML | "as HTML", "html version", "html output", "--html" | Screenshot-ready, embed in Notion as web bookmark, save as .html for sharing |
| Plain text | "plain text", "no markdown", "--text" | Recruiter emails, ATS forms, anything that strips formatting |
| Compact summary | "summary only", "tl;dr", "--compact" | Single-paragraph fit verdict for quick triage |

If multiple formats are requested, produce all of them in sequence.

### HTML template

When HTML is requested, produce a standalone HTML document with inline CSS using Coyote brand colours. The template is screenshot-ready at 760px width.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>JD Fit Report — [Role]</title>
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
  .score-block { text-align: center; margin: 2rem 0; }
  .score-number { font-size: 4rem; font-weight: 700; color: var(--coyote-orange);
    display: inline-block; padding: 0 1.5rem; }
  .score-rationale { font-style: italic; opacity: 0.9; margin-top: 0.5rem; }
  .criterion { margin: 1rem 0; padding: 0.75rem 1rem; background: var(--coyote-mid);
    border-left: 3px solid var(--coyote-orange); border-radius: 4px; }
  .criterion-title { font-weight: 600; color: var(--coyote-orange); }
  .evidence { font-style: italic; opacity: 0.85; font-size: 0.9rem; margin-top: 0.3rem; }
  .flag { background: var(--flag-bg); padding: 0.75rem 1rem; border-radius: 4px;
    border-left: 3px solid #C04848; margin: 0.5rem 0; }
  .think { background: var(--think-bg); padding: 0.75rem 1rem; border-radius: 4px;
    border-left: 3px solid #6FA86F; margin: 0.5rem 0; }
  .tailoring { background: var(--coyote-mid); padding: 1rem 1.25rem; border-radius: 8px;
    border-left: 3px solid var(--coyote-orange); margin: 1rem 0; }
  .footer { margin-top: 2.5rem; padding-top: 1rem; border-top: 1px solid var(--coyote-mid);
    font-size: 0.85rem; opacity: 0.75; text-align: center; }
  .footer a { color: var(--coyote-orange); text-decoration: none; }
</style>
</head>
<body>
  <h1>JD Fit Report</h1>
  <div class="meta">
    <strong>Role:</strong> [extracted title]<br>
    <strong>Firm:</strong> [extracted firm or "Not specified"]<br>
    <strong>Role type:</strong> [Permanent / Contract / etc.]<br>
    <strong>Compensation:</strong> [salary or day rate, or "Not specified"]<br>
    <strong>Location:</strong> [extracted or "Not specified"]<br>
    <strong>IR35</strong> (contract only): [Outside / Inside / Not specified / PAYE]
  </div>
  <p style="opacity: 0.85;"><strong>Scored against your criteria:</strong> [one-line summary]</p>

  <div class="score-block">
    <div class="score-number">[X] / 10</div>
    <div class="score-rationale">[one-line rationale]</div>
  </div>

  <h2>Top 3 selection criteria</h2>
  <div class="criterion">
    <div class="criterion-title">1. [Criterion 1]</div>
    <div class="evidence">Evidence: "[quoted phrase]"</div>
  </div>
  <div class="criterion">
    <div class="criterion-title">2. [Criterion 2]</div>
    <div class="evidence">Evidence: "[quoted phrase]"</div>
  </div>
  <div class="criterion">
    <div class="criterion-title">3. [Criterion 3]</div>
    <div class="evidence">Evidence: "[quoted phrase]"</div>
  </div>

  <h2>Exclusion flags</h2>
  <div class="flag">[Flag 1]</div>
  <div class="flag">[Flag 2]</div>

  <h2>Think twice before applying</h2>
  <div class="think"><strong>1.</strong> [Observation 1]</div>
  <div class="think"><strong>2.</strong> [Observation 2]</div>
  <div class="think"><strong>3.</strong> [Observation 3]</div>

  <h2>Tailoring angle</h2>
  <div class="tailoring">[paragraph]</div>

  <div class="footer">
    Built by <strong style="color: var(--coyote-orange);">Coyote Consulting</strong>.
    Full skill + docs: <a href="https://www.notion.so/364bea2c53d8812492c1cd5c1298d1c0">Coyote Resources — JD Scorer UK</a>
  </div>
</body>
</html>
```

For HTML output, save to a file in the user's working folder (e.g., `jd-fit-report-[role-slug]-[YYYY-MM-DD].html`) and provide a computer:// link so they can open it directly. Do not paste raw HTML into chat unless the user explicitly asks.

## Scoring rubric (0-10 anchors)

Anchor against the user's stated criteria. Do not default to assumptions the user did not state.

| Score | Meaning |
|---|---|
| 9-10 | Exceptional fit. Role family, seniority, sector, stack, rate/salary, location all align. No deal-breakers triggered. |
| 7-8 | Strong fit. 1-2 minor gaps vs profile, addressable in cover note. No deal-breakers. |
| 5-6 | Plausible fit. Material gaps in 1-2 axes (scope, sector, stack, seniority). |
| 3-4 | Weak fit. Significant mismatch on multiple axes. |
| 0-2 | Hard no. User deal-breaker triggered, or fundamental role-family / seniority / sector mismatch. |

The score must reference specific JD language AND specific profile criteria (met or violated). Never score 7 by default.

## Top 3 selection criteria extraction

Look for, in priority order:

1. **Repetition**: phrases appearing 2+ times across the JD.
2. **Deal-breaker language**: "must have", "essential", "non-negotiable", "minimum X years".
3. **Quantified asks**: "owning £Xm budget", "team of N", "X% growth".
4. **Operating model verbs**: "build", "scale", "transform", "turnaround", "embed", "integrate".

Quote source phrases verbatim. No paraphrasing.

## UK exclusion glossary

Library of UK-specific JD patterns. Each pattern only flags when it conflicts with a user-stated criterion.

| Pattern | JD signals | Flag when user profile says... |
|---|---|---|
| IR35 unclear (contract) | No mention of IR35 / inside / outside / umbrella / PAYE on a contract role | contract_type is Outside IR35 |
| Inside IR35 / PAYE stated (contract) | "Inside IR35", "PAYE", "umbrella required", "umbrella company" | contract_type is Outside IR35 (hard exclude) or Open (flag) |
| Outside IR35 stated (contract) | "Outside IR35", "limited company", "B2B engagement" | contract_type is permanent-only (flag) |
| Day rate below floor (contract) | Explicit day rate stated below day_rate_floor | day_rate_floor set |
| Day rate missing (contract) | Contract role with no day rate or rate range stated | day_rate_floor set |
| Salary below floor (perm) | Explicit salary stated below salary_floor | salary_floor set |
| Salary missing (perm) | Permanent role with no salary or range stated | salary_floor set |
| Clearance required | "SC", "DV", "BPSS", "security cleared", "must be eligible" | clearance says user does not hold it |
| Office-only | "Onsite", "5 days a week", "no remote", "in-office" | location says remote or hybrid preferred |
| Hybrid duration mismatch | "2-3 days/week onsite" on a long engagement | location specifies max days/week or max duration shorter than role |
| ERP / SAP / Workday focus | "SAP", "S/4HANA", "Workday", "Oracle Fusion", "Finance Transformation", "Finance ERP", "ERP rollout" | sectors_exclude contains ERP-family terms |
| OTC / S2C / P2P core scope | "Order-to-Cash", "Sales-to-Cash", "Procure-to-Pay" as primary deliverable | Same as ERP family |
| Permanent only when contract sought | "Permanent", "FTE", "full-time employment" only | contract_type is contract-only |
| Contract only when perm sought | "Day rate", "outside IR35", "limited company" only | contract_type is permanent-only |
| Buzzword inflation | 5+ vague terms with no concrete deliverable | Always surface as "Think twice" candidate |
| Title over-claims scope | Title says Director/Head but body lists IC or PMO tasks ("co-ordinate", "track", "support", "manage RAID log") | Always surface as "Think twice" |
| Title under-claims scope | Title says PO/PM/Lead but body spans Director-grade work (transformation delivery, exec governance, multi-team leadership, P&L, offshore SI oversight) | Always surface as "Think twice" — signals mis-scoped brief or recruiter buying down day rate via under-titling |
| Consulting-led delivery | "Big 4", "top-tier strategy consulting", offshore SI model | Surface as "Think twice" — risk of figurehead-only role |
| Org maturity warning | "Recently restructured", "high-growth", "transition", "first hire in this role" | Always surface as "Think twice" |

## UK recruiter context glossary

Some UK recruiter brands have characteristic role-shaping patterns. When the recruiter (or staffing brand) is named in the JD, surface the context as additional grounding in the Top 3 or Think Twice sections. This is **context, not a flag** — never auto-exclude a role based on the recruiter alone.

| Recruiter | Typical pattern | Useful framing |
|---|---|---|
| Empresaria, Hays, Robert Half | Generalist staffing, often umbrella / PAYE, FS-heavy | Expect Inside IR35 by default. Outside IR35 conversions rare. |
| Investigo, La Fosse, BIE Executive | Mix of contract and perm, senior leadership focus | More likely Outside IR35 if contract. Brief shape negotiable. |
| Robert Walters, Michael Page | Perm-heavy, mid-senior | Salary range usually disclosed. Contract roles often umbrella. |
| Harnham, Annapurna | Data/analytics specialist, contract-heavy | Domain-narrow but often Outside IR35. |
| PSD Group, Riviera, La Fosse Programmes | Senior tech/digital interim, transformation | Strong fit for Director/Principal contract scoring. |
| Free-Work, Comet (FR-origin) | Freelance platforms, mostly FR market | Surface that the listing may be FR-shaped even when scoping a UK gig. |
| Big 4 / Top consulting subcontract | Job advertised by a recruiter for a Big 4 delivery seat | Always trigger "consulting-led delivery" flag in Think Twice. |

If the recruiter is unfamiliar, do not invent context. Surface them neutrally as "Recruiter: [name] (no banked context)".

## "Think twice" archetypes

Pick 2 to 3 per report. Always grounded in JD phrases.

- **Title vs reality gap**: title says Director, day-to-day reads as PMO.
- **Hidden scope**: bundles GTM + delivery + ops = 1.5 FTE problem.
- **Market context**: salary 15%+ below market for the user's seniority.
- **Org maturity**: recent restructure, multiple failed predecessors, ambiguous reporting line.
- **Sector trap**: tooling lock-in (Salesforce, SAP) reduces transferability.
- **Stack mismatch**: legacy or single-vendor stack conflicts with nice-to-haves.
- **Geography**: hybrid pattern incompatible with stated location.
- **Buzzword inflation**: too many keywords with no concrete deliverable.
- **Criteria the user didn't list**: gentle surfacing of something the user might not have thought to encode (e.g., language requirement, travel, on-call).

Generic "watch for scope creep" is not allowed. Every observation must quote a JD phrase.

## Tailoring angle rules

One paragraph, ~80 words. Voice: confident, direct, peer-to-peer. Tell the user:

1. Which past role or proof point to lead with in the summary.
2. Which 1-2 metrics to surface in the top 4 bullets.
3. Which technology / methodology to name-check.
4. What to deprioritise or omit.

Examples of voice: "Lead with the Sky CTI transformation. Drop the Nokia pre-sales context. Name-check value-stream design and OKR governance in the summary." Not "you might want to consider".

## Few-shot example (anonymised real UK Outside-IR35 contract role)

> The example below is a contract scoring. Permanent role scoring follows the same template, swapping the IR35 line for *(not applicable)*, surfacing salary range instead of day rate, and matching against `salary_floor` instead of `day_rate_floor`. All other sections behave identically.


### Input JD

```
Product Principal / Programme Director — Healthcheck Engagement (Synectics)

We are recruiting on behalf of a leading UK consultancy for a Product Principal / Programme Director to lead a high-stakes healthcheck engagement on a regulated-sector client account. The role is structured outside IR35 via a B2B consulting engagement model.

You will:
- Run a 6-week diagnostic across product, programme, and engineering layers.
- Interview stakeholders from C-suite to delivery teams (target: 50+ interviews).
- Produce a 30-page diagnostic report and 3-5 year transformation roadmap.
- Present findings to the client's executive committee.
- Coach a small in-house product team on operating model and discovery practice.

The successful candidate will demonstrate:
- 10+ years of Programme / Product leadership experience.
- Track record in C-suite engagement and executive committee reporting.
- Strong continuous discovery and product operating model expertise.
- Experience in regulated sectors (financial services, healthcare, media).
- Confidence presenting to non-technical executive audiences.

This is a 6-week initial engagement with potential extension. Day rate £750-900 depending on experience. London-based with hybrid working (2-3 days per week onsite).
```

### Example user profile

```yaml
role_family: "Programme Director / Head of Transformation"
seniority: "Director / Principal"
sectors_target: ["SaaS", "Media", "Telco", "FinTech"]
sectors_exclude: ["ERP", "SAP", "Finance Transformation"]
contract_type: "Outside IR35 contract"
day_rate_floor: 700
location: "UK remote, London hybrid OK, Bordeaux preferred"
clearance: "No SC / DV (non-UK passport)"
must_have_skills: ["cloud delivery", "value stream design", "OKR governance", "executive communication"]
deal_breakers: ["ERP implementations", "PMO support roles", "Inside IR35"]
cv_summary: "20+ years at Sky, WBD, Disney+, Nokia, BT. Transformation between C-suite strategy and engineering execution. Owned £10M P&L at Nokia. Led Sky CTI cost transformation (-40% opex). Strong cloud delivery (AWS/K8s), value-stream design, OKR governance, pre-sales."
```

### Expected output

```markdown
# JD Fit Report

**Role**: Product Principal / Programme Director — Healthcheck Engagement
**Firm**: Not specified (consultancy intermediary; underlying client is regulated-sector)
**Day rate / salary**: £750-900 per day
**Location / remote policy**: London, 2-3 days per week onsite (hybrid)
**IR35**: Outside (B2B consulting engagement model stated)

**Scored against your criteria**: Programme Director, Outside IR35, £700+/day, sectors target SaaS/Media/Telco/FinTech, deal-breakers include PMO support and ERP

## Fit Score: 8 / 10

Strong fit. C-suite engagement, programme leadership, continuous discovery, and regulated-sector exposure all land directly on your stated must-haves. Day rate clears your £700 floor. One axis to verify: sector (regulated could mean financial services ERP-adjacent rather than media/telco) and the hybrid pattern given Bordeaux base.

## Top 3 selection criteria

The hiring manager will filter on these in week one. Mirror this language in your CV summary and cover note.

1. **C-suite engagement at executive committee level** — Evidence: "Present findings to the client's executive committee", "Confidence presenting to non-technical executive audiences"
2. **Product operating model + continuous discovery craft** — Evidence: "Strong continuous discovery and product operating model expertise", "Coach a small in-house product team on operating model and discovery practice"
3. **Regulated-sector track record** — Evidence: "Experience in regulated sectors (financial services, healthcare, media)"

## Exclusion flags

- Hybrid pattern (2-3 days/week onsite in London) is incompatible with Bordeaux base unless TGV commute is acceptable. Verify before accepting.

## Think twice before applying

1. The JD says "regulated sectors (financial services, healthcare, media)". If the underlying client is financial services and the diagnostic touches Finance ERP or core banking, this drifts toward your stated deal-breaker. Ask the recruiter to name the sector before the first call.
2. "Coach a small in-house product team" is a coaching deliverable layered onto a 6-week diagnostic. That is 1.3 to 1.5 FTE of work in a 6-week window. Clarify whether the coaching is structured (workshops, playbooks) or expected as continuous mentoring you absorb alongside the diagnostic.
3. The 50+ stakeholder interviews and 30-page report in 6 weeks is an aggressive cadence. Workable, but ask whether a research analyst or junior is supporting interview synthesis, or whether you own it solo.

## Tailoring angle

Lead with the Sky CTI cost transformation (-40% opex) as your headline regulated-context proof point, and pair it with the Disney+ 1M+ user product operating model rollout to cover continuous discovery. Name-check value-stream design and OKR governance in the summary. Drop the Nokia pre-sales detail unless directly asked. Surface "30-page diagnostic + executive committee reporting" verbatim in your top bullet, matching the JD's own framing.

---
*Built by Coyote Consulting. Full skill + docs: [Coyote Resources — JD Scorer UK](https://www.notion.so/364bea2c53d8812492c1cd5c1298d1c0)*
```

## Operating rules

- **Never invent JD content**. If the JD does not state IR35, do not assume it. Flag "Not specified".
- **Never invent exclusion flags** the user did not ask for. The glossary patterns are matched against user criteria.
- **Always quote source phrases verbatim** in the Top 3 and Think Twice sections.
- **Never default the score to 7**. Force calibration against the rubric.
- **The Coyote footer stays** on every output. It is the brand carrier.
- **Profile reads are silent**. Do not announce "reading your profile" — just use it.
- **No em dashes** in the output. The user requested this and it is brand-consistent.
