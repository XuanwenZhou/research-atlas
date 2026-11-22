"""Deterministic regression checks using the explicitly synthetic example."""
import copy
import csv
import json
import tempfile
import unittest
from pathlib import Path
from data_model import read_json, validate, duplicate_candidates, merge_papers, arxiv_key
from build_html import build
from export_bibliography import export, bib_escape

ROOT = Path(__file__).resolve().parent.parent

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.data = read_json(ROOT / 'assets' / 'example-data.json')
    def codes(self):
        return {e['code'] for e in validate(self.data)['errors']}
    def warn_codes(self):
        return {w['code'] for w in validate(self.data)['warnings']}
    def test_example_is_structurally_valid(self):
        self.assertFalse(validate(self.data)['errors'])
        self.assertTrue(self.data['metadata']['is_synthetic'])
    def test_missing_id(self):
        del self.data['papers'][0]['id']
        self.assertIn('id', self.codes())
    def test_duplicate_id(self):
        self.data['methods'].append(copy.deepcopy(self.data['methods'][0]))
        self.assertIn('duplicate_id', self.codes())
    def test_broken_reference(self):
        self.data['edges'][0]['target'] = 'missing'
        self.assertIn('dangling_reference', self.codes())
    def test_invalid_relation(self):
        self.data['edges'][0]['type'] = 'similar'
        self.assertIn('edge_type', self.codes())
    def test_no_verified_inference(self):
        self.data['edges'][0]['verification'] = 'verified'
        self.assertIn('unsupported_verified_edge', self.codes())
    def test_verified_edge_requires_original_fulltext(self):
        e = self.data['edges'][0]
        e.update(verification='verified', claim_basis='fact')
        self.assertIn('unsupported_verified_edge', self.codes())
        e['evidence'] = [dict(source_type='primary_paper', access_level='full_text', source_id='test-only-primary', locator='Sec 3', summary='TEST FIXTURE', checked_at='2026-11-11')]
        self.assertNotIn('unsupported_verified_edge', self.codes())
    def test_calendar_date(self):
        self.data['papers'][0]['first_public_date'] = '2025-02-29'
        self.assertIn('date', self.codes())
    def test_unsafe_url(self):
        self.data['papers'][0]['url'] = 'javascript:alert(1)'
        self.assertIn('unsafe_url', self.codes())
    def test_group_cycle(self):
        self.data['groups'][0]['parent_id'] = 'adaptive'
        self.assertIn('hierarchy', self.codes())
    def test_wrong_primary_membership(self):
        self.data['methods'][0]['group_ids'] = ['optimization']
        self.assertIn('primary_membership', self.codes())
    def test_arxiv_versions_share_identity(self):
        self.assertEqual(arxiv_key('https://arxiv.org/abs/2301.12345v2'), arxiv_key('2301.12345v1'))
    def test_deduplicate_does_not_mutate(self):
        p = copy.deepcopy(self.data['papers'][0]); p['id'] = 'p-copy'
        self.data['papers'].append(p)
        before = copy.deepcopy(self.data)
        self.assertTrue(duplicate_candidates(self.data))
        self.assertEqual(before, self.data)
    def test_merge_keeps_id_and_retargets_methods(self):
        p = copy.deepcopy(self.data['papers'][0]); p['id'] = 'p-copy'
        self.data['papers'].append(p)
        self.data['methods'][1]['paper_ids'] = ['p-copy']
        merged = merge_papers(self.data, {'p-copy': 'p-alpha'})
        self.assertEqual(merged['methods'][1]['paper_ids'], ['p-alpha'])
        self.assertEqual(merged['papers'][0]['id'], 'p-alpha')
        self.assertEqual(merged['papers'][0]['merged_records'][0]['id'], 'p-copy')
        self.assertFalse(validate(merged)['errors'])
        self.assertEqual(len(self.data['papers']), 5)
    def test_merge_rejects_conflicting_identifiers(self):
        self.data['papers'][0]['doi'] = '10.1234/a'
        self.data['papers'][1]['doi'] = '10.1234/b'
        with self.assertRaises(ValueError):
            merge_papers(self.data, {'p-beta': 'p-alpha'})
    def test_strict_rejects_unverified_example(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                build(self.data, Path(d) / 'map.html', strict=True)
    def test_html_embed_does_not_execute_data(self):
        payload = '</script><script>window.INJECTED=1</script>'
        self.data['methods'][0]['name'] = payload
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / 'map.html'; build(self.data, target)
            self.assertNotIn(payload, target.read_text(encoding='utf-8'))
            embedded = target.read_text(encoding='utf-8').split('type="application/json">', 1)[1].split('</script>', 1)[0]
            self.assertEqual(json.loads(embedded)['canonical']['methods'][0]['name'], payload)
            self.assertTrue((Path(d) / 'unresolved.json').exists())
    def test_bibliography_safe_and_paper_level(self):
        self.data['papers'][0]['title'] = '=1+2'
        with tempfile.TemporaryDirectory() as d:
            export(self.data, d)
            with open(Path(d) / 'bibliography.csv', encoding='utf-8-sig', newline='') as f:
                rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 4)
            self.assertEqual(rows[0]['title'], "'=1+2")
            bib = (Path(d) / 'bibliography.bib').read_text(encoding='utf-8')
            self.assertEqual(bib.count('@misc{'), 4)
            self.assertIn(r'\&', bib_escape('A&B'))
    def test_rebuild_preserves_canonical(self):
        with tempfile.TemporaryDirectory() as d:
            build(self.data, Path(d) / 'map.html')
            self.assertEqual(read_json(Path(d) / 'project-data.json'), self.data)
    def test_build_rejects_bad_data(self):
        self.data['edges'][0]['source'] = 'missing'
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                build(self.data, Path(d) / 'map.html')
    def test_problem_equals_mechanism_warns(self):
        self.data['methods'][0]['problem'] = self.data['methods'][0]['mechanism']
        self.assertIn('problem_equals_mechanism', self.warn_codes())
    def test_duplicate_edge_pair_warns(self):
        dup = copy.deepcopy(self.data['edges'][0])
        dup['id'] = 'e-dup-theme'
        dup['type'] = 'theme'
        self.data['edges'].append(dup)
        self.assertIn('duplicate_edge_pair', self.warn_codes())
    def test_group_order_fragmented_warns(self):
        self.data['groups'].append(dict(
            id='rep-sub-2', name='二级分散子类', parent_id='representation',
            definition='测试', problem='测试', rationale='测试', representative_method_ids=[], index=3
        ))
        self.assertIn('group_order_fragmented', self.warn_codes())
    def test_reverse_date_edge_warns(self):
        self.data['edges'][0]['source'], self.data['edges'][0]['target'] = 'm-gamma', 'm-alpha'
        self.assertIn('reverse_date_edge', self.warn_codes())
    def test_title_only_fact_edge_warns(self):
        self.data['edges'][0]['claim_basis'] = 'fact'
        self.assertIn('title_only_fact_edge', self.warn_codes())
    def test_html_payload_is_slim_canonical(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / 'map.html'; build(self.data, target)
            embedded = json.loads(target.read_text(encoding='utf-8').split('type="application/json">', 1)[1].split('</script>', 1)[0])
            self.assertEqual(set(embedded.keys()), {'canonical'})
            self.assertEqual(embedded['canonical'], self.data)
    def test_bibtex_protects_title_case(self):
        self.data['papers'][0]['title'] = '3DGS-SLAM via NeRF'
        with tempfile.TemporaryDirectory() as d:
            export(self.data, d)
            bib = (Path(d) / 'bibliography.bib').read_text(encoding='utf-8')
            self.assertIn('title = {{3DGS-SLAM via NeRF}}', bib)
    def test_recent_coverage_gap_and_report_table(self):
        d = copy.deepcopy(self.data)
        d['metadata']['is_synthetic'] = False
        d['metadata']['search_cutoff'] = '2026-11-22'
        # Expand to 15 older methods (2018) so recent 3-year window (2024-2026) is empty for representation
        for i in range(12):
            m = copy.deepcopy(d['methods'][0])
            m['id'] = f'm-old-{i}'
            d['methods'].append(m)
        warns = {w['code'] for w in validate(d)['warnings']}
        self.assertIn('recent_coverage_gap', warns)
        with tempfile.TemporaryDirectory() as tmp:
            build(d, Path(tmp) / 'map.html')
            report_md = (Path(tmp) / 'verification-report.md').read_text(encoding='utf-8')
            self.assertIn('## 一级方向 × 近年覆盖', report_md)
            self.assertIn('| 表示机制 |', report_md)

if __name__ == '__main__':
    unittest.main(verbosity=2)
