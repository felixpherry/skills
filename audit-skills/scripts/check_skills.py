"""Mechanical checks for agent skills, from Anthropic's skill authoring best practices.

Usage: python3 -I check_skills.py <skills folder | one skill folder> [--only a,b] [--private w1,w2] [--known k1,k2] [--skills-root DIR] [--json]

Prints one finding per line: skill, file:line, rule, level, message. Levels: fix (breaks a rule), check (look at it), note (fine for Claude Code, matters elsewhere).
Exits 1 when any finding has level fix.
"""
import argparse, json, re, sys
from pathlib import Path

NAME_RE = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
PORTABLE_KEYS = {'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools'}
CLAUDE_CODE_KEYS = {'when_to_use', 'argument-hint', 'arguments', 'disable-model-invocation', 'user-invocable', 'paths', 'model',
                    'effort', 'context', 'agent', 'hooks', 'shell', 'disallowed-tools', 'background'}
BUILT_IN = {'simplify', 'loop', 'run', 'init', 'review', 'security-review', 'code-review', 'update-config', 'keybindings-help',
            'claude-in-chrome', 'skill-doctor', 'skill-creator'}
FIRST_PERSON = re.compile(r"^(I|I'm|I'll|We|You)\b|\b(I can|I will|I'll|let me)\b")
TRIGGER = re.compile(r'\b(use|when|whenever|trigger)\b', re.I)
OUTSIDE = re.compile(r'(~/|\$HOME\b|/Users/|/home/)[^\s`)"\']*')
WINDOWS = re.compile(r'\b[\w.-]+\\[\w.-]+\.\w{1,5}\b')
SKILL_REF = re.compile(r'`/?([a-z0-9]+(?:-[a-z0-9]+)*)`\s+skill\b|\b([a-z0-9]+(?:-[a-z0-9]+)+)\s+skill\b|`/([a-z0-9]+(?:-[a-z0-9]+)+)[\s`]')
IPV4 = re.compile(r'\b(?!127\.|0\.0\.0\.0)(?:\d{1,3}\.){3}\d{1,3}\b')
DATED = re.compile(r'\b(as of|since|until|before|after)\s+(\d{4}|(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|jun|jul|aug|sept?|oct|nov|dec)\b)', re.I)
LOCAL_LINK = re.compile(r'\]\((?!https?:|mailto:|#)([^)\s]+)\)')
TOC = re.compile(r'^#+\s*(contents|table of contents)\b', re.I | re.M)


