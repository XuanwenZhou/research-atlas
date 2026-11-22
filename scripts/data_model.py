"""Shared canonical data operations. Python 3.10+, standard library only."""
import copy
import datetime as dt
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlparse, unquote

STATUS = {'verified', 'partial', 'pending', 'disputed'}
TYPES = {'direct', 'extension', 'borrow', 'theme'}
ID = re.compile(r'^[A-Za-z0-9_.:-]+$')

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def title_key(s):
    return ''.join(c for c in unicodedata.normalize('NFKC', str(s or '')).casefold() if c.isalnum())

def doi_key(s):
    s = unquote(str(s or '')).strip().lower()
    return re.sub(r'^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)', '', s)

def arxiv_key(s):
    s = re.sub(r'^https?://arxiv\.org/(?:abs|pdf)/', '', str(s or '').strip(), flags=re.I)
    return re.sub(r'v\d+$', '', s.removesuffix('.pdf'), flags=re.I).lower()

def date_ok(s):
    if s is None or s == '':
        return True
    if not isinstance(s, str) or not re.fullmatch(r'\d{4}(?:-\d{2})?(?:-\d{2})?', s):
        return False
    try:
        dt.date.fromisoformat(s + ('-01-01' if len(s) == 4 else '-01' if len(s) == 7 else ''))
        return True
    except ValueError:
        return False

def valid_url(s):
    try:
        p = urlparse(s)
        return p.scheme in {'http', 'https'} and bool(p.hostname) and not any(c.isspace() for c in s)
    except (ValueError, TypeError):
        return False

def duplicate_candidates(data):
    buckets = {}
    for p in data.get('papers', []):
        if not isinstance(p, dict) or not isinstance(p.get('id'), str):
            continue
        for kind, value in [('doi', doi_key(p.get('doi'))), ('arxiv', arxiv_key(p.get('arxiv_id'))), ('title', title_key(p.get('title')))]:
            if value:
                buckets.setdefault((kind, value), []).append(p['id'])
    return [{'kind': k, 'key': v, 'paper_ids': ids, 'action': 'review_required'}
            for (k, v), ids in sorted(buckets.items()) if len(ids) > 1]

