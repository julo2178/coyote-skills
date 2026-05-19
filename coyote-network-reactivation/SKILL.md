---
name: network-reactivation
description: Build and run a structured reactivation campaign for dormant LinkedIn contacts (ex-colleagues, ex-managers, ex-clients) you have lost touch with over the years. Triggers when the user mentions reconnecting with old contacts, reactivating their network, reaching out to former colleagues, building a list of past relationships, processing a LinkedIn connections export, drafting reconnection DMs, or asking how to reach out to people they have not spoken to in years. Use this skill whenever someone wants to systematically reconnect with their dormant professional network rather than send one-off messages, even if they do not explicitly use the word "reactivation". The skill produces a triage system, archetype-matched DM templates in EN and FR, and a workflow that prioritizes warmth over transactional outreach.
---

# Network Reactivation

A system for reconnecting with dormant warm relationships in a way that builds long-term capital instead of burning it.

## When this matters

People accumulate hundreds of professional relationships over a career. Most go cold. The classic mistakes when trying to reconnect:

1. **Bulk DM energy.** Generic openers ("Hope you're well!") that pattern-match instantly to mass outreach and get ignored.
2. **Transactional framing.** Leading with an ask (job, intro, advice) before re-establishing the relationship.
3. **No system.** One-off messages with no tracking, no review loop, no priority. Three weeks in, the campaign collapses.

This skill prevents all three by building structure first, then content second, with a coach-review loop baked in.

## Core principle

**Reconnect first. Intent comes later.**

Every opener written under this skill is purely relational. Zero mention of jobs, projects, products, or anything you might want from the contact. The relationship gets re-established before any ask is ever raised. This is not optional: it is what separates this approach from spammy reach-out templates.

## The five archetypes

People relate to you differently based on the original power dynamic. The same opener cannot work across all of them:

1. **Ex-manager** (they were senior to you) → respectful, anchored in a specific moment they led or taught
2. **Ex-peer** (same level, worked closely) → warm, equal footing, shared trench memory
3. **Ex-direct-report** (you managed them) → care-driven, invest in them not extract from them
4. **Ex-client** (they paid for your work) → non-transactional, prove no ask in opener
5. **Cross-functional / faded** (knew each other distantly) → low-pressure, easy out built in

Templates for each archetype in EN and FR live in `templates/dm-templates.md`.

## Workflow

### Phase 1 — Build the tracking infrastructure

Before any outreach, create a database (Notion, Airtable, or even a structured spreadsheet) with these fields:

**Identity**: Name, Current Role, Current Company, LinkedIn URL
**Relationship history**: How we met (company name), Era, Their role then, Relationship type (manager / peer / direct report / client / cross-functional), Strength (strong / warm / faded)
**Geo + density**: Geo (Paris / London / Bordeaux / etc.), Mutual connections count
**Outreach state**: Status (To triage / To contact / DM sent / Reply received / Catch-up booked / Active relationship / Out of reach), Priority, Last contact date, DM sent date, Notes
**Review layer**: Reviewed by coach (checkbox), Coach comment

A ready-to-use Notion template is referenced in `references/notion-template.md`.

### Phase 2 — Source the contact list

Two complementary sources, run in parallel:

**A. LinkedIn CSV export (breadth)**
1. Settings & Privacy → Data Privacy → Get a copy of your data → tick "Connections" only → Request archive
2. LinkedIn delivers the CSV by email in ~10 minutes
3. CSV contains: First Name, Last Name, URL, Email Address, Company, Position, Connected On

**B. Brain-dump (depth)**
For each major chapter of your career (employer, client, project), list the people you actually worked with daily. Names you remember without prompting are the warmest. Vague memories ("Maria something, designer") still go in: the CSV will fill the gaps.

### Phase 3 — Classify and triage

Using the script in `scripts/classify-csv.py` (or manually), enrich each CSV row with:
- `How we met` based on the Company field matched against the user's career history (provided as input)
- `Era` based on `Connected On` date
- All entries default to `Status = To triage` and `Strength = warm`

