"""Build a self-contained HTML and a reviewable data/report bundle."""
import argparse
import datetime as dt
import json
from collections import Counter
from pathlib import Path
from data_model import read_json, write_json, validate, html_payload
from export_bibliography import export

def build(data, output, strict=False):
    report = validate(data)
    if report['errors'] or (strict and report['warnings']):
        raise ValueError(f"Validation failed: {len(report['errors'])} errors, {len(report['warnings'])} warnings: {report['errors'][:3]}")
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    template = (Path(__file__).resolve().parent.parent / 'assets' / 'evolution-map-template.html').read_text(encoding='utf-8')
    if template.count('__RESEARCH_DATA__') != 1:
        raise ValueError('Template must contain exactly one data marker')
    payload = json.dumps(html_payload(data), ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    output.write_text(template.replace('__RESEARCH_DATA__', payload), encoding='utf-8')
    out = output.parent
    write_json(out / 'project-data.json', data)
    write_json(out / 'groups.json', data['groups'])
    write_json(out / 'edges.json', dict(edges=data['edges'], research_tracks=[dict(id=t['id'], edges=t.get('edges', [])) for t in data['research_tracks']]))
    write_json(out / 'validation.json', report)
    write_json(out / 'unresolved.json', dict(issues=report['warnings'], manual=data['metadata'].get('unresolved', [])))
    export(data, out)
    counts = report['counts']
    warning_counts = Counter(x['code'] for x in report['warnings'])
    md = ['# 文献检索与核验报告', '', f"领域：{data['metadata'].get('domain', '')}",
          f"检索截止：{data['metadata'].get('search_cutoff') or '未记录'}", f"构建时间（UTC）：{dt.datetime.now(dt.timezone.utc).isoformat()}",
          '', '## 实际数据', '', *[f'- {k}: {v}' for k, v in counts.items()],
          '', '## 覆盖与限制', '', str(data['metadata'].get('coverage_limitations') or '未记录'),
          '', '结构检查通过；未在本次构建中进行在线链接访问、原文重读或浏览器交互测试。',
          '构建不会把 first_html_delivered 自动设为 true；实际向用户交付后由研究工作流记录。',
          '', '## 待核问题', '', *[f'- {k}: {v}' for k, v in sorted(warning_counts.items())],
          '', '完整问题见 unresolved.json；事实与推断分别保存在每条关系的 claim_basis。',
          '', '## 检索日志', '', '```json', json.dumps(data['metadata'].get('search_log', []), ensure_ascii=False, indent=2), '```',
          '', '## 用户确认记录', '', '```json', json.dumps(data['metadata'].get('review_decisions', []), ensure_ascii=False, indent=2), '```']
    (out / 'verification-report.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    return report

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input')
    p.add_argument('--output', required=True)
    p.add_argument('--strict', action='store_true')
    a = p.parse_args()
    try:
        r = build(read_json(a.input), a.output, a.strict)
    except (ValueError, OSError, TypeError) as e:
        p.exit(1, str(e) + '\n')
    print(f"Built: {a.output}; warnings={len(r['warnings'])}")

if __name__ == '__main__':
    main()
