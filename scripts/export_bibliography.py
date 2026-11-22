"""Export paper-level CSV and BibTeX without inventing unknown metadata."""
import argparse
import csv
from pathlib import Path
from data_model import read_json, validate

def csv_cell(value):
    s = '' if value is None else str(value)
    return "'" + s if s.lstrip().startswith(('=', '+', '-', '@')) or s.startswith(('\t', '\r', '\n')) else s

def bib_escape(value):
    chars = {'\\': r'{\textbackslash}', '{': r'\{', '}': r'\}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '~': r'{\textasciitilde}', '^': r'{\textasciicircum}'}
    return ''.join(chars.get(c, c) for c in str(value)).replace('\n', ' ')

def export(data, directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    keys = ['id', 'title', 'authors', 'doi', 'arxiv_id', 'first_public_date', 'publication_date', 'venue', 'publication_status', 'url', 'verification']
    with (directory / 'bibliography.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        for p in data['papers']:
            writer.writerow([csv_cell('; '.join(p.get(k, [])) if k == 'authors' else p.get(k)) for k in keys])
    entries = []
    for p in data['papers']:
        fields = {'title': p['title'], 'author': ' and '.join(p.get('authors', [])), 'doi': p.get('doi'), 'eprint': p.get('arxiv_id'), 'url': p.get('url')}
        # Publication year belongs to published/accepted records, not arXiv year guessed from ID.
        date = p.get('publication_date') or p.get('first_public_date')
        if date:
            fields['year'] = date[:4]
        if p.get('venue'):
            fields['howpublished'] = p['venue']
        if p.get('arxiv_id'):
            fields['archivePrefix'] = 'arXiv'
        entries.append('@misc{' + p['id'] + ',\n' + ',\n'.join(
            '  ' + k + ' = {' + ('{' + bib_escape(v) + '}' if k == 'title' else bib_escape(v)) + '}'
            for k, v in fields.items() if v) + '\n}')
    (directory / 'bibliography.bib').write_text('\n\n'.join(entries) + '\n', encoding='utf-8')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input')
    p.add_argument('--output-dir', required=True)
    a = p.parse_args()
    data = read_json(a.input)
    if validate(data)['errors']:
        p.exit(1, '数据结构错误，请先运行 validate_data.py\n')
    export(data, a.output_dir)
    print('CSV and BibTeX exported.')

if __name__ == '__main__':
    main()
