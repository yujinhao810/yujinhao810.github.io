"""Copy the confirmed author's public posts; Python standard library only.

Fetches are cached outside docs. Never logs in or changes the source site.
Run with --collect to cache source data, then without it to write Markdown.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from collections import Counter
from datetime import datetime
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / '.cache' / 'kajspace'
ORIGIN = 'https://kajspace.cn'
AUTHOR = '/people/cf18d0be-ad58-414d-a05f-d42105cbbc9f/'
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


class Node:
    def __init__(self, tag='', attrs=None):
        self.tag, self.attrs, self.children = tag, dict(attrs or []), []

    def text(self):
        return ''.join(c.text() if isinstance(c, Node) else c for c in self.children)

    def find(self, predicate):
        for child in self.children:
            if isinstance(child, Node):
                if predicate(child):
                    yield child
                yield from child.find(predicate)

    def has_class(self, name):
        return name in self.attrs.get('class', '').split()


class Tree(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = Node('root')
        self.stack = [self.root]
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def first(node, predicate):
    return next(node.find(predicate), None)


def fetch(url, key):
    path = CACHE / key
    if path.exists():
        return path.read_bytes()
    for attempt in range(3):
        try:
            data = urlopen(Request(url, headers={'User-Agent': 'JynxHao-Blog-Migration/1.0'}), timeout=40).read()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            return data
        except Exception:
            if attempt == 2:
                raise
            time.sleep(1)


def collect():
    url, seen, records = ORIGIN + AUTHOR, set(), []
    expected = None
    while url:
        tree = Tree(fetch(url, 'profile-' + hashlib.sha256(url.encode()).hexdigest()[:12] + '.html').decode('utf-8')).root
        index = first(tree, lambda n: n.attrs.get('id') == 'article-index')
        if not index:
            raise ValueError('Public author index unavailable')
        if expected is None:
            expected = int(re.search(r'共\s*(\d+)\s*篇', index.text())[1])
        for heading in index.find(lambda n: n.tag == 'h3'):
            link = first(heading, lambda n: n.tag == 'a' and '/articles/' in n.attrs.get('href', ''))
            if link:
                href = urljoin(ORIGIN, link.attrs['href'])
                if href not in seen:
                    seen.add(href)
                    records.append({'source': href, 'listTitle': heading.text().strip()})
        next_link = first(index, lambda n: n.tag == 'a' and n.attrs.get('href') and n.text().strip() == '下一页')
        url = urljoin(url, next_link.attrs['href']) if next_link else None
    assert len(records) == expected, (len(records), expected)
    for i, record in enumerate(records):
        source_id = record['source'].rstrip('/').split('/')[-1]
        tree = Tree(fetch(record['source'], source_id + '.html').decode('utf-8')).root
        article = first(tree, lambda n: n.tag == 'article' and n.has_class('article-reader'))
        header = first(article, lambda n: n.tag == 'header')
        author = first(header, lambda n: n.has_class('article-reader__author'))
        assert urlsplit(urljoin(ORIGIN, author.attrs['href'])).path == AUTHOR, record['source']
        date = first(header, lambda n: n.tag == 'time').attrs['datetime']
        datetime.fromisoformat(date)
        record.update(id=source_id, title=first(header, lambda n: n.tag == 'h1').text().strip(), publishedAt=date)
        tags = first(header, lambda n: n.attrs.get('aria-label') == '文章标签')
        record['tags'] = [n.text().strip() for n in tags.find(lambda n: n.tag == 'a')] if tags else []
        print(f'Fetched {i+1}/{len(records)}: {source_id}', flush=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    (CACHE / 'records.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Collected {len(records)} public posts.', flush=True)


def category(record, body):
    title, tags = record['title'], record['tags']
    if re.search(r'^(?:LeetCode|力扣|HOT100|\d+\s*[.、])', title, re.I) or '算法' in tags:
        return 'algorithm'
    if 'Agent' in tags or re.search(r'RAG|MCP|Agent|LangGraph|SSE|工具调用|向量|流式', title, re.I):
        return 'ai-agent'
    if '后端' in tags or re.search(r'Nest|Node|后端|数据库|Redis|MySQL', title, re.I):
        return 'node'
    if re.search(r'HealthFlow|低代码|项目', title, re.I):
        return 'project'
    if re.search(r'Vue|React|Pinia|Vite|Webpack|组件|虚拟|Diff|Fiber|路由', title, re.I):
        return 'vue'
    if '前端' in tags or re.search(r'JavaScript|TypeScript|JS|TS|CSS|HTML|浏览器|Promise|闭包|原型|跨域', title, re.I):
        return 'javascript'
    return 'notes'


def escaped(text):
    # Markdown must not interpret Vue interpolation or untrusted HTML as components.
    return escape(text, quote=False).replace('{{', '&#123;&#123;').replace('}}', '&#125;&#125;').replace('\\', '\\\\').replace('*', '\\*').replace('_', '\\_').replace('`', '\\`')


class Converter:
    def __init__(self, source, slug):
        self.source, self.slug = source, slug
        self.assets = []
        self.warnings = []
        self.removed_empty_blocks = 0
        self.code_blocks = []

    def children(self, node):
        return ''.join(self.convert(c) for c in node.children)

    def convert(self, node):
        if isinstance(node, str):
            return escaped(node)
        tag = node.tag
        if tag in ('script', 'style', 'button', 'svg') or node.has_class('article-code-block__tools'):
            return ''
        if tag == 'pre':
            code = first(node, lambda n: n.tag == 'code') or node
            text = code.text().rstrip('\n')
            if not text.strip():
                self.removed_empty_blocks += 1
                return ''
            lang = code.attrs.get('data-language', '') or code.attrs.get('class', '').removeprefix('language-')
            if lang in ('', 'text', 'plaintext'):
                if re.search(r'^\s*(interface|type)\s+\w+', text, re.M):
                    lang = 'ts'
                elif re.search(r'\b(function|const|let|var|return|console\.|prototype)\b|=>|===|\b(?:if|for|while)\s*\(', text):
                    lang = 'js'
                elif re.search(r'</?[A-Za-z][^>]*>', text):
                    lang = 'html'
                else:
                    lang = 'text'
            fence = '`' * max(3, max((len(m[0]) + 1 for m in re.finditer(r'`+', text)), default=3))
            # Protect code whitespace from paragraph/heading cleanup below.
            token = f'\x00KAJ_CODE_{len(self.code_blocks)}\x00'
            self.code_blocks.append((token, f'{fence}{lang}\n{text}\n{fence}'))
            return f'\n\n{token}\n\n'
        if tag == 'code':
            text = node.text()
            fence = '`' * max(1, max((len(m[0]) + 1 for m in re.finditer(r'`+', text)), default=1))
            pad = ' ' if '`' in text else ''
            return fence + pad + text + pad + fence
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            # Retain source heading IDs for internal links in imported posts.
            anchor = node.attrs.get('id', '')
            suffix = f' {{#{anchor}}}' if anchor and re.fullmatch(r'[\w-]+', anchor) else ''
            return '\n\n' + '#' * max(2, int(tag[1])) + ' ' + self.children(node).strip() + suffix + '\n\n'
        if tag == 'p':
            return '\n\n' + self.children(node).strip() + '\n\n'
        if tag == 'br':
            return '  \n'
        if tag == 'hr':
            return '\n\n---\n\n'
        if tag in ('strong', 'b'):
            text = self.children(node)
            return text[:len(text)-len(text.lstrip())] + '**' + text.strip() + '**' + text[len(text.rstrip()):] if text.strip() else text
        if tag in ('em', 'i'):
            return '*' + self.children(node) + '*'
        if tag in ('del', 's'):
            return '~~' + self.children(node) + '~~'
        if tag in ('ul', 'ol'):
            items = [c for c in node.children if isinstance(c, Node) and c.tag == 'li']
            start = int(node.attrs.get('start', 1))
            lines = []
            for i, item in enumerate(items):
                prefix = f'{start+i}. ' if tag == 'ol' else '- '
                content = self.children(item).strip()
                lines.append(prefix + content.replace('\n', '\n' + ' ' * len(prefix)))
            return '\n\n' + '\n'.join(lines) + '\n\n'
        if tag == 'blockquote':
            return '\n\n' + '\n'.join('> ' + line for line in self.children(node).strip().splitlines()) + '\n\n'
        if tag == 'table':
            rows = []
            for tr in node.find(lambda n: n.tag == 'tr'):
                cells = [n for n in tr.children if isinstance(n, Node) and n.tag in ('th', 'td')]
                rows.append([self.children(c).strip().replace('\n', '<br>').replace('|', '\\|') for c in cells])
            if not rows:
                return ''
            width = max(map(len, rows))
            rows = [r + [''] * (width-len(r)) for r in rows]
            result = ['| ' + ' | '.join(rows[0]) + ' |', '| ' + ' | '.join(['---'] * width) + ' |']
            result += ['| ' + ' | '.join(row) + ' |' for row in rows[1:]]
            return '\n\n' + '\n'.join(result) + '\n\n'
        if tag == 'a':
            href = node.attrs.get('href', '')
            if not href or urlsplit(href).scheme not in ('', 'http', 'https', 'mailto'):
                return self.children(node)
            href = href if href.startswith('#') else urljoin(self.source, href)
            return '[' + self.children(node).strip() + '](' + href.replace(' ', '%20').replace(')', '%29') + ')'
        if tag == 'img':
            src = urljoin(self.source, node.attrs.get('src', ''))
            if not src.startswith(('https://', 'http://')):
                return ''
            suffix = Path(urlsplit(src).path).suffix.lower()
            if suffix not in ('.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg'):
                suffix = '.png'
            name = hashlib.sha256(src.encode()).hexdigest()[:16] + suffix
            data = fetch(src, 'assets/' + name)
            asset = ROOT / 'docs/public/images/kajspace' / name
            asset.parent.mkdir(parents=True, exist_ok=True)
            asset.write_bytes(data)
            self.assets.append(src)
            return '![' + escaped(node.attrs.get('alt', '')).replace(']', '\\]') + '](/images/kajspace/' + name + ')'
        if tag in ('sup', 'sub'):
            return f'<{tag}>' + self.children(node) + f'</{tag}>'
        if tag == 'span' and node.attrs.get('id'):
            return '<span id="' + escape(node.attrs['id'], quote=True) + '"></span>' + self.children(node)
        return self.children(node)


def migrate():
    records = json.loads((CACHE / 'records.json').read_text(encoding='utf-8'))
    manifest = ROOT / 'migration/kajspace-manifest.json'
    previous = {r['id']: r for r in json.loads(manifest.read_text(encoding='utf-8'))} if manifest.exists() else {}
    report = []
    for record in records:
        tree = Tree((CACHE / (record['id'] + '.html')).read_text(encoding='utf-8')).root
        body = first(tree, lambda n: n.has_class('article-prose'))
        if not body or not body.text().strip():
            raise ValueError('Missing article body: ' + record['source'])
        folder = category(record, body)
        slug = 'kaj-' + record['id'].lower()
        if record['id'] == '01M4QHQ4JHD8ZERV1GS2XEEP2J':
            # Already migrated and corrected; keep its established URL and body.
            target = ROOT / 'docs/posts/algorithm/shuffle-array.md'
            text = target.read_text(encoding='utf-8')
            if 'publishedAt:' not in text:
                text = text.replace('date: 2026-10-12', 'date: 2026-10-12\npublishedAt: ' + json.dumps(record['publishedAt']) + '\nsource: ' + json.dumps(record['source']))
                target.write_text(text, encoding='utf-8')
            report.append({**record, 'path': target.relative_to(ROOT).as_posix(), 'existing': True, 'assets': [], 'warnings': []})
            continue
        target = ROOT / 'docs/posts' / folder / (slug + '.md')
        converter = Converter(record['source'], slug)
        first_block = next((n for n in body.children if isinstance(n, Node)), None)
        def title_key(value):
            return re.sub(r'[\W_]+', '', re.sub(r'^(?:力扣|leetcode)\s*', '', value, flags=re.I)).lower()
        if first_block and first_block.tag == 'h1' and (title_key(first_block.text()) == title_key(record['title']) or first_block.text().startswith(record['title'] + '：')):
            # The page heading already supplies the same title; keep its link anchor.
            body.children.remove(first_block)
            anchor = first_block.attrs.get('id', '')
            if anchor:
                body.children.insert(0, Node('span', [('id', anchor)]))
            # Retain an extended title's subject as a small introductory line.
            if first_block.text().startswith(record['title'] + '：'):
                subtitle = Node('p')
                subtitle.children = [first_block.text()[len(record['title']) + 1:]]
                body.children.insert(1, subtitle)
        markdown = converter.convert(body).strip()
        markdown = re.sub(r'\n[ \t]+\n', '\n\n', markdown)
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        # One page title; source headings remain intact as section headings.
        markdown = re.sub(r'^# (.+)$', r'## \1', markdown, flags=re.M)
        repairs = []
        def local_reference(match):
            return '`' + match[1].replace('\\_', '_').replace('\\*', '*') + '`'
        markdown, local_refs = re.subn(r'\[([^\]]+)\]\((?:[A-Za-z]:|file:)[^)]*\)', local_reference, markdown)
        if local_refs:
            repairs.append(f'Converted {local_refs} machine-specific file links to code references')
        if record['id'] == '01M4G30NDN2AZQ6YM535GEA3HX':
            # The source HTML lost math spans. Values follow directly from its
            # Map + index-range recursion implementation (one visit per node).
            replacements = {
                '设二叉树共有 个节点。': '设二叉树共有 `n` 个节点。',
                '### 时间复杂度： ': '### 时间复杂度：`O(n)` ',
                '构建 `Map` 需要 时间。': '构建 `Map` 需要 `O(n)` 时间。',
                '每次 `Map.get()` 平均为 。': '每次 `Map.get()` 平均为 `O(1)`。',
                '因此，总时间复杂度为：': '因此，总时间复杂度为 `O(n)`。',
                '### 空间复杂度： ': '### 空间复杂度：`O(n)` ',
                '`Map` 存储所有节点的位置，占用 空间。': '`Map` 存储所有节点的位置，占用 `O(n)` 空间。',
                '递归调用栈最坏需要 空间': '递归调用栈最坏需要 `O(n)` 空间',
                '因此，辅助空间复杂度为 。': '因此，辅助空间复杂度为 `O(n)`。',
                '将时间复杂度优化到 。': '将时间复杂度优化到 `O(n)`。',
            }
            for old, new in replacements.items():
                assert old in markdown, old
                markdown = markdown.replace(old, new)
            repairs.append('Restored n, O(n) and O(1) in complexity analysis from the shown algorithm')
        for token, code_block in converter.code_blocks:
            def restore(match):
                prefix = match[1]
                continuation = re.sub(r'(?:[-*+]|\d+\.) $', lambda m: ' ' * len(m[0]), prefix)
                lines = code_block.split('\n')
                return prefix + lines[0] + ''.join('\n' + continuation + line for line in lines[1:])
            markdown = re.sub(r'^([ \t>]*(?:(?:[-*+]|\d+\.) )?)' + re.escape(token), restore, markdown, flags=re.M)
            assert token not in markdown, 'Unresolved code placeholder'
        intro = first(body, lambda n: n.tag == 'p' and bool(n.text().strip()))
        description = re.sub(r'\s+', ' ', intro.text()).strip()[:120] if intro else record['title']
        fields = {'title': record['title'], 'description': description, 'date': record['publishedAt'][:10], 'publishedAt': record['publishedAt'], 'source': record['source'], 'tags': record['tags']}
        frontmatter = '\n'.join(key + ': ' + json.dumps(value, ensure_ascii=False) for key, value in fields.items())
        output = f'---\n{frontmatter}\n---\n\n# {escaped(record["title"])}\n\n{markdown}\n'
        if target.exists() and target.read_text(encoding='utf-8') != output:
            expected_hash = previous.get(record['id'], {}).get('contentHash')
            if not expected_hash or hashlib.sha256(target.read_bytes()).hexdigest() != expected_hash:
                raise ValueError('Refusing to overwrite modified imported post: ' + str(target))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding='utf-8')
        empty_cells = sum(not n.text().strip() for n in body.find(lambda n: n.tag == 'td'))
        if empty_cells:
            converter.warnings.append(f'{empty_cells} empty table cells in source HTML')
        report.append({**record, 'path': target.relative_to(ROOT).as_posix(), 'existing': False, 'assets': converter.assets, 'warnings': converter.warnings, 'repairs': repairs, 'removedEmptyCodeBlocks': converter.removed_empty_blocks, 'contentHash': hashlib.sha256(target.read_bytes()).hexdigest()})
    dest = ROOT / 'migration/kajspace-manifest.json'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'total': len(report), 'new': sum(not r['existing'] for r in report), 'categories': dict(Counter(Path(r['path']).parent.name for r in report)), 'sourceWarnings': sum(bool(r['warnings']) for r in report)}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--collect', action='store_true')
    args = parser.parse_args()
    collect() if args.collect else migrate()
