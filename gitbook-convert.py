#!/usr/bin/env python3
"""Convert the Mintlify MDX docs (docs-site) into GitBook-flavoured Markdown.

Input : /Users/arambarnett/Projects/monkeygun/docs-site  (mdx + docs.json + openapi.json + images)
Output: a fresh directory with .md pages, README.md, SUMMARY.md, .gitbook.yaml, api-reference/*.md
"""
import json, os, re, shutil, sys

SRC = '/Users/arambarnett/Projects/monkeygun/docs-site'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp/mgdocs-gitbook'

def rel_link(from_page, target):
    """'/guides/foo#x' from page 'concepts/bar' -> '../guides/foo.md#x'"""
    if not target.startswith('/'):
        return target
    path, _, anchor = target.partition('#')
    path = path.strip('/')
    if path == '':
        path = 'README'
    elif path == 'introduction':
        path = 'README'
    depth = from_page.count('/')
    prefix = '../' * depth
    out = f'{prefix}{path}.md'
    return out + (f'#{anchor}' if anchor else '')

def convert(page, text):
    # frontmatter
    m = re.match(r'---\n(.*?)\n---\n', text, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(':')
            fm[k.strip()] = v.strip().strip('"')
        text = text[m.end():]
    title = fm.get('title', page)
    desc = fm.get('description', '')

    # Protect fenced code blocks from transformations
    blocks = []
    def stash(mm):
        blocks.append(mm.group(0)); return f'@@BLOCK{len(blocks)-1}@@'
    text = re.sub(r'```.*?```', stash, text, flags=re.S)

    # CodeGroup -> tabs of code blocks (title from info string: ```ts Node)
    def codegroup(mm):
        inner = mm.group(1)
        tabs = []
        for ref in re.findall(r'@@BLOCK(\d+)@@', inner):
            blk = blocks[int(ref)]
            head = blk.split('\n', 1)[0]
            parts = head[3:].split(None, 1)
            lang = parts[0] if parts else ''
            label = parts[1] if len(parts) > 1 else lang
            blocks[int(ref)] = f'```{lang}\n' + blk.split('\n', 1)[1]
            tabs.append(f'{{% tab title="{label}" %}}\n@@BLOCK{ref}@@\n{{% endtab %}}')
        return '{% tabs %}\n' + '\n'.join(tabs) + '\n{% endtabs %}'
    text = re.sub(r'<CodeGroup>(.*?)</CodeGroup>', codegroup, text, flags=re.S)

    # Steps
    text = re.sub(r'<Steps>\s*', '{% stepper %}\n', text)
    text = re.sub(r'\s*</Steps>', '\n{% endstepper %}', text)
    text = re.sub(r'<Step title="([^"]*)">', r'{% step %}\n### \1', text)
    text = re.sub(r'</Step>', '{% endstep %}', text)
    # Tabs
    text = re.sub(r'<Tabs>', '{% tabs %}', text)
    text = re.sub(r'</Tabs>', '{% endtabs %}', text)
    text = re.sub(r'<Tab title="([^"]*)">', r'{% tab title="\1" %}', text)
    text = re.sub(r'</Tab>', '{% endtab %}', text)
    # Hints
    for tag, style in [('Tip', 'success'), ('Note', 'info'), ('Warning', 'warning'), ('Info', 'info')]:
        text = re.sub(rf'<{tag}>\s*', f'{{% hint style="{style}" %}}\n', text)
        text = re.sub(rf'\s*</{tag}>', f'\n{{% endhint %}}', text)
    # Accordions -> details
    text = re.sub(r'<AccordionGroup>\s*', '', text)
    text = re.sub(r'\s*</AccordionGroup>', '', text)
    text = re.sub(r'<Accordion title="([^"]*)">', r'<details>\n<summary>\1</summary>\n', text)
    text = re.sub(r'</Accordion>', '\n</details>', text)
    # Cards -> link list
    text = re.sub(r'<CardGroup[^>]*>\s*', '', text)
    text = re.sub(r'\s*</CardGroup>', '', text)
    def card(mm):
        attrs, body = mm.group(1), ' '.join(mm.group(2).split())
        t = re.search(r'title="([^"]*)"', attrs); h = re.search(r'href="([^"]*)"', attrs)
        link = rel_link(page, h.group(1)) if h else None
        head = f'[**{t.group(1)}**]({link})' if link else f'**{t.group(1)}**'
        return f'* {head} — {body}'
    text = re.sub(r'<Card([^>]*)>(.*?)</Card>', card, text, flags=re.S)
    # Update (changelog) -> heading
    text = re.sub(r'<Update label="([^"]*)" description="([^"]*)">', r'## \1 — \2', text)
    text = re.sub(r'</Update>', '', text)
    # Frames with video / img
    def frame(mm):
        attrs, body = mm.group(1), mm.group(2)
        cap = re.search(r'caption="([^"]*)"', attrs)
        caption = cap.group(1) if cap else ''
        v = re.search(r'<video[^>]*src="([^"]*)"[^>]*>', body)
        i = re.search(r'<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"', body)
        if v:
            poster = re.search(r'poster="([^"]*)"', body)
            out = f'{{% embed url="{v.group(1)}" %}}\n{caption}\n{{% endembed %}}'
            if poster: out = f'[![{caption}]({poster.group(1)})]({v.group(1)})\n\n' + out
            return out
        if i:
            return f'<figure><img src="{i.group(1)}" alt="{i.group(2)}"><figcaption><p>{caption}</p></figcaption></figure>'
        return body
    text = re.sub(r'<Frame([^>]*)>(.*?)</Frame>', frame, text, flags=re.S)
    # JSX string escapes like {'{id}'} -> {id}
    text = re.sub(r"\{'([^']*)'\}", r'\1', text)
    # internal links
    text = re.sub(r'\]\((/[^)]*)\)', lambda mm: f']({rel_link(page, mm.group(1))})', text)
    # restore code blocks
    text = re.sub(r'@@BLOCK(\d+)@@', lambda mm: blocks[int(mm.group(1))], text)
    # dedent: JSX bodies were indented; outside fences strip leading spaces, inside a fence strip the fence's own indent
    out_lines, fence_indent = [], None
    for line in text.split('\n'):
        if fence_indent is None:
            stripped = line.lstrip(' ')
            if stripped.startswith('```'):
                fence_indent = len(line) - len(stripped)
            out_lines.append(stripped)
        else:
            cut = min(fence_indent, len(line) - len(line.lstrip(' ')))
            l2 = line[cut:]
            out_lines.append(l2)
            if l2.lstrip().startswith('```'):
                fence_indent = None
    text = '\n'.join(out_lines)
    # tidy blank lines
    text = re.sub(r'\n{3,}', '\n\n', text).strip() + '\n'
    head = f'# {title}\n\n' + (f'{desc}\n\n' if desc else '')
    return head + text

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    docs = json.load(open(os.path.join(SRC, 'docs.json')))
    groups = docs['navigation']['tabs'][0]['groups']
    summary = ['# Table of contents', '', '* [Introduction](README.md)']
    for g in groups:
        summary.append(f'\n## {g["group"]}\n')
        for p in g['pages']:
            src = os.path.join(SRC, p + '.mdx')
            text = open(src).read()
            md = convert(p, text)
            title = re.search(r'^# (.*)$', md, re.M).group(1)
            outp = 'README.md' if p == 'introduction' else p + '.md'
            os.makedirs(os.path.dirname(os.path.join(OUT, outp)) or OUT, exist_ok=True)
            open(os.path.join(OUT, outp), 'w').write(md)
            if p != 'introduction':
                summary.append(f'* [{title}]({outp})')
    # API reference pages from openapi.json
    api = json.load(open(os.path.join(SRC, 'openapi.json')))
    os.makedirs(os.path.join(OUT, 'api-reference'), exist_ok=True)
    shutil.copy(os.path.join(SRC, 'openapi.json'), os.path.join(OUT, 'openapi.json'))
    by_tag = {}
    for path, ops in api['paths'].items():
        for method, op in ops.items():
            by_tag.setdefault(op.get('tags', ['other'])[0], []).append((path, method, op))
    order = ['videos', 'sources', 'library', 'voices', 'channels', 'series', 'account', 'webhooks', 'embed', 'billing']
    summary.append('\n## API reference\n')
    summary.append('* [Overview](api-reference/README.md)')
    intro = ['# API reference', '', f'Base URL `https://api.monkeygun.com/v1` · `Authorization: Bearer mk_live_…` · OpenAPI source: [openapi.json](../openapi.json) (also served live at https://api.monkeygun.com/v1/openapi.json).', '', 'Every tool in the catalog is `POST /v1/tools/{name}` with a JSON body matching its schema. The pages below are generated from the OpenAPI document.', '']
    for tag in order + [t for t in by_tag if t not in order]:
        if tag not in by_tag: continue
        items = by_tag[tag]
        fname = f'api-reference/{tag}.md'
        lines = [f'# {tag.capitalize()}', '']
        for path, method, op in sorted(items, key=lambda x: (0 if not x[0].startswith('/tools/') else 1, x[2].get('summary',''))):
            lines.append(f'## {op.get("summary", path)}')
            lines.append('')
            lines.append(f'{{% openapi src="../openapi.json" path="{path}" method="{method}" %}}')
            lines.append(f'[openapi.json](../openapi.json)')
            lines.append('{% endopenapi %}')
            lines.append('')
        open(os.path.join(OUT, fname), 'w').write('\n'.join(lines))
        summary.append(f'* [{tag.capitalize()}]({fname})')
        intro.append(f'* [{tag.capitalize()}]({tag}.md) — {len(items)} operations')
    open(os.path.join(OUT, 'api-reference', 'README.md'), 'w').write('\n'.join(intro) + '\n')
    open(os.path.join(OUT, 'SUMMARY.md'), 'w').write('\n'.join(summary) + '\n')
    shutil.copytree(os.path.join(SRC, 'images'), os.path.join(OUT, 'images'))
    open(os.path.join(OUT, '.gitbook.yaml'), 'w').write('root: ./\n\nstructure:\n  readme: README.md\n  summary: SUMMARY.md\n')
    n = sum(1 for r, _, fs in os.walk(OUT) for f in fs if f.endswith('.md'))
    print(f'wrote {n} markdown files to {OUT}')

main()
