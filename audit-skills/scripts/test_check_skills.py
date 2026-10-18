"""Runs check_skills.py on a folder with one clean skill and one with planted problems.

Usage: python3 -I test_check_skills.py
"""
import json, subprocess, sys, tempfile
from pathlib import Path

CHECK = Path(__file__).with_name('check_skills.py')

GOOD = """---
name: good-skill
description: Turns meeting notes into a task list. Use when the user pastes notes and asks for next steps.
---

# Good skill

Read [the format](format.md), then hand off to the bad-skill skill.
"""

BAD = """---
name: wrong-name
description: I can help with anything.
color: blue
metadata:
  based-on: "something from someone (MIT)"
---

Run scripts\\fix.py, then read ~/.agents/rules.md and [notes](notes.md) and [gone](missing.md).
Ask the ghost-skill skill. Call acme for access, at 10.1.2.3. Updated before March.
"""

NOTES = '[more](deeper.md)\n' + 'line\n' * 120


def write(root, rel, text):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    write(root, 'good-skill/SKILL.md', GOOD)
    write(root, 'good-skill/format.md', '# Format\n\nOne task per line.\n')
    write(root, 'bad-skill/SKILL.md', BAD)
    write(root, 'bad-skill/notes.md', NOTES)
    write(root, 'bad-skill/deeper.md', 'deep\n')
    done = subprocess.run([sys.executable, '-I', str(CHECK), tmp, '--private', 'acme', '--json'], capture_output=True, text=True)
    findings = json.loads(done.stdout)

good = [f for f in findings if f['skill'] == 'good-skill']
assert good == [], f'the clean skill should have no findings, got {good}'

rules = {(f['rule'], f['level']) for f in findings if f['skill'] == 'bad-skill'}
expected = {
    ('name', 'fix'), ('description', 'fix'), ('frontmatter', 'fix'), ('windows-path', 'fix'), ('outside-path', 'check'),
    ('link', 'fix'), ('missing-skill', 'check'), ('private', 'fix'), ('private', 'check'), ('dated', 'check'),
    ('toc', 'fix'), ('nested-ref', 'fix'), ('credit', 'fix'),
}
assert rules == expected, f'missing {expected - rules}, unexpected {rules - expected}'
descriptions = [f['message'] for f in findings if f['skill'] == 'bad-skill' and f['rule'] == 'description']
assert len(descriptions) == 2, f'both first person and no trigger should be flagged, got {descriptions}'
assert done.returncode == 1, 'fix-level findings should exit 1'
print('ok')
