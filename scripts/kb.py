#!/usr/bin/env python3
"""Build metadata indexes and resolve reading manifests; never load document bodies."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

LAYERS = ('brief', 'detail', 'examples', 'sources', 'assets')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def encoded(data):
    return json.dumps(data, ensure_ascii=False, indent=2) + '\n'


def local(root, base, name):
    if not isinstance(name, str) or not name or Path(name).is_absolute():
        raise ValueError(f'非法相对路径：{name}')
    target = (base / name).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f'路径超出知识库：{name}')
    if not target.is_file():
        raise ValueError(f'文件不存在：{target}')
    return target.relative_to(root.resolve()).as_posix()


def validate_topic(data):
    keys = {'id', 'title', 'summary', 'kind', 'scope', 'status', 'entrypoints', 'requires', 'related'}
    if not isinstance(data, dict) or set(data) != keys:
        raise ValueError('topic.json 字段须与 schemas/topic.schema.json 一致')
    for key in ('id', 'title', 'summary'):
        if not isinstance(data[key], str) or not data[key].strip():
            raise ValueError(f'主题缺少 {key}')
    if not re.fullmatch(r'[a-z0-9][a-z0-9._-]*', data['id']):
        raise ValueError(f'非法 ID：{data["id"]}')
    for key, values in [('kind', ('concept', 'method', 'template', 'example', 'reference')),
                        ('scope', ('general', 'industry', 'company')),
                        ('status', ('general', 'reference', 'example'))]:
        if data[key] not in values:
            raise ValueError(f'{data["id"]} 的 {key} 不合法')
    entries = data['entrypoints']
    if not isinstance(entries, dict) or not {'brief', 'detail'} <= set(entries) or set(entries) - set(LAYERS):
        raise ValueError(f'{data["id"]} 必须声明 brief/detail，且不能使用未知层级')
    if any(not isinstance(v, str) or not v for v in entries.values()):
        raise ValueError('入口必须为非空相对文件路径')
    for key in ('requires', 'related'):
        v = data[key]
        if not isinstance(v, list) or any(not isinstance(x, str) for x in v) or len(v) != len(set(v)):
            raise ValueError(f'{key} 必须是无重复 ID 的数组')


def collect(root):
    root = root.resolve()
    config = read(root / 'kb.json')
    if config['version'] != 1:
        raise ValueError('不支持的 kb.json 版本')
    topics, locations = {}, {}
    extensions = [(root / x['path']).resolve() for x in config.get('extensions', [])]
    for domain in config['domains']:
        base = (root / domain['path']).resolve()
        if not base.is_relative_to(root) or not base.is_dir():
            raise ValueError(f'领域目录无效：{domain["path"]}')
        for path in sorted(base.rglob('topic.json')):
            if any(path.resolve().is_relative_to(x) for x in extensions):
                continue
            data = read(path)
            validate_topic(data)
            ident = data['id']
            if ident in topics:
                raise ValueError(f'重复主题 ID：{ident}')
            for value in data['entrypoints'].values():
                rel = local(root, path.parent, value)
                if any((root / rel).is_relative_to(x) for x in extensions):
                    raise ValueError(f'通用主题不能隐式读取扩展：{ident}')
            topics[ident] = data
            locations[ident] = path.relative_to(root).as_posix()
    for ident, data in topics.items():
        for dep in data['requires'] + data['related']:
            if dep not in topics:
                raise ValueError(f'{ident} 引用未知 ID：{dep}')
    order(topics, list(topics))
    return config, topics, locations


def order(topics, ids):
    result, seen, active = [], set(), set()
    def visit(ident):
        if ident not in topics:
            raise ValueError(f'未知主题 ID：{ident}')
        if ident in active:
            raise ValueError(f'必需依赖循环：{ident}')
        if ident in seen:
            return
        active.add(ident)
        for dep in topics[ident]['requires']:
            visit(dep)
        active.remove(ident)
        seen.add(ident)
        result.append(ident)
    for ident in ids:
        visit(ident)
    return result


def outputs(root):
    config, topics, locations = collect(root)
    result, nodes = {}, {}
    for ident, data in topics.items():
        # A topic directory is a content unit; its parent is the leaf catalog.
        parent = Path(locations[ident]).parent.parent
        while parent != Path('.'):
            nodes.setdefault(parent, {'version': 1, 'title': parent.name, 'groups': [], 'topics': []})
            parent = parent.parent
        leaf = Path(locations[ident]).parent.parent
        card = {k: data[k] for k in ('id', 'title', 'summary', 'kind', 'scope', 'status')}
        card['metadata'] = locations[ident]
        card['brief'] = local(root, (root / locations[ident]).parent, data['entrypoints']['brief'])
        nodes[leaf]['topics'].append(card)
    for node in sorted(nodes):
        if node.parent in nodes:
            nodes[node.parent]['groups'].append({'title': node.name, 'catalog': (node / 'catalog.json').as_posix()})
        nodes[node]['topics'].sort(key=lambda x: x['id'])
        result[(node / 'catalog.json').as_posix()] = nodes[node]
    domains = []
    for domain in config['domains']:
        path = str(Path(domain['path']) / 'catalog.json')
        if path not in result:
            raise ValueError(f'领域没有注册主题：{domain["id"]}')
        domains.append({k: domain[k] for k in ('id', 'title', 'summary')} | {'catalog': path})
    result['catalog.json'] = {'version': 1, 'path_base': 'repository-root', 'domains': domains,
                              'extensions': config.get('extensions', [])}
    result['index/topics.json'] = {'version': 1, 'topics': {
        ident: {'metadata': locations[ident], 'sha256': hashlib.sha256(
            (root / locations[ident]).read_bytes()).hexdigest()} for ident in sorted(topics)}}
    return result


def build(root):
    generated = outputs(root)
    for path, data in generated.items():
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(encoded(data), encoding='utf-8')
    return len(generated)


def check(root):
    generated = outputs(root)
    for path, data in generated.items():
        target = root / path
        if not target.exists() or target.read_text(encoding='utf-8') != encoded(data):
            raise ValueError(f'索引缺失或过期，请运行 build：{path}')
    return len(generated)


def resolve(root, ids, layer='brief', max_bytes=None, allow_reference=False):
    root = root.resolve()
    if layer not in LAYERS:
        raise ValueError(f'未知层级：{layer}')
    registry = read(root / 'index/topics.json')['topics']
    topics, bases = {}, {}
    def load(ident):
        if ident in topics:
            return
        if ident not in registry:
            raise ValueError(f'未知主题 ID：{ident}')
        record = registry[ident]
        path = root / local(root, root, record['metadata'])
        if hashlib.sha256(path.read_bytes()).hexdigest() != record['sha256']:
            raise ValueError(f'主题索引过期，请运行 build：{ident}')
        data = read(path)
        validate_topic(data)
        if data['id'] != ident:
            raise ValueError(f'索引 ID 不一致：{ident}')
        if data['status'] == 'reference' and not allow_reference:
            raise ValueError(f'主题原义待核实，需显式 --allow-reference：{ident}')
        topics[ident], bases[ident] = data, path.parent
        for dep in data['requires']:
            load(dep)
    for ident in ids:
        load(ident)
    files, seen = [], set()
    for ident in order(topics, ids):
        data = topics[ident]
        # Required concepts are read at brief depth for selection and detail depth for use.
        selected = layer if ident in ids else ('brief' if layer == 'brief' else 'detail')
        levels = ['brief'] if selected == 'brief' else ['brief', 'detail']
        if selected not in ('brief', 'detail'):
            levels.append(selected)
        for level in levels:
            if level not in data['entrypoints']:
                raise ValueError(f'{ident} 没有 {level} 入口')
            path = local(root, bases[ident], data['entrypoints'][level])
            if path not in seen:
                seen.add(path)
                files.append({'id': ident, 'layer': level, 'path': path,
                              'bytes': (root / path).stat().st_size})
    total = sum(x['bytes'] for x in files)
    if max_bytes is not None and total > max_bytes:
        raise ValueError(f'读取预算不足：需要 {total} 字节，预算 {max_bytes}；未输出不完整清单')
    revision, dirty = None, None
    # Git walks up directories: a vendor copy must not inherit its consumer's identity.
    top = subprocess.run(['git', '-C', str(root), 'rev-parse', '--show-toplevel'],
                         capture_output=True, text=True)
    if top.returncode == 0 and Path(top.stdout.strip()).resolve() == root:
        rev = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'], capture_output=True, text=True)
        state = subprocess.run(['git', '-C', str(root), 'status', '--porcelain'], capture_output=True, text=True)
        revision = rev.stdout.strip() if rev.returncode == 0 else None
        dirty = bool(state.stdout.strip()) if state.returncode == 0 else None
    return {'version': 1, 'revision': revision,
            'dirty': dirty,
            'requested': ids, 'layer': layer, 'total_bytes': total, 'files': files}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('build', help='生成分层索引')
    commands.add_parser('check', help='验证元数据、依赖、入口及索引同步')
    target = commands.add_parser('resolve', help='输出需读取的文件清单，不读取正文')
    target.add_argument('ids', nargs='+')
    target.add_argument('--layer', choices=LAYERS, default='brief')
    target.add_argument('--max-bytes', type=int)
    target.add_argument('--allow-reference', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'resolve':
            result = resolve(args.root, args.ids, args.layer, args.max_bytes, args.allow_reference)
        else:
            result = {'catalogs': globals()[args.command](args.root), 'status': 'ok'}
        print(encoded(result), end='')
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'错误：{exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
