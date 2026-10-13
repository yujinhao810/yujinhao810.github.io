"""Audit the built site against cached source posts and the migration manifest."""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, unquote
from migrate_kajspace import Tree, first, ROOT, CACHE

dist = ROOT / 'docs/.vitepress/dist'
manifest = json.loads((ROOT / 'migration/kajspace-manifest.json').read_text(encoding='utf-8'))
records = json.loads((CACHE / 'records.json').read_text(encoding='utf-8'))
assert len(manifest) == len(records) == 92
assert len({r['id'] for r in manifest}) == 92
assert len({r['path'] for r in manifest}) == 92
pages = {path.resolve(): Tree(path.read_text(encoding='utf-8')).root for path in dist.rglob('*.html')}

code_blocks = 0
for record in manifest:
    markdown = (ROOT / record['path']).read_text(encoding='utf-8')
    published = json.loads(re.search(r'^publishedAt: (.+)$', markdown, re.M)[1])
    source_record = next(r for r in records if r['id'] == record['id'])
    assert published == record['publishedAt'] == source_record['publishedAt'], record['id']
    date = re.search(r'^date: (.+)$', markdown, re.M)[1].strip('"')
    assert date == published[:10], record['id']
    assert re.search(r'^source: (.+)$', markdown, re.M)
    target = (dist / Path(record['path']).relative_to('docs').with_suffix('.html')).resolve()
    page = pages[target]
    publication = first(page, lambda n: n.has_class('article-publication'))
    assert publication and first(publication, lambda n: n.tag == 'time').attrs['datetime'] == published, record['id']
    doc = first(page, lambda n: n.has_class('vp-doc'))
    assert len(list(doc.find(lambda n: n.tag == 'h1'))) == 1, record['id']
    if not record['existing']:
        source_tree = Tree((CACHE / (record['id'] + '.html')).read_text(encoding='utf-8')).root
        body = first(source_tree, lambda n: n.has_class('article-prose'))
        original = [n.text().strip() for n in body.find(lambda n: n.tag == 'pre') if n.text().strip()]
        built = [n.text().strip() for n in doc.find(lambda n: n.tag == 'pre')]
        assert original == built, (record['id'], 'Code content changed', len(original), len(built))
        code_blocks += len(original)

links = 0
pager_links = 0
for path, page in pages.items():
    ids = {n.attrs['id'] for n in page.find(lambda n: 'id' in n.attrs)}
    for n in page.find(lambda n: 'href' in n.attrs or 'src' in n.attrs):
        for attr in ('href', 'src'):
            value = n.attrs.get(attr)
            if not value:
                continue
            assert not re.match(r'^(?:[A-Za-z]:|file:)', value), (str(path), 'Machine-specific link')
            url = urlsplit(value)
            if url.scheme or url.netloc:
                continue
            target = dist / unquote(url.path).lstrip('/') if url.path.startswith('/') else path.parent / unquote(url.path)
            if not url.path:
                target = path
            elif url.path.endswith('/'):
                target /= 'index.html'
            elif not target.suffix:
                target = target.with_suffix('.html')
            target = target.resolve()
            assert target.is_file(), (str(path.relative_to(dist)), value)
            if url.fragment and target in pages:
                target_ids = {x.attrs['id'] for x in pages[target].find(lambda x: 'id' in x.attrs)}
                assert unquote(url.fragment) in target_ids, (str(path.relative_to(dist)), value)
            if n.has_class('pager-link'):
                assert path.relative_to(dist).as_posix().startswith('posts/'), str(path)
                label = first(n, lambda x: x.has_class('title')).text()
                heading = first(pages[target], lambda x: x.tag == 'h1').text().replace('\u200b', '').strip()
                assert label == heading, (str(path), label, heading)
                pager_links += 1
            links += 1

summary = {
    'sourcePosts': len(records), 'migratedPosts': len(manifest),
    'newPosts': sum(not r['existing'] for r in manifest),
    'sitePosts': len(list((ROOT / 'docs/posts').rglob('*.md'))) - 1,
    'htmlPages': len(pages), 'originalCodeBlocksPreserved': code_blocks,
    'localLinksAssetsAnchors': links, 'articlePagerLinks': pager_links,
    'removedEmptyCodeBlocks': sum(r.get('removedEmptyCodeBlocks', 0) for r in manifest),
    'localImages': len(list((ROOT / 'docs/public/images/kajspace').glob('*'))),
    'status': 'passed',
}
(ROOT / 'migration/verification.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
print(json.dumps(summary, indent=2))
