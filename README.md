# skills

Agent skills I use with Claude Code. Most of them chain into one flow, from planning a change to an open PR with passing checks.

## Install

```sh
npx skills add felixpherry/skills
```

To see the list or install one skill:

```sh
npx skills add felixpherry/skills --list
npx skills add felixpherry/skills --skill unslop
```

Several skills call others by name, like babysit calling fix-ci. Installing all of them is the simplest way to keep those chains working.

## The flow

1. **plan-with-me** plans the change with you before any code gets written.
2. **approve-plan** turns the plan into a spec and a task list, then starts ship-plan in its own session.
3. **ship-plan** runs a task loop, checks the work against the plan, reviews it, and opens a PR.
4. **babysit** keeps the PR mergeable until you merge it.

## Plan and ship

| Skill | What it does |
|---|---|
| plan-with-me | Traces the code, asks questions with lettered options, and ends with a short plan to approve. |
| approve-plan | Writes the spec and task list, picks the loop, model and effort, and starts an unattended run. |
| ship-plan | Takes an approved plan to an open PR with nobody watching. Never merges. |
| run-simple-loop | Works through the plan task by task, with tests and a commit per phase. It's the everyday default. |
| run-phased-loop | Adds a full test run, a review and notes after every phase. For work where later phases depend on earlier ones. |
| run-micro-loop | Runs a small, low-risk plan straight through and commits once at the end. |
| check-gaps | Lists every gap between the work and its acceptance criteria. Also reviews a teammate's PR against its Jira ticket. |
| hand-off | Writes a handoff note and starts a fresh agent on it in a new session, with its own worktree for code work. |

## Review and fix PRs

| Skill | What it does |
|---|---|
| interrogate | Four agents review the same change for correctness, security, structure and tests. It merges what they find and sorts it by what to act on. |
| review-code | Reviews the changes since a commit or branch against the repo's coding standards and the original spec. |
| check-blast-radius | Finds what a change could break outside the diff, and runs real code to prove the one fact it's safe because of. |
| deslop | Removes AI slop from a branch's code changes. |
| make-pr-easy-to-review | Cleans up commit history and rewrites the PR description for reviewers. The code stays the same. |
| babysit | Fixes failing CI, merge conflicts and simple review comments on an open PR. Never replies to reviewers or merges. |
| fix-ci | Reads the failing checks and fixes them until they pass. |
| fix-merge-conflicts | Resolves merge conflicts and checks that the build and tests still pass. |
| get-pr-comments | Turns a PR's review comments into a short to-do list, most important first. |

## Understand code

| Skill | What it does |
|---|---|
| explain-how | How code works: the architecture, the runtime flow, and where things live. |
| explain-why | Why code is the way it is. Searches git history, PRs, tickets, docs and chat, and keeps what's known apart from what's guessed. |
| teach | Runs explain-how and explain-why and turns what they find into one plain explanation. |
| read-ticket | Reads a Jira ticket in full, every field, comment and attachment, and asks for anything it can't open. |

## Write

| Skill | What it does |
|---|---|
| unslop | Cuts AI tells from any writing. |
| bro | Restates the last message in plain words. |
| catch-me-up | Sums up what changed in the chat since your last message, and what needs your call. |
| write-confluence-doc | Writes Confluence pages people can skim, with bold claims, tables and a TL;DR up top. |
| write-investigation | Writes an engineering investigation as a story, with evidence for every claim. |
| write-typescript | TypeScript rules for types, narrowing, validation at boundaries and tests. |

## Other

| Skill | What it does |
|---|---|
| prototype | Builds a throwaway prototype to answer a design question. |
| run-arena | Runs several agents at the same task, picks the best attempt, and merges in the best parts of the others. |
| audit-skills | Checks a skills folder against Anthropic's authoring guide and fixes only what you approve. |
| add-db-connection | Adds a MySQL database to vim-dadbod-ui in Neovim, optionally through an SSH bastion. |

## What they need

- **The GitHub CLI.** babysit, fix-ci, get-pr-comments, make-pr-easy-to-review, review-code, check-gaps, explain-why and ship-plan call `gh`.
- **orb, a terminal multiplexer for coding agents.** approve-plan, hand-off, ship-plan, plan-with-me and run-arena use it to start agents in their own sessions and panes.
- **[lavish-axi](https://github.com/kunchenguid/lavish-axi).** plan-with-me and audit-skills show plans and reviews as pages you can click through.
- **Jira and Confluence access.** read-ticket and check-gaps read Jira tickets. write-confluence-doc writes Confluence pages.

## Credits

Many of these skills started from other people's work. pstack by Lauren Tan, its Claude Code port by Michael Denyer, and Matt Pocock's skills are the main sources. [NOTICE.md](NOTICE.md) lists which skill came from where, and each skill names its source in its `based-on` line.

## License

MIT. See [LICENSE](LICENSE).
