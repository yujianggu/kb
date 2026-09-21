import importlib.util
import json
from pathlib import Path
import tempfile
import subprocess
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'scripts' / 'kb.py'


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(MODULE.exists(), '需要实现知识库工具 scripts/kb.py')
        spec = importlib.util.spec_from_file_location('kb', MODULE)
        self.kb = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.kb)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.write('kb.json', {'version': 1, 'domains': [
            {'id': 'test', 'title': '测试', 'summary': '测试领域', 'path': '领域'}], 'extensions': []})
        self.topic('a')
        self.topic('b')

    def write(self, path, data):
        file = self.root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')

    def topic(self, name, **changes):
        data = {'id': name, 'title': name, 'summary': '主题用途', 'kind': 'method',
                'scope': 'general', 'status': 'general', 'entrypoints':
                {'brief': '摘要.md', 'detail': '正文.md', 'examples': '案例.md'},
                'requires': [], 'related': []}
        data.update(changes)
        base = self.root / '领域' / name
        base.mkdir(parents=True, exist_ok=True)
        for p in ['摘要.md', '正文.md', '案例.md']:
            (base / p).write_text(name + p, encoding='utf-8')
        self.write(f'领域/{name}/topic.json', data)

    def test_brief_only_does_not_expand_related(self):
        self.topic('a', related=['b'])
        self.kb.build(self.root)
        result = self.kb.resolve(self.root, ['a'], 'brief')
        self.assertEqual([x['path'] for x in result['files']], ['领域/a/摘要.md'])

    def test_detail_includes_required_dependencies_once(self):
        self.topic('a', requires=['b'], related=['b'])
        self.kb.build(self.root)
        result = self.kb.resolve(self.root, ['a', 'b'], 'detail')
        self.assertEqual([x['path'] for x in result['files']],
                         ['领域/b/摘要.md', '领域/b/正文.md', '领域/a/摘要.md', '领域/a/正文.md'])

    def test_cycle_and_unknown_dependency_rejected(self):
        for requirement in ['a', 'missing']:
            with self.subTest(requirement=requirement):
                self.topic('a', requires=[requirement])
                with self.assertRaises(ValueError):
                    self.kb.build(self.root)

    def test_duplicate_id_rejected(self):
        self.topic('b', id='a')
        with self.assertRaises(ValueError):
            self.kb.build(self.root)

    def test_missing_file_and_outside_path_rejected(self):
        for path in ['missing.md', '../../../outside.md']:
            with self.subTest(path=path):
                self.topic('a', entrypoints={'brief': path, 'detail': '正文.md'})
                with self.assertRaises(ValueError):
                    self.kb.build(self.root)

    def test_stale_index_rejected(self):
        self.kb.build(self.root)
        self.topic('a', summary='更新后的用途')
        with self.assertRaises(ValueError):
            self.kb.check(self.root)

    def test_budget_does_not_silently_truncate(self):
        self.kb.build(self.root)
        with self.assertRaises(ValueError):
            self.kb.resolve(self.root, ['a'], 'detail', max_bytes=1)

    def test_reference_requires_explicit_opt_in(self):
        self.topic('b', status='reference')
        self.topic('a', requires=['b'])
        self.kb.build(self.root)
        with self.assertRaises(ValueError):
            self.kb.resolve(self.root, ['a'], 'detail')
        result = self.kb.resolve(self.root, ['a'], 'detail', allow_reference=True)
        self.assertEqual(len(result['files']), 4)

    def test_missing_optional_layer_is_reported(self):
        self.topic('a', entrypoints={'brief': '摘要.md', 'detail': '正文.md'})
        self.kb.build(self.root)
        with self.assertRaises(ValueError):
            self.kb.resolve(self.root, ['a'], 'examples')

    def test_copy_inside_consumer_does_not_claim_consumer_revision(self):
        parent = self.root
        nested = parent / 'vendor' / 'kb'
        nested.mkdir(parents=True)
        (parent / 'kb.json').rename(nested / 'kb.json')
        (parent / '领域').rename(nested / '领域')
        subprocess.run(['git', 'init', '-q', str(parent)], check=True, capture_output=True)
        subprocess.run(['git', '-C', str(parent), '-c', 'user.name=Test',
                        '-c', 'user.email=test@example.invalid', '-c', 'commit.gpgsign=false',
                        'commit', '--allow-empty', '-qm', 'Consumer'], check=True, capture_output=True)
        self.kb.build(nested)
        result = self.kb.resolve(nested, ['a'])
        self.assertIsNone(result['revision'])
        self.assertIsNone(result['dirty'])

    def test_generated_catalogs_are_hierarchical_and_repeatable(self):
        self.kb.build(self.root)
        before = (self.root / 'catalog.json').read_bytes()
        root = json.loads(before)
        self.assertNotIn('topics', root)
        self.assertEqual(root['domains'][0]['catalog'], '领域/catalog.json')
        self.kb.build(self.root)
        self.kb.check(self.root)
        self.assertEqual(before, (self.root / 'catalog.json').read_bytes())


if __name__ == '__main__':
    unittest.main()
