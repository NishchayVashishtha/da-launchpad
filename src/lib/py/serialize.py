"""Shared serializer: turns a practice `result` into {columns, rows} or {value}.
Used by the browser Pyodide runner (loaded as raw text) and by scripts/py_harness.py."""
import json, math, datetime


def _scalar(v):
    try:
        import numpy as np
        if isinstance(v, np.generic):
            v = v.item()
        elif isinstance(v, np.ndarray):
            return [_scalar(x) for x in v.tolist()]
    except ImportError:
        pass
    try:
        import pandas as pd
        if v is pd.NaT:
            return None
        if isinstance(v, pd.Timestamp):
            return str(v)
    except ImportError:
        pass
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    if isinstance(v, (datetime.date, datetime.datetime)):
        return str(v)
    if isinstance(v, (set, frozenset)):
        try:
            v = sorted(v)
        except TypeError:
            v = list(v)
    if isinstance(v, (list, tuple)):
        return [_scalar(x) for x in v]
    if isinstance(v, dict):
        return {str(k): _scalar(x) for k, x in v.items()}
    if isinstance(v, bytes):
        return v.decode("utf-8", "replace")
    return v


def serialize(result):
    try:
        import pandas as pd
    except ImportError:
        pd = None
    if pd is not None:
        if isinstance(result, pd.Series):
            name = result.name if result.name is not None else "value"
            if isinstance(result.index, pd.RangeIndex):
                result = result.to_frame(name=name)
            else:
                result = result.rename(name).reset_index()
        if isinstance(result, pd.DataFrame):
            df = result
            if not isinstance(df.index, pd.RangeIndex) or df.index.name is not None:
                df = df.reset_index()
            return {
                "columns": [str(c) for c in df.columns],
                "rows": [[_scalar(x) for x in row] for row in df.itertuples(index=False, name=None)],
            }
    return {"value": _scalar(result)}


def to_json(result):
    return json.dumps(serialize(result))
