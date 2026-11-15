"""Check a Confluence HTML draft against the rules a script can see.

Usage: python3 -I check_draft.py <draft.html> [--title "<page title>"]
Prints one line per problem as <line>: <message> and exits 1, or prints nothing and exits 0.
"""
import argparse
import sys
from html.parser import HTMLParser
from pathlib import Path

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
DASHES = {"—": "em dash", "–": "en dash"}


class Draft(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.problems = []
        self.top_level = []
        self.headings = []
        self.links = []
        self.heading = None
        self.tldr_bullets = None
        self.list_depth_in_tldr = 0

    def line(self):
        return self.getpos()[0]

    def panel_type(self, attrs):
        kind = dict(attrs).get("data-type") or ""
        return kind if kind.startswith("panel-") else None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        panel = self.panel_type(attrs) if tag == "div" else None
        inside_panel = any(entry["panel"] for entry in self.stack)
        if tag.startswith("ac:") or tag.startswith("ri:"):
            self.problems.append((self.line(), f"storage XML <{tag}>: write plain HTML"))
        if tag == "time":
            self.problems.append((self.line(), "date chip <time>: write the date as plain text"))
        if tag == "table" and inside_panel:
            self.problems.append((self.line(), "table inside a panel"))
        if panel and inside_panel:
            self.problems.append((self.line(), "panel inside a panel"))
        if tag == "a":
            self.links.append((self.line(), attributes.get("href") or ""))
        if tag in HEADINGS:
            self.heading = {"tag": tag, "line": self.line(), "text": ""}
        if not self.stack:
            self.top_level.append({"tag": tag, "panel": panel, "line": self.line(), "text": "", "first": None})
        elif len(self.stack) >= 1 and self.stack[0]["panel"] and self.top_level[-1]["first"] is None and tag != "p":
            self.top_level[-1]["first"] = tag
        if self.tldr_bullets is not None and tag in {"ul", "ol"}:
            self.list_depth_in_tldr += 1
        if self.tldr_bullets is not None and tag == "li" and self.list_depth_in_tldr == 1:
            self.tldr_bullets += 1
        if tag not in VOID:
            self.stack.append({"tag": tag, "panel": panel})

    def handle_endtag(self, tag):
        if tag in HEADINGS and self.heading:
            text = " ".join(self.heading["text"].split())
            self.headings.append({**self.heading, "text": text})
            if self.tldr_bullets is not None and self.list_depth_in_tldr == 0:
                self.close_tldr()
            if self.heading["tag"] == "h2" and text == "TL;DR":
                self.tldr_bullets = 0
                self.tldr_line = self.heading["line"]
            self.heading = None
        if self.tldr_bullets is not None and tag in {"ul", "ol"}:
            self.list_depth_in_tldr -= 1
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]["tag"] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        if self.heading:
            self.heading["text"] += data
        if self.stack and self.top_level:
            if self.top_level[-1]["first"] is None and data.strip() and self.stack[0]["panel"]:
                self.top_level[-1]["first"] = "text"
        for character, name in DASHES.items():
            if character in data:
                offset = data[: data.index(character)].count("\n")
                self.problems.append((self.line() + offset, f"{name}: use a period, colon, comma, parentheses, or \"to\""))

    def close_tldr(self):
        if not 3 <= self.tldr_bullets <= 5:
            self.problems.append((self.tldr_line, f"TL;DR has {self.tldr_bullets} bullets: use three to five"))
        self.tldr_bullets = None


def check(text, title):
    draft = Draft()
    draft.feed(text)
    draft.close()
    if draft.tldr_bullets is not None:
        draft.close_tldr()
    problems = draft.problems

    for character, name in DASHES.items():
        if character in title:
            problems.append((0, f"{name} in the title"))

    anchors = {heading["text"].replace(" ", "-") for heading in draft.headings}
    for line, href in draft.links:
        if href == "#" or href == "":
            problems.append((line, "link with no target"))
        elif href.startswith("#") and href[1:] not in anchors:
            problems.append((line, f"same-page link {href} matches no heading"))

    blocks = draft.top_level
    info_panels = [block for block in blocks if block["panel"] == "panel-info"]
    if len(info_panels) != 1:
        problems.append((info_panels[1]["line"] if len(info_panels) > 1 else 1, f"{len(info_panels)} info panels: use exactly one"))
    if blocks and blocks[0]["panel"] != "panel-info":
        problems.append((blocks[0]["line"], "the page does not open with the info panel"))

    if not draft.headings or draft.headings[0]["tag"] != "h2" or draft.headings[0]["text"] != "TL;DR":
        problems.append((draft.headings[0]["line"] if draft.headings else 1, "the first heading is not <h2>TL;DR</h2>"))
    else:
        tldr_line = draft.headings[0]["line"]
        for block in blocks[1:]:
            if block["line"] >= tldr_line:
                break
            if block["panel"] != "panel-note":
                problems.append((block["line"], f"<{block['tag']}> sits between the info panel and the TL;DR: only a note panel may"))

    run = 0
    for block in blocks:
        run = run + 1 if block["panel"] else 0
        if run == 3:
            problems.append((block["line"], "three panels in a row"))
        if block["panel"] and block["first"] != "strong":
            problems.append((block["line"], "panel does not open with a bold claim"))

    return sorted(set(problems))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("draft")
    parser.add_argument("--title", default="")
    arguments = parser.parse_args()
    problems = check(Path(arguments.draft).read_text(), arguments.title)
    for line, message in problems:
        print(f"{line or 'title'}: {message}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
