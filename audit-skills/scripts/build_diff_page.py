"""Render one skill-change item as a Lavish before/after page.

Usage: python3 -I build_diff_page.py <spec.json> <out.html>
spec: {item, kind, title, summary: [html], files: [{label, why, old_path|old, new_path|new}], moves: [html], after: [html]}
"""
import html, json, sys
from pathlib import Path

spec = json.loads(Path(sys.argv[1]).read_text())
base = Path(sys.argv[1]).parent


def read(f, key):
    if f.get(key + '_path'):
        p = Path(f[key + '_path']).expanduser()
        if not p.is_absolute():
            p = base / p
        return p.read_text() if p.exists() else ''
    return f.get(key, '')


files = [{'label': f['label'], 'why': f.get('why', ''), 'old': read(f, 'old'), 'new': read(f, 'new')} for f in spec['files']]
lis = lambda xs: ''.join(f'<li>{x}</li>' for x in xs)
cards = ''.join(
    f'<section class="space-y-2"><h3 class="font-mono text-sm font-semibold">{html.escape(f["label"])}</h3>'
    f'<p class="text-sm text-base-content/70">{f["why"]}</p><div id="d{i}" class="rounded-box overflow-hidden border border-base-content/10"></div></section>'
    for i, f in enumerate(files))
moves = f'<section class="space-y-2"><h3 class="font-semibold">Files that move</h3><ul class="list-disc pl-5 text-sm space-y-1">{lis(spec["moves"])}</ul></section>' if spec.get('moves') else ''
after = f'<section class="space-y-2"><h3 class="font-semibold">After writing, I check</h3><ul class="list-disc pl-5 text-sm space-y-1">{lis(spec["after"])}</ul></section>' if spec.get('after') else ''
item = html.escape(str(spec['item']))
files_json = json.dumps(files).replace('</', '<\\/')

page = f'''<!doctype html>
<html lang="en" data-theme="luxury" data-lavish-annotate="on">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Item {item} diff</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daisyui@5.5.19/daisyui.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daisyui@5.5.19/themes.css">
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4.2.4/dist/index.global.js"></script>
<style>*,*::before,*::after{{box-sizing:border-box}} :where(.grid,.flex)>*{{min-width:0}} body{{background:var(--color-base-100);color:var(--color-base-content)}}</style>
</head>
<body>
<main class="max-w-5xl mx-auto px-4 py-8 space-y-8">
  <header class="space-y-2">
    <div class="flex flex-wrap gap-2 items-center"><span class="badge badge-neutral font-mono">item {item}</span><span class="badge badge-soft badge-warning">{html.escape(spec["kind"])}</span></div>
    <h1 class="text-3xl font-bold">{html.escape(spec["title"])}</h1>
    <ul class="list-disc pl-5 space-y-1">{lis(spec["summary"])}</ul>
  </header>
  {moves}
  {cards}
  {after}
  <form id="verdict" data-lavish-question="item-{item}" class="card card-border bg-base-200" data-lavish-annotate="off">
    <div class="card-body p-4 gap-3">
      <p class="font-semibold">Write this?</p>
      <textarea name="note" class="textarea w-full" rows="2" placeholder="What to change (leave empty if OK)"></textarea>
      <div class="flex flex-wrap gap-3">
        <button type="submit" name="v" value="ok" class="btn btn-primary">OK, write it</button>
        <button type="submit" name="v" value="change" class="btn">Change it first</button>
      </div>
    </div>
  </form>
</main>
<script type="module">
  import {{ FileDiff }} from "https://esm.sh/@pierre/diffs@1.2.10?bundle";
  const files = {files_json};
  files.forEach((f, i) => new FileDiff({{ theme: {{ light: "github-light", dark: "github-dark" }}, themeType: "dark", overflow: "wrap", diffStyle: "split" }})
    .render({{ containerWrapper: document.querySelector("#d" + i), oldFile: {{ name: f.label, contents: f.old }}, newFile: {{ name: f.label, contents: f.new }} }}));
  const form = document.getElementById("verdict");
  form.addEventListener("submit", (e) => {{
    e.preventDefault();
    const v = e.submitter?.value || "ok";
    const note = new FormData(form).get("note").trim();
    if (!window.lavish) return;
    const text = v === "ok" ? "Item {item}: OK, write it" + (note ? ". Note: " + note : "") : "Item {item}: change first: " + (note || "(see my annotations)");
    window.lavish.queuePrompt(text, {{ tag: "item-verdict", text, element: form, data: {{ item: "{item}", verdict: v, note }} }});
  }});
</script>
</body>
</html>
'''
Path(sys.argv[2]).write_text(page)
print(sys.argv[2])
