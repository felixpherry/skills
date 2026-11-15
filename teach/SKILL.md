---
name: teach
description: "Explains a body of work plainly so a person actually understands it. Runs explain-how and explain-why and weaves what they find into one clear account. Use for 'teach me this', 'help me really understand X', or 'explain this change or subsystem to me'."
metadata:
  based-on: "teach from pstack by Lauren Tan, via michael-denyer/pstack-claude (MIT)"
---

# Teach

**Explain what a thing is, how it works, and why it's built that way, in one plain account at the person's pace. The goal is that they understand it, not that you change anything.**

1. **Decide the few things they should walk away understanding.** Choose them from why they're asking (about to change it, reviewing it, debugging it, new to it) and what they already know, both read from the conversation, not quizzed out of them. Skip what they plainly know. Put the depth where their question is.
2. **Let explain-how and explain-why do the digging.** Read the code yourself to get oriented, then invoke explain-how for how it works and explain-why for why, in parallel, and blend what they find into one explanation. Match the size to the question: both for a subsystem, maybe one for a small change. Keep explain-why narrow by default since its full sweep is slow. Put the narrowing in the ask itself (a scoped question, git plus a source or two) so explain-why records the skipped categories, and widen it only when the reasons are the point. Reword freely, except explain-why's confidence language: its hedges are findings, not style.
3. **Start with a plain definition.** Name the thing and say what it is in general terms, the way a senior engineer would say it out loud, with its common name if it has one. Then tie it to the case in front of you ("in X, we use this to ...") and build from there: how it works, the deeper reasons, the edge cases. For each part, explain the problem it solves and how it actually works. Walk through what happens as the person does the thing (opens a long chat, scrolls up) when that makes it land. Listing functions and constants is reference, not teaching.
4. **Give the smallest complete answer first, then stop.** That is the definition in a sentence or two, one short sentence per main part, and at most one picture. Add layers when they ask. Never a wall of text.
5. **Keep it a conversation.** Offer to go deeper or move on, and follow their lead. No quizzes, and no asking them to say it back. When you would pause, stop and let them respond. Running one-shot with no live human, deliver only the smallest complete answer, then end with one line per layer you could add, without writing those layers.
6. **Show, and build the picture up.** Open the diff, the code, or the debugger when that is the fastest way to land it. Draw when a picture lands faster than words; a single simple point needs no figure. The first answer's one picture shows only the main parts. In the layers they ask for, anything with three or more moving parts gets a short series, not one diagram with everything: each diagram redraws the last and adds one part. To teach a flow from A to B to C, draw A to B, then redraw and add C, then redraw and add the return edge. One all-at-once diagram is a reference, not teaching.
7. **Match the medium to the idea.** A mermaid diagram fits a flow or structure where the labels carry the meaning. When the idea is spatial (layout, overlap, scroll position, a before and after), use an image-generation tool if you have one, drawn marker-on-whiteboard style with a few short labels, since image models garble long text. The build-up rule holds for generated images too.

## How it reads

Write in plain spoken English, the way you'd explain it to a colleague, and run it past the unslop skill. Be tight, not terse: cut filler and hedging, keep the part that makes it click. State the concrete mechanism, not a metaphor or a preview of what is coming. This is the target density: "Virtualization runs in two parts, one for rendering and one for loading from disk. When an item scrolls out past the buffer, both its DOM node and its in-memory data are evicted."

- **Just say it.** Don't print labels that announce the point ("the key insight", "TL;DR"), flag a part as important or hard ("this is the tricky part", "here is where it gets interesting"), or stage the pacing ("Pause").
- **Short sentences.** Normal sentence case. No em dashes. One or two commas per sentence; if clauses pile up, split them.
- **One name per concept,** kept throughout.
- **No mirror sentences** ("A without B, or B without A") **and no tidy closers** ("the rest follows").
- **The words in these steps are directions to you,** not headers or phrases to print.

Where the user's own instructions (CLAUDE.md, AGENTS.md) set a writing style or a way to show diagrams, such as a page instead of Mermaid in a terminal, theirs win.

**Reply:** the explanation itself, never a report about what you did. Lead with the main point, then the plain account of what it is, how it works, and why, and the threads worth chasing with explain-how or explain-why.
