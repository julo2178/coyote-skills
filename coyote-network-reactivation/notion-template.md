# Notion Template — Network Reactivation Tracker

The recommended database structure for tracking reactivation outreach.

## Database schema

| Field | Type | Options / Notes |
| --- | --- | --- |
| Name | Title | Contact's full name |
| Current Role | Text | What they do now |
| Current Company | Text | Their current employer |
| LinkedIn URL | URL | Their profile link |
| How we met | Select | Sky UK / Disney+ / WBD / Nokia / BT / Alcatel-Lucent / Merapar / Consulting client / Personal / Other (customise to your career) |
| Era | Select | <2010 / 2010-2015 / 2015-2020 / 2020-2024 / 2024+ |
| Their role then | Text | Their role when you worked together |
| Relationship type | Select | Manager / Direct report / Peer / Cross-functional / Client / Vendor / Other |
| Strength | Select | 🟢 Strong / 🟡 Warm / ⚪ Faded |
| Geo | Select | Paris / London / Bordeaux / Other France / Other UK / Other EU / Rest of world / Unknown |
| Mutual connections | Number | LinkedIn count, useful for warm-intro chains |
| Status | Select | 📋 To triage / 🎯 To contact / 💬 DM sent / 🔄 Reply received / ☕ Catch-up booked / ✅ Active relationship / ❌ Out of reach |
| Priority | Select | 🔥 High / 🟡 Medium / ⚪ Low |
| Last contact date | Date | Last actual exchange |
| DM sent date | Date | When you sent the reactivation DM |
| Notes | Text | Free-form context |
| Coach reviewed | Checkbox | True once your coach has approved the DM |
| Coach comment | Text | Coach's tweaks or notes |
| Created | Created time | Auto-set |

## Recommended views

### 1. 📋 Triage queue (default, table)

Filter: `Status = 📋 To triage`
Sort: `Strength` ASC, then `Created` DESC
Show: Name, Current Role, Current Company, How we met, Strength, Geo, Mutual connections, Notes

This is where new entries land before they're worked. Where you start every triage session.

### 2. 🏢 By Company (board)

Group by: `How we met`
Sort: `Strength` ASC
Show: Name, Current Role, Current Company, Era, Strength, Status

Lets you see all Sky UK contacts together, all Disney+ together, etc. Useful when prepping for a session focused on a single chapter of your career.

### 3. 🔄 Outreach pipeline (board)

Group by: `Status`
Sort: `Priority` ASC, then `DM sent date` DESC
Show: Name, Current Company, How we met, Priority, Last contact date, DM sent date

Kanban view: To contact → DM sent → Reply received → Catch-up booked → Active relationship. The operational heartbeat of the campaign.

### 4. 👥 Coach review queue (table)

Filter: `Coach reviewed = unchecked AND Status != 📋 To triage`
Sort: `Priority` ASC
Show: Name, Current Company, How we met, Priority, Status, Notes

Surfaces only entries you've worked on but your coach hasn't reviewed yet. Send the link to your coach, they work through this view, you ship after they approve.

## How to install

**Option 1 — Manual (15 min)**

Create a new Notion database with the schema above. Add the 4 views. Done.

**Option 2 — Duplicate from a public template**

A duplicatable Notion template URL will be shared in the resource pack. Click the "Duplicate" button in the top-right of the template page, the database lands in your workspace ready to use.

## Tips for using the tracker

- **Don't chase a clean DB.** It's a working tool, not an archive. Vague entries ("Maria, designer at WBD around 2020") are valuable. The CSV import will fill many gaps automatically.
- **Triage in batches, don't drip-feed.** Set aside 30 minutes once a week to move 20-30 contacts from `📋 To triage` to `🎯 To contact` or `❌ Out of reach`. Avoid working the tracker every day, it becomes tedious.
- **Coach review is not optional.** The `👥 Coach review queue` view exists for a reason. Self-review fails at this scale.
- **Status changes drive the rhythm.** Update Status the moment something happens (DM sent, reply landed, catch-up booked). Stale Status = dead campaign.