def validate(data):
    errors, warnings = [], []
    def issue(level, code, location, message):
        (errors if level == 'error' else warnings).append(dict(code=code, location=location, message=message))
    if not isinstance(data, dict):
        return dict(ok=False, errors=[dict(code='root', location='$', message='顶层必须为对象')], warnings=[], counts={})
    tables = {}
    for name in ('papers', 'methods', 'groups', 'edges', 'surveys', 'research_tracks'):
        rows = data.get(name)
        if not isinstance(rows, list) or any(not isinstance(x, dict) for x in rows):
            issue('error', 'table', name, '必需为对象数组')
            rows = []
        tables[name] = {}
        for n, row in enumerate(rows):
            ident = row.get('id')
            if not isinstance(ident, str) or not ID.fullmatch(ident):
                issue('error', 'id', f'{name}[{n}]', 'ID 缺失或包含不支持字符')
            elif ident in tables[name]:
                issue('error', 'duplicate_id', f'{name}.{ident}', 'ID 重复')
            else:
                tables[name][ident] = row
    meta = data.get('metadata')
    if not isinstance(meta, dict):
        issue('error', 'metadata', 'metadata', 'metadata 必需为对象')
        meta = {}
    if meta.get('schema_version') != '1.0':
        issue('error', 'schema_version', 'metadata', '仅支持 schema_version=1.0')
    for key in ('domain', 'search_cutoff', 'coverage_limitations'):
        if not meta.get(key):
            issue('warning', 'metadata_missing', f'metadata.{key}', '缺少范围或覆盖说明')
    if not date_ok(meta.get('search_cutoff')):
        issue('error', 'date', 'metadata.search_cutoff', '日期格式或日历值无效')
    if not meta.get('search_log'):
        issue('warning', 'search_log', 'metadata', '无实际检索日志，不得宣称穷尽或最新')
    def ref(ids, table, loc):
        if not isinstance(ids, list):
            issue('error', 'array', loc, '引用必须为数组')
            return
        for ident in ids:
            if not isinstance(ident, str) or ident not in table:
                issue('error', 'dangling_reference', loc, f'无效引用: {ident}')
    def sources(row, loc):
        ev = row.get('evidence', [])
        prov = row.get('provenance', [])
        if not isinstance(ev, list) or any(not isinstance(e, dict) for e in ev):
            issue('error', 'evidence', loc, 'evidence 必须为对象数组')
            ev = []
        if not isinstance(prov, list) or any(not isinstance(e, dict) for e in prov):
            issue('error', 'provenance', loc, 'provenance 必须为对象数组')
            prov = []
        if not ev and not prov:
            issue('warning', 'no_source', loc, '缺少来源')
        for s in ev + prov:
            if not s.get('url') and not s.get('source_id'):
                issue('warning', 'source_missing', loc, '来源缺少 URL 或本地材料键')
            if s.get('survey_id') and s['survey_id'] not in tables['surveys']:
                issue('error', 'survey_reference', loc, '来源综述不存在')
        for e in ev:
            if row.get('verification') == 'verified' and not e.get('checked_at'):
                issue('warning', 'evidence_date', loc, '已核证据缺少核验日期')
        return ev
    def state(row, loc):
        if row.get('verification') not in STATUS:
            issue('error', 'verification', loc, 'verification 状态缺失或无效')
        elif row['verification'] != 'verified':
            issue('warning', 'unverified', loc, '信息仍有待核或争议')
    for ident, p in tables['papers'].items():
        loc = 'papers.' + ident
        if not p.get('title'):
            issue('error', 'title', loc, '缺少论文标题')
        if not isinstance(p.get('authors'), list) or any(not isinstance(a, str) for a in p.get('authors', [])):
            issue('error', 'authors', loc, 'authors 必须为姓名数组')
        elif not p['authors']:
            issue('warning', 'authors_missing', loc, '作者待核')
        for key in ('first_public_date', 'publication_date'):
            if not date_ok(p.get(key)):
                issue('error', 'date', loc + '.' + key, '日期格式或日历值无效')
        if not p.get('first_public_date'):
            issue('warning', 'date_missing', loc, '首次公开日期待核')
        if isinstance(p.get('first_public_date'), str) and isinstance(p.get('publication_date'), str) and p['first_public_date'][:4] > p['publication_date'][:4]:
            issue('warning', 'date_order', loc, '首次公开年晚于发表年，需回查')
        if p.get('doi') and not re.fullmatch(r'10\.\d{4,9}/\S+', doi_key(p['doi'])):
            issue('error', 'doi', loc, 'DOI 语法无效')
        state(p, loc)
        sources(p, loc)
    for ident, m in tables['methods'].items():
        loc = 'methods.' + ident
        if not m.get('name'):
            issue('error', 'name', loc, '缺少方法名')
        if not m.get('paper_ids'):
            issue('error', 'paper_missing', loc, '至少关联一篇论文')
        ref(m.get('paper_ids'), tables['papers'], loc + '.paper_ids')
        ref(m.get('group_ids'), tables['groups'], loc + '.group_ids')
        if m.get('primary_group') not in tables['groups']:
            issue('error', 'primary_group', loc, '主分类不存在')
        elif m['primary_group'] not in (m.get('group_ids') or []):
            issue('error', 'primary_membership', loc, 'group_ids 必须包含主分类')
        for key in ('tags', 'aliases', 'modules'):
            if not isinstance(m.get(key), list) or any(not isinstance(x, str) for x in m.get(key, [])):
                issue('error', 'array', loc + '.' + key, '必须为字符串数组')
        if m.get('featured') and not m.get('featured_reason'):
            issue('warning', 'featured_reason', loc, '代表性推荐依据缺失')
        if not m.get('classification_basis'):
            issue('warning', 'classification_basis', loc, '分类依据待补')
        if m.get('problem') and m.get('mechanism') and title_key(m['problem']) == title_key(m['mechanism']):
            issue('warning', 'problem_equals_mechanism', loc, 'problem 与 mechanism 内容重复；无独立问题陈述时请置 null')
        state(m, loc)
        sources(m, loc)
    def group_check(groups, loc):
        gm = {g.get('id'): g for g in groups}
        if len(gm) != len(groups) or any(not isinstance(k, str) or not ID.fullmatch(k) for k in gm):
            issue('error', 'group_id', loc, '分类 ID 缺失或重复')
        seen_roots, current_root, seen_ids = set(), None, set()
        fragmented = False
        for g in groups:
            gid = g.get('id')
            parent = g.get('parent_id')
            if parent:
                if parent not in gm or parent == gid or gm.get(parent, {}).get('parent_id'):
                    issue('error', 'hierarchy', loc + '.' + str(gid), '仅允许无环的一二级分类')
                elif parent not in seen_ids:
                    fragmented = True
            root = parent if (parent and parent in gm) else gid
            if root != current_root:
                if root in seen_roots:
                    fragmented = True
                if current_root is not None:
                    seen_roots.add(current_root)
                current_root = root
            if isinstance(gid, str):
                seen_ids.add(gid)
            ref(g.get('representative_method_ids', []), tables['methods'], loc)
            if not g.get('name'):
                issue('error', 'group_name', loc, '分类名称缺失')
            if not g.get('definition') or not g.get('rationale'):
                issue('warning', 'taxonomy_basis', loc + '.' + str(gid), '分类定义或依据待补')
        if fragmented:
            issue('warning', 'group_order_fragmented', loc, '二级分类未紧随所属一级分类连续排列，建议保持同父分组相邻')
        return gm
    group_check(list(tables['groups'].values()), 'groups')
    seen_edges = set()
    def earliest_year(mid):
        m = tables['methods'].get(mid)
        if not m:
            return None
        ys = [tables['papers'][pid]['first_public_date'][:4]
              for pid in m.get('paper_ids', [])
              if pid in tables['papers'] and isinstance(tables['papers'][pid].get('first_public_date'), str)
              and len(tables['papers'][pid]['first_public_date']) >= 4]
        return min(ys) if ys else None
    def edge_check(edges, loc):
        pair_seen = {}
        for e in edges:
            el = loc + '.' + str(e.get('id'))
            if not isinstance(e.get('id'), str) or not ID.fullmatch(e['id']) or e['id'] in seen_edges:
                issue('error', 'edge_id', el, '边 ID 缺失、非法或全局重复')
            seen_edges.add(e.get('id'))
            src, tgt, etype = e.get('source'), e.get('target'), e.get('type')
            ref([src, tgt], tables['methods'], el)
            if src == tgt:
                issue('error', 'self_edge', el, '不允许自环')
            if etype not in TYPES:
                issue('error', 'edge_type', el, '关系类型无效')
            if isinstance(src, str) and isinstance(tgt, str) and src != tgt and etype in TYPES:
                ukey = frozenset((src, tgt))
                prev = pair_seen.setdefault(ukey, [])
                if any((p_s == src and p_t == tgt) or p_ty == 'theme' or etype == 'theme' for p_s, p_t, p_ty in prev):
                    issue('warning', 'duplicate_edge_pair', el, '同一对方法存在重复边或与技术边重叠的同方向边')
                prev.append((src, tgt, etype))
                if etype != 'theme':
                    sy, ty = earliest_year(src), earliest_year(tgt)
                    if sy and ty and sy > ty:
                        issue('warning', 'reverse_date_edge', el, f'起点首次公开年({sy})晚于终点({ty})，请核查预印本与发表日期')
            if e.get('claim_basis') not in {'fact', 'inference'}:
                issue('error', 'claim_basis', el, '必须区分事实与推断')
            c = e.get('confidence')
            if c is None:
                issue('warning', 'confidence_missing', el, '置信度尚未校准')
            elif not isinstance(c, (int, float)) or isinstance(c, bool) or not 0 <= c <= 1:
                issue('error', 'confidence', el, '置信度必须在 0–1')
            if not e.get('description') or not e.get('basis'):
                issue('warning', 'edge_basis', el, '关系说明或判断依据缺失')
            state(e, el)
            ev = sources(e, el)
            primary = any(x.get('source_type') == 'primary_paper' and x.get('access_level') == 'full_text'
                          and x.get('locator') and (x.get('url') or x.get('source_id')) and x.get('checked_at')
                          and (x.get('summary') or x.get('quote')) for x in ev)
            if etype != 'theme' and e.get('verification') == 'verified' and (e.get('claim_basis') != 'fact' or not primary):
                issue('error', 'unsupported_verified_edge', el, '已核技术边必须是事实并有原始全文证据、位置和核验日')
            elif etype != 'theme' and not primary:
                issue('warning', 'edge_evidence_pending', el, '技术关系缺少已定位的原始全文证据')
            if etype != 'theme' and e.get('claim_basis') == 'fact' and ev and all(x.get('access_level') in {'metadata', 'metadata_only'} for x in ev):
                issue('warning', 'title_only_fact_edge', el, '仅凭题名/元数据记录不得标为 fact，请核对摘要或全文后确认')
    edge_check(list(tables['edges'].values()), 'edges')
    if len(tables['methods']) >= 20:
        connected = {nid for e in tables['edges'].values() for nid in (e.get('source'), e.get('target')) if nid in tables['methods']}
        isolated = len(tables['methods']) - len(connected)
        if isolated > len(tables['methods']) * 0.5:
            issue('warning', 'isolated_methods_high', 'edges', f'孤立方法占比偏高（{isolated}/{len(tables["methods"])}），请核查新增批次是否遗漏有依据的关系，勿无依据强连')
    for tid, t in tables['research_tracks'].items():
        loc = 'research_tracks.' + tid
        ref(t.get('method_ids', []), tables['methods'], loc)
        if 'global_edge_ids' in t:
            ref(t['global_edge_ids'], tables['edges'], loc + '.global_edge_ids')
        gs = t.get('groups', [])
        assignments, edges = t.get('assignments', []), t.get('edges', [])
        if not all(isinstance(a, list) and all(isinstance(x, dict) for x in a) for a in (gs, assignments, edges)):
            issue('error', 'track_shape', loc, '专题分类、归属及边必须为对象数组')
            continue
        gm = group_check(gs, loc + '.groups')
        assigned = set()
        for a in assignments:
            ref([a.get('method')], tables['methods'], loc)
            ref(a.get('memberships', []), gm, loc)
            if a.get('method') in assigned or a.get('method') not in t.get('method_ids', []):
                issue('error', 'track_assignment', loc, '专题归属重复或不属于专题成员')
            assigned.add(a.get('method'))
            if a.get('primary') not in gm or a.get('primary') not in a.get('memberships', []):
                issue('error', 'track_primary', loc, '专题主归属无效')
        if gm and assigned != set(t.get('method_ids', [])):
            issue('error', 'track_coverage', loc, '专题路线未覆盖所有成员')
        edge_check(edges, loc + '.edges')
        for e in edges:
            if any(e.get(k) not in t.get('method_ids', []) for k in ('source', 'target')):
                issue('error', 'track_edge_membership', loc, '专题边端点不在专题成员中')
    for candidate in duplicate_candidates(data):
        issue('warning', 'duplicate_candidate', 'papers', f"{candidate['kind']}: {candidate['paper_ids']}")
    def scan(x, loc):
        if isinstance(x, dict):
            for k, v in x.items():
                if k == 'legacy':
                    continue
                if isinstance(v, str) and k in {'url', 'source_url'} and v:
                    if not valid_url(v):
                        issue('error', 'unsafe_url', loc + '.' + k, '只允许有效 http/https URL')
                    elif x.get('url_status') != 'verified':
                        issue('warning', 'url_unchecked', loc + '.' + k, '未记录实际链接访问核验')
                if k == 'checked_at' and not date_ok(v):
                    issue('error', 'date', loc + '.' + k, '核验日期无效')
                scan(v, loc + '.' + k)
        elif isinstance(x, list):
            for i, v in enumerate(x):
                scan(v, f'{loc}[{i}]')
    scan(data, '$')
    return dict(ok=not errors, errors=errors, warnings=warnings,
                counts={k: len(v) for k, v in tables.items()},
                scope='结构和证据字段校验；未进行在线链接访问或学术真实性复核')

