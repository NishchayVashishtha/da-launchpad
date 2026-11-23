"""Runs python practice solutions. Input: path to JSON {"root": <repo root>, "items": [{"id", "code"}]}.
Prints JSON {id: {"ok": true, "result": {...}} | {"ok": false, "error": "..."}} on the last stdout line.
Convention: code defines `load(dataset, table)` (provided) and assigns `result`."""
import sys, json, os, io, contextlib, traceback

inp = json.load(open(sys.argv[1]))
root = inp["root"]
sys.path.insert(0, os.path.join(root, "src", "lib", "py"))
from serialize import serialize  # noqa: E402
import pandas as pd  # noqa: E402
import numpy as np  # noqa: E402

_cache = {}


def load(dataset, table):
    p = os.path.join(root, "public", "data", "csv", dataset, table + ".csv")
    if p not in _cache:
        _cache[p] = pd.read_csv(p)
    return _cache[p].copy()


out = {}
for it in inp["items"]:
    ns = {"load": load, "pd": pd, "np": np, "__name__": "__main__"}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(it["code"], it["id"], "exec"), ns)
        if "result" not in ns:
            raise NameError("solution did not assign `result`")
        out[it["id"]] = {"ok": True, "result": serialize(ns["result"])}
    except BaseException:
        out[it["id"]] = {"ok": False, "error": traceback.format_exc(limit=3)}
print("\n@@RESULT@@" + json.dumps(out))
