"""Atualiza arquivo estático de resultados; executado pelo GitHub Actions."""
import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = 'https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil'
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; Loteria/1.0)', 'Accept': 'application/json'}
OUT = Path('data/results.json')

def get(number=None):
    url = BASE + ('/' + str(number) if number is not None else '')
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.load(resp)

def valid(row):
    return isinstance(row, dict) and isinstance(row.get('numero'), int) and len(row.get('listaDezenas', [])) == 15

def main():
    previous = []
    if OUT.exists():
        try:
            previous = json.loads(OUT.read_text(encoding='utf-8')).get('results', [])
        except (ValueError, OSError):
            pass
    by_number = {r['numero']: r for r in previous if valid(r)}
    latest = get()
    if not valid(latest):
        raise RuntimeError('Resposta inesperada da fonte oficial; arquivo anterior preservado')
    by_number[latest['numero']] = latest
    for number in range(latest['numero'] - 1, max(0, latest['numero'] - 100), -1):
        if number in by_number:
            continue
        try:
            row = get(number)
            if valid(row):
                by_number[number] = row
        except Exception as exc:
            print('Falha no concurso', number, str(exc))
        time.sleep(0.15)
    results = [by_number[n] for n in sorted(by_number, reverse=True) if n <= latest['numero']][:100]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    temp = OUT.with_suffix('.tmp')
    temp.write_text(json.dumps({'updated_at': datetime.now(timezone.utc).isoformat(), 'results': results}, ensure_ascii=False), encoding='utf-8')
    os.replace(temp, OUT)
    print('Concursos salvos:', len(results))

if __name__ == '__main__':
    main()