def view_model(data):
    papers = {p['id']: p for p in data['papers']}
    methods = []
    for m in data['methods']:
        ps = [papers[i] for i in m['paper_ids']]
        p = ps[0]
        dates = sorted(x['first_public_date'] for x in ps if x.get('first_public_date'))
        legacy = m.get('legacy', {})
        row = dict(legacy)
        row.update(m)
        row.update(title=p['title'], authors=p.get('authors', []), papers=ps,
                   date=dates[0] if dates else '时间待核', group=m['primary_group'],
                   url=p.get('url'), tech=m.get('mechanism'), limit=m.get('limitations'),
                   references=m.get('provenance', []), dateBasis=p.get('date_basis', ''),
                   dateAudit=legacy.get('dateAudit'), publication=legacy.get('publication'))
        methods.append(row)
    groups = [dict(g, desc=g.get('definition', ''), index=g.get('index', i)) for i, g in enumerate(data['groups'])]
    def edge(e):
        return dict(e, label=e.get('description', ''), evidenceText='；'.join(x.get('summary', '') for x in e.get('evidence', [])),
                    url=next((x.get('url') for x in e.get('evidence', []) if x.get('url')), ''), origin=e.get('claim_basis'))
    tracks = []
    for t in data['research_tracks']:
        if t.get('enabled', True):
            tracks.append(dict(t, groups=[dict(g, desc=g.get('definition', ''), index=g.get('index', i)) for i,g in enumerate(t.get('groups', []))],
                               edges=[edge(e) for e in t.get('edges', [])]))
    return dict(methods=methods, groups=groups, edges=[edge(e) for e in data['edges']],
                surveys=data['surveys'], tracks=tracks, metadata=data['metadata'], canonical=data)

