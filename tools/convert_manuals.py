#!/usr/bin/env python3
"""Convert a Sphinx singleindex.html into one Markdown file per source document.

usage: convert_manuals.py <singleindex.html> <outdir> <base-url> [--exclude REGEX]

Used to build skills/yocto-manuals/references/manuals/ from the official
docs.yoctoproject.org "singleindex.html" pages (one per release). Standard
library only. The source HTML is not stored in the repository.
"""
import html
import os
import re
import sys
from html.parser import HTMLParser

SKIP_TAGS = {"script", "style", "nav", "head", "footer"}
BLOCK = {"p", "div", "section", "table", "tr", "blockquote", "dl", "ul", "ol"}


class Conv(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.docs = {}          # docname -> list of chunks
        self.order = []
        self.cur = None
        self.out = []
        self.skip = 0
        self.pre = 0
        self.lists = []
        self.in_main = False
        self.hlevel = None
        self.ignore_depth = 0
        self.ignore_stack = []

    def emit(self, s):
        if self.cur is not None:
            self.docs[self.cur].append(s)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "") or ""
        if tag == "span" and (a.get("id") or "").startswith("document-"):
            name = a["id"][len("document-"):]
            self.cur = name
            if name not in self.docs:
                self.docs[name] = []
                self.order.append(name)
            return
        if tag in SKIP_TAGS or "headerlink" in cls or "wy-nav" in cls or "rst-footer" in cls:
            self.skip += 1
            self.ignore_stack.append(tag)
            return
        if self.skip:
            if tag == self.ignore_stack[-1] if self.ignore_stack else False:
                pass
            self.ignore_stack.append(tag)
            return
        if re.fullmatch(r"h[1-6]", tag):
            self.emit("\n\n" + "#" * int(tag[1]) + " ")
        elif tag == "pre":
            self.pre += 1
            self.emit("\n\n```\n")
        elif tag == "code" and not self.pre:
            self.emit("`")
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag in ("ul", "ol"):
            self.lists.append(tag)
            self.emit("\n")
        elif tag == "li":
            self.emit("\n" + "  " * (len(self.lists) - 1) + "- ")
        elif tag == "dt":
            self.emit("\n\n**")
        elif tag == "dd":
            self.emit("\n")
        elif tag == "br":
            self.emit("\n")
        elif tag in ("td", "th"):
            self.emit(" | ")
        elif tag in BLOCK:
            self.emit("\n\n")

    def handle_endtag(self, tag):
        if self.ignore_stack:
            # pop to matching tag
            while self.ignore_stack:
                t = self.ignore_stack.pop()
                if t in SKIP_TAGS or True:
                    pass
                if t == tag:
                    break
            if not self.ignore_stack:
                self.skip = 0
            return
        if re.fullmatch(r"h[1-6]", tag):
            self.emit("\n")
        elif tag == "pre":
            self.pre = max(0, self.pre - 1)
            self.emit("\n```\n")
        elif tag == "code" and not self.pre:
            self.emit("`")
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag in ("ul", "ol"):
            if self.lists:
                self.lists.pop()
            self.emit("\n")
        elif tag == "dt":
            self.emit("**")
        elif tag in BLOCK:
            self.emit("\n")

    def handle_startendtag(self, tag, attrs):
        if tag == "br" and not self.skip:
            self.emit("\n")

    def handle_data(self, data):
        if self.skip:
            return
        if self.pre:
            self.emit(data)
        else:
            self.emit(re.sub(r"\s+", " ", data))


# Keep public project addresses; replace personal ones so the repository carries no
# individual contact details or machine paths copied from manual examples.
PUBLIC_EMAIL = re.compile(r"@(lists\.[a-z.]+|example\.com|[a-z.]*yoctoproject\.org)$|^git@")


def sanitize(text):
    def email(m):
        addr = m.group(0)
        return addr if PUBLIC_EMAIL.search(addr) else "<email>"

    text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email, text)
    text = re.sub(r"/(home|Users)/(?!root\b|user\b)[A-Za-z0-9._-]+", r"/\1/user", text)
    text = re.sub(r"([A-Za-z]:\\Users\\)[A-Za-z0-9._-]+", r"\1user", text)
    return text


def tidy(text):
    text = sanitize(text)
    text = text.replace("¶", "")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\*\*\s*\*\*", "", text)
    # Sphinx wraps list item bodies in <p>; pull the first paragraph onto the bullet.
    text = re.sub(r"(?m)^([ ]*)- *\n+", r"\1- ", text)
    return text.strip() + "\n"


def main():
    src, outdir, base = sys.argv[1:4]
    exclude = None
    if len(sys.argv) > 5 and sys.argv[4] == "--exclude":
        exclude = re.compile(sys.argv[5])
    p = Conv()
    with open(src, encoding="utf-8") as f:
        p.feed(f.read())
    os.makedirs(outdir, exist_ok=True)
    for name in p.order:
        if exclude and exclude.search(name):
            continue
        body = tidy("".join(p.docs[name]))
        path = os.path.join(outdir, name + ".md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        header = (
            f"<!-- Source: {base}{name}.html (converted from singleindex.html). "
            "License: see LICENSE-docs.md in this folder. -->\n\n"
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(header + body)
        print(f"{len(body):>9} {path}")


if __name__ == "__main__":
    main()
