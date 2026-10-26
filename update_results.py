"""Atualiza até 100 concursos de quatro modalidades da Caixa."""
import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://servicebus2.caixa.gov.br/portaldeloterias/api/"
MODES = {"lotofacil": 15, "megasena": 6, "quina": 5, "timemania": 7}
HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

def fetch(mode, number=None):
    url = BASE + mode + ("/" + str(number) if number is not None else "")
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)

def valid(row, count):
    return (isinstance(row, dict) and isinstance(row.get("numero"), int)
            and isinstance(row.get("listaDezenas"), list)
            and len(row["listaDezenas"]) == count)

def run_mode(mode, count):
    path = Path("data") / (mode + ".json")
    previous = []
    if path.exists():
        try:
            previous = json.loads(path.read_text(encoding="utf-8")).get("results", [])
        except (ValueError, OSError):
            pass
    by_number = {r["numero"]: r for r in previous if valid(r, count)}
    latest = fetch(mode)
    if not valid(latest, count):
        raise RuntimeError("Resposta inesperada para " + mode)
    by_number[latest["numero"]] = latest
    for number in range(latest["numero"] - 1, max(0, latest["numero"] - 100), -1):
        if number in by_number:
            continue
        try:
            row = fetch(mode, number)
            if valid(row, count):
                by_number[number] = row
        except Exception as exc:
            print(mode, number, "falhou:", exc)
        time.sleep(0.1)
    selected = [by_number[n] for n in sorted(by_number, reverse=True) if n <= latest["numero"]][:100]
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps({"updated_at": datetime.now(timezone.utc).isoformat(),
                               "results": selected}, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)
    print(mode, len(selected), "concursos")

def main():
    failures = []
    for mode, count in MODES.items():
        try:
            run_mode(mode, count)
        except Exception as exc:
            failures.append(mode)
            print("Erro em", mode, str(exc))
    if len(failures) == len(MODES):
        raise RuntimeError("Nenhuma modalidade atualizada")

if __name__ == "__main__":
    main()