def html_payload(data):
    """Slim single-source payload embedded in HTML; the viewer hydrates view models client-side."""
    return dict(canonical=data)

def merge_papers(data, plan):
    result = copy.deepcopy(data)
    by_id = {p['id']: p for p in result['papers']}
    if not isinstance(plan, dict) or not plan or any(not isinstance(k, str) or not isinstance(v, str) for k, v in plan.items()):
        raise ValueError('合并计划必须为非空 old_id: retained_id 对象')
    if any(k not in by_id or v not in by_id or k == v or v in plan for k, v in plan.items()):
        raise ValueError('合并计划有无效 ID、自合并或链式映射；请直接映射至保留 ID')
    # Do not silently resolve conflicting metadata; user resolves it before planning.
    clusters = {}
    for old, kept in plan.items():
        clusters.setdefault(kept, [by_id[kept]]).append(by_id[old])
    for kept, cluster in clusters.items():
        for field, normalizer in [('doi', doi_key), ('arxiv_id', arxiv_key)]:
            values = {normalizer(p.get(field)) for p in cluster if p.get(field)}
            if len(values) > 1:
                raise ValueError(f'{kept}: {field} 存在冲突，先人工核对')
    for old, kept in plan.items():
        a, b = by_id[old], by_id[kept]
        b.setdefault('merged_records', []).append(copy.deepcopy(a))
        b['previous_ids'] = list(dict.fromkeys(b.get('previous_ids', []) + [old] + a.get('previous_ids', [])))
        for key, value in a.items():
            if key != 'id' and not b.get(key) and value:
                b[key] = value
        for key in ('provenance', 'evidence', 'aliases'):
            vals = b.get(key, []) + a.get(key, [])
            b[key] = list({json.dumps(x, sort_keys=True, ensure_ascii=False): x for x in vals}.values())
        if a.get('verification') != b.get('verification'):
            b['verification'] = 'pending'
    result['papers'] = [p for p in result['papers'] if p['id'] not in plan]
    for m in result['methods']:
        m['paper_ids'] = list(dict.fromkeys(plan.get(i, i) for i in m['paper_ids']))
    result['metadata'].setdefault('paper_id_redirects', {}).update(plan)
    result['metadata'].setdefault('change_log', []).append(dict(action='merge_papers', redirects=plan))
    return result
