---
name: audit-skills
description: Audits a folder of agent skills against Anthropic's skill authoring best practices, then fixes only what the user approves. A script checks the mechanical rules (frontmatter limits, body length, reference depth, paths outside the skill, links to missing skills, private words); the agent judges descriptions, overlaps and usage. Findings go on a review page, and every edit is shown as a before/after diff and written only after the user says so. Use for "audit my skills", "clean up my skills", "are my skills any good", before publishing a skills folder, or after installing several new skills.
---

# Audit skills

Review a skills folder the way a careful maintainer would: measure, judge, show, then change one thing at a time with the user's OK.

## Rules

- **One item at a time.** Every add or edit gets a before/after diff page and is written only after the user answers "OK, write it". Removals and moves need only the approved list.
- **Move, never delete.** Removed skills and replaced files go to a `removed-<YYYY-MM-DD>/` folder next to the skills folder.
- **Leave skills installed by other tools alone.** Folders the skills folder's `.gitignore` lists, symlinks, and plugin skills get reported, with the fix pointed at their source.
- **Keep work files in `.plans/skills-audit-<YYYY-MM-DD>/`** inside the skills folder.

## Workflow

Copy this checklist into your notes and tick it as you go:

```
- [ ] 1. Measure: check script, usage, read every skill
- [ ] 2. Judge what the script can't
- [ ] 3. Report page, user picks the list
- [ ] 4. Apply the list, one item at a time
- [ ] 5. Re-check the folder and report
```

### 1. Measure

- **Run the check script** from this skill's folder:
  `python3 -I scripts/check_skills.py <skills folder> --private <words> --json > .plans/skills-audit-<date>/findings.json`
  - `--private`: when the folder will be published, the user's name, company, and internal host or project names, comma-separated. Take them from `git config user.name`, the user's email domain and the conversation; ask only if still unknown.
  - Levels: `fix` breaks a rule, `check` needs a look, `note` is fine for Claude Code but rejected by claude.ai and the API.
- **Get usage** in Claude Code with `claude -p "/skill-doctor"`: each skill's per-turn listing cost, uses and last use over the past week. Skip this on other agents.
- **Read every SKILL.md**, frontmatter first, then the body.

### 2. Judge

The script can't see these. Check each skill for:

- **Trigger:** the description says what it does and when to use it, in the third person, with the words a user would actually type. It fires on the right requests and stays quiet on the wrong ones.
- **Overlap:** two skills that answer the same request, or a skill that duplicates a built-in one.
- **Dead weight:** unused in the usage data, and no other skill depends on it. Weigh its per-turn listing cost.
- **Body:** explains what the model already knows, offers a menu where one default would do, uses two words for one thing, or leaves a fragile step without a script or a validate-and-retry loop.
- **Chains:** skills that call others by an old name, or build a command from a template the script can't resolve (like `/<kind>-loop`).
- **Credit:** a skill based on someone else's work names it in a `metadata: based-on:` line, and the folder's NOTICE credits it.

### 3. Report

Build one review page for the whole folder. Run `npx -y lavish-axi --help` and follow it to open the page and wait for feedback.

- **One row per skill:** its findings (script and judgment), its cost and usage, and a proposed action: keep, edit, merge, hide from the slash menu, or remove.
- **Checkboxes with your recommendation pre-ticked,** and one button that sends the chosen list back.
- **Lead with the few findings that matter.** A wall of `note` lines buries them.

### 4. Apply

Work through the approved list in order:

- **Removals and moves:** do them straight from the list, into the `removed-<date>/` folder.
- **Adds and edits:**
  1. Write the new version to `.plans/skills-audit-<date>/item<N>/<skill>/`.
  2. Check it: `python3 -I scripts/check_skills.py .plans/skills-audit-<date>/item<N>/<skill> --skills-root <skills folder>`. Fix until no `fix` findings remain.
  3. Build the diff page: `python3 -I scripts/build_diff_page.py <spec.json> <out.html>` (the spec format is in the script's docstring). Show it and wait for the verdict.
  4. On "OK, write it": back up the old files to `removed-<date>/`, copy the new ones in, and re-run the check with `--only <skill>`.
  5. On "change it first": revise and show a new diff.

### 5. Close

Re-run the check script on the whole folder. Report in a few lines: what changed, what's left open and why, and where the backups are.

## Sources

- Anthropic's skill authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Claude Code skills (frontmatter fields): https://code.claude.com/docs/en/skills
- Test the checker after changing it: `python3 -I scripts/test_check_skills.py`