After classification, the user reviews the triage queue and sets:
- `Strength` (Strong / Warm / Faded)
- `Priority` (High / Medium / Low)
- `Relationship type` (Manager / Peer / Direct report / Client / Cross-functional)

This is a manual pass: only the user knows the relational context. Do not try to infer relationship type from job titles alone.

### Phase 4 — Draft DMs using templates

For each `To contact` entry, use the matching template from `templates/dm-templates.md`. Fill in the bracketed variables:
- `[First name]`
- `[specific moment]` — a concrete shared memory, never generic
- `[current company]`
- For ex-managers: a specific thing they taught or led
- For ex-peers: a specific shared trench moment
- For ex-direct-reports: a specific moment that earned your respect
- For ex-clients: a specific outcome from the engagement

If you cannot anchor the message in a specific memory, the contact is either too faded for a warm DM (use archetype 5: reintroduction) or you should skip them.

### Phase 5 — Coach review loop

Before sending, the user has a coach (LinkedIn visibility coach, mentor, or just a sharp peer) review every DM. The coach catches:
- Generic openers that slipped through
- Accidental ask in the close
- Tone mismatch with the original relationship
- Specifics that read as fabricated

Do not skip this step. Self-review fails because the writer is too close to the words.

### Phase 6 — Send and track

After coach approval:
1. Send the DM
2. Update the tracker: `Status = DM sent`, fill `DM sent date`
3. Log any reply: `Status = Reply received`
4. If a catch-up gets booked: `Status = Catch-up booked`
5. After the first real conversation: `Status = Active relationship`

### Phase 7 — Reply handling

When a contact replies, the second message is where most reconnection campaigns die. The user freezes, defaults to "let's grab coffee", and the warmth dissipates.

Reply-handling rules per archetype are in `templates/dm-templates.md`. The general principle: ask one question about *their* current work before offering anything about yours. Let them open the door if they want to. Never push.

## Anti-patterns to refuse

When drafting DMs under this skill, refuse to generate any of the following:

1. **Generic openers** — "Hope you're well!", "Long time no see!", "Hi [name], saw your profile and thought I'd reach out". These pattern-match to bulk DM and the contact deletes within 5 seconds.
2. **CV / portfolio / Calendly link in opener** — Even one link kills the warmth. The opener is text only.
3. **Mission, job, or product mention in the first message** — Save for after they reply AND ask what you are doing now.
4. **"Quick coffee?" close** — Implies obligation. Use "would love to hear what you are up to" instead.
5. **Apologising for losing touch** — Lowers your status. State it neutrally or skip it.
6. **Long monologues about the user's life** — They did not ask. One sentence max about the user, the rest is about them or the shared past.

If the user asks to draft a DM that violates one of these patterns, push back once with the reason and offer the corrected version.

## Output format for DM drafts

Always format DM drafts as follows so the user can copy-paste straight into LinkedIn:

```
=== [Contact Name] — [Archetype] ===

[Pre-flight check]
- Anchor: [the specific memory the message hooks on]
- Length: [word count]
- Pattern check: ✓ no generic opener, ✓ no ask, ✓ specific anchor, ✓ low-pressure close

[DM body — copy from here]
Hi [First name],

...

Best,
[Your name]
[End of DM]

[Reply-handling note]
If they reply: [archetype-specific guidance]
```

## Scope

This skill covers:
- Database schema design for relationship tracking
- LinkedIn CSV parsing and classification
- DM drafting across 5 archetypes in EN and FR
- Coach-review workflow
- Reply-handling guidance

This skill does not cover:
- Cold outreach to people you have never met (different methodology, do not reuse these templates)
- Sales prospecting (transactional by design, opposite framing)
- Recruiter outreach (use a recruiter-specific template, not these)

## References

- `templates/dm-templates.md` — Full DM templates, 5 archetypes × EN+FR + reply-handling
- `references/notion-template.md` — Database schema and 4 recommended views
- `references/anti-patterns.md` — Detailed anti-patterns with examples
- `scripts/classify-csv.py` — Optional script to bulk-classify a LinkedIn CSV export against a user-provided career history