def frontmatter(text):
    """Top-level keys of the leading --- block, with their values, plus the body's first line number."""
    lines = text.split('\n')
    if not lines or lines[0].strip() != '---':
        return None, 1
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == '---'), None)
    if end is None:
        return None, 1
    keys, key = {}, None
    for line in lines[1:end]:
        m = re.match(r'^([A-Za-z0-9_-]+):\s*(.*)$', line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            keys[key] = '' if value in ('>', '|', '>-', '|-') else value.strip('"\'')
        elif key and line.startswith((' ', '\t')):
            keys[key] = (keys[key] + ' ' + line.strip()).strip()
    return keys, end + 2


def audit(skill_dir, known, private):
    out = []
    name = skill_dir.name
    add = lambda f, line, rule, level, msg: out.append({'skill': name, 'file': f, 'line': line, 'rule': rule, 'level': level, 'message': msg})
    text = (skill_dir / 'SKILL.md').read_text(errors='replace')
    fm, body_start = frontmatter(text)
    if fm is None:
        add('SKILL.md', 1, 'frontmatter', 'fix', 'no --- frontmatter block at the top')
        fm = {}
    n = fm.get('name', '')
    if not n:
        add('SKILL.md', 1, 'name', 'fix', 'name is missing')
    else:
        if n != name:
            add('SKILL.md', 1, 'name', 'fix', f'name "{n}" differs from the folder "{name}"')
        if len(n) > 64 or not NAME_RE.match(n):
            add('SKILL.md', 1, 'name', 'fix', 'name must be 64 characters at most: lowercase letters, digits, single hyphens')
        if re.search('anthropic|claude', n):
            add('SKILL.md', 1, 'name', 'fix', 'name must not contain "anthropic" or "claude"')
    d = fm.get('description', '')
    if not d:
        add('SKILL.md', 1, 'description', 'fix', 'description is missing')
    else:
        if len(d) > 1024:
            add('SKILL.md', 1, 'description', 'fix', f'description is {len(d)} characters; the limit is 1024')
        if re.search(r'<[A-Za-z/][^>]*>', d):
            add('SKILL.md', 1, 'description', 'fix', 'description contains an XML tag')
        if FIRST_PERSON.search(d):
            add('SKILL.md', 1, 'description', 'fix', 'description should be third person ("Turns X into Y"), not "I"/"you"')
        if not TRIGGER.search(d + ' ' + fm.get('when_to_use', '')):
            add('SKILL.md', 1, 'description', 'fix', 'description says what it does but not when to use it')
        if len(d) + len(fm.get('when_to_use', '')) > 1536:
            add('SKILL.md', 1, 'description', 'check', 'description plus when_to_use is cut at 1536 characters in the listing')
    for key in fm:
        if key not in PORTABLE_KEYS | CLAUDE_CODE_KEYS:
            add('SKILL.md', 1, 'frontmatter', 'fix', f'unknown key "{key}" is silently ignored; a typo, or belongs under metadata')
        elif key in CLAUDE_CODE_KEYS:
            add('SKILL.md', 1, 'portability', 'note', f'"{key}" works in Claude Code only; claude.ai and the API reject it')
    body_lines = len(text.split('\n')) - body_start + 1
    if body_lines > 500:
        add('SKILL.md', body_start, 'length', 'fix', f'body is {body_lines} lines; keep it under 500 and move detail to reference files')

    for f in sorted(p for p in skill_dir.rglob('*') if p.is_file()):
        rel = f.relative_to(skill_dir).as_posix()
        try:
            lines = f.read_text().split('\n')
        except (UnicodeDecodeError, OSError):
            continue
        is_md = f.suffix == '.md'
        for i, line in enumerate(lines, 1):
            outside = sorted({m.group(0) for m in OUTSIDE.finditer(line)})
            if outside:
                add(rel, i, 'outside-path', 'check', f'{", ".join(outside)}: outside the skill; breaks on other machines and agents unless that is the point')
            if is_md and WINDOWS.search(line):
                add(rel, i, 'windows-path', 'fix', 'use forward slashes in paths')
            for w in private:
                if re.search(r'\b' + re.escape(w) + r'\b', line, re.I):
                    add(rel, i, 'private', 'fix', f'mentions "{w}"')
            if IPV4.search(line):
                add(rel, i, 'private', 'check', 'an IP address')
            if is_md:
                if DATED.search(line):
                    add(rel, i, 'dated', 'check', 'time-sensitive wording; move old behaviour to an "old patterns" section')
                for m in SKILL_REF.finditer(line):
                    ref = next(g for g in m.groups() if g)
                    if ref not in known and ref != name:
                        add(rel, i, 'missing-skill', 'check', f'refers to "{ref}", which is not a skill here or a known built-in')
                for m in LOCAL_LINK.finditer(line):
                    target = m.group(1).split('#')[0]
                    if target and not (f.parent / target).exists():
                        add(rel, i, 'link', 'fix', f'links to {target}, which does not exist')
        if is_md and rel != 'SKILL.md' and len(lines) > 100 and not TOC.search('\n'.join(lines)):
            add(rel, 1, 'toc', 'fix', f'{len(lines)} lines with no contents section at the top')

    direct = {(skill_dir / m.group(1).split('#')[0]).resolve() for m in LOCAL_LINK.finditer(text)} | {(skill_dir / 'SKILL.md').resolve()}
    for ref in sorted(direct):
        if ref.suffix == '.md' and ref.is_file() and ref.name != 'SKILL.md':
            for n2 in LOCAL_LINK.finditer(ref.read_text(errors='replace')):
                t = n2.group(1).split('#')[0]
                if t.endswith('.md') and (ref.parent / t).is_file() and (ref.parent / t).resolve() not in direct:
                    add(ref.relative_to(skill_dir.resolve()).as_posix(), 1, 'nested-ref', 'fix', f'links on to {t}; keep references one level deep from SKILL.md')

    based_on = re.search(r'^\s+based-on:', text.split('\n---', 1)[0], re.M)
    notice = next((p for p in (skill_dir.parent / 'NOTICE.md', skill_dir.parent / 'NOTICE') if p.is_file()), None)
    if based_on and (notice is None or not re.search(r'\b' + re.escape(name) + r'\b', notice.read_text())):
        add('SKILL.md', 1, 'credit', 'fix', 'has based-on but the folder NOTICE does not credit it')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('folder')
    ap.add_argument('--only', default='')
    ap.add_argument('--private', default='')
    ap.add_argument('--known', default='')
    ap.add_argument('--skills-root')
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    folder = Path(a.folder).expanduser()
    skills = [folder] if (folder / 'SKILL.md').is_file() else sorted(p for p in folder.iterdir() if (p / 'SKILL.md').is_file())
    if a.only:
        skills = [s for s in skills if s.name in a.only.split(',')]
    root = Path(a.skills_root).expanduser() if a.skills_root else (folder.parent if (folder / 'SKILL.md').is_file() else folder)
    known = BUILT_IN | {p.name for p in root.iterdir() if (p / 'SKILL.md').is_file()} | {k for k in a.known.split(',') if k}
    private = [w for w in a.private.split(',') if w]
    findings = [f for s in skills for f in audit(s, known, private)]
    if a.json:
        print(json.dumps(findings, indent=1))
    else:
        for f in findings:
            print(f"{f['skill']}\t{f['file']}:{f['line']}\t{f['rule']}\t{f['level']}\t{f['message']}")
        print(f'{len(skills)} skills, {len(findings)} findings', file=sys.stderr)
    sys.exit(1 if any(f['level'] == 'fix' for f in findings) else 0)


if __name__ == '__main__':
    main()
