---
name: read-ticket
description: Reads a Jira ticket completely, every custom field, comment and attachment included, then stops on anything it still can't open (like a Figma link) and asks for it. Use whenever a ticket key is referenced and the agent needs to know what the ticket asks for.
---

<instructions>

Read the referenced Jira ticket in full, open its assets, then gate on anything still missing. This skill reads;
it does not design, plan, or summarize.

## Fetch everything

The requirement usually does **not** live in `description`. Acceptance criteria,
implementation notes, design links and effort fields are all **custom fields**. A
hand-picked `fields` array silently drops them and you will miss the actual spec.

Use the Atlassian MCP v2 tools (`https://mcp.atlassian.com/v2/mcp`). Get `cloudId` once
from `getAccessibleAtlassianResources` (or pass the site hostname).

- **`getJiraIssue` with `view: "full"`.** The default compact view leaves custom fields
  out. Custom fields come back under `fields.customFields`, already labelled.
- **Comments separately.** `getJiraIssue` only counts them. Fetch them with
  `listJiraIssueComments` (find it with `discover`, run it with `executeRead`).

Then read **every** custom field that isn't empty, titled by its label. Do not skip a
field because its id is unfamiliar or its label sounds irrelevant — field ids differ per
site and per project, and the one you skip is the one holding the acceptance criteria.

Rich-text custom fields can come back as raw **ADF JSON** or HTML even when you asked for
markdown. Parse them yourself — headings, bullets, bold, links, tables, panels, and
`media` nodes — so no content is lost.

Also pull `parent` (epic context), `subtasks`, `issuelinks`, and comments when
`comment.total > 0`; decisions frequently live in comments rather than the body.

## Then open the assets

Attachments and recordings often hold the real spec. Open every one; don't judge from the
filename whether it looks relevant.

- **Attachments:** every entry in `fields.attachment` (ask `getJiraIssue` for
  `fields: ["attachment"]` if the full view left it out). Images embedded in the
  description or comments are attachments too. For each, get a download command with
  `downloadJiraIssueAttachment` (through `executeRead`) and run it, saving to a scratch
  folder outside the repo so nothing gets committed. Look at images; read text, CSV and
  documents. Delete the downloads when done.
- **Loom links:** read the transcript with `getLoomVideo` (`expand: ["transcript"]`).
- **Linked Confluence pages:** read them with `getConfluenceContent`.

## Then gate on blocking assets

Anything you still can't open is a **blocking asset**:

- **Every Figma link**, wherever it appears — description, a design custom field,
  comments — unless a Figma tool is connected and can read the frame.
- **Every attachment, recording or page that failed to open**, and every link behind a
  login you don't have.

**If there are any**, present them and stop. Never bury them in a prose paragraph. They
get their own `## Blocking assets` heading as a **numbered list**, one line per asset,
grouped by kind, each stating what it is and what you need from the user:

```
## Blocking assets

1. **Figma** — <link> (node 3747-434942). Which frame is authoritative? Can you paste
   the frame or its spec values?
2. **Attachment** — `SEO Bottom Content Template.csv` (240 B) failed to download. Can
   you share the file?
3. **Google Doc** — <link>, needs a login. Can you paste the relevant part?
```

Number continuously across kinds so the user can reply "1 and 3". Then wait. Do not
start planning, do not explore the codebase for a solution, do not offer a provisional
approach, and never guess at a design or a document you have not seen. Name whatever
step you are deferring so the user knows what resumes.

**If there are none**, continue straight into whatever comes next.

**Unattended** (inside a run nobody is watching, like ship-plan): list the blocking assets
in your output and continue without them instead of waiting.

</instructions>
