"""Build starter .ipynb files from scripts/notebooks/specs/*.json into public/downloads/notebooks/.
Spec: {filename, title, dataset, cells:[{type: markdown|code, source}]}. Deterministic output."""
import json, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
out = root / "public" / "downloads" / "notebooks"; out.mkdir(parents=True, exist_ok=True)
for spec_path in sorted((root / "scripts" / "notebooks" / "specs").glob("*.json")):
    s = json.loads(spec_path.read_text())
    cells = []
    for c in s["cells"]:
        src = c["source"] if isinstance(c["source"], str) else "".join(c["source"])
        lines = src.splitlines(keepends=True)
        if c["type"] == "code":
            cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": lines})
        else:
            cells.append({"cell_type": "markdown", "metadata": {}, "source": lines})
    nb = {"nbformat": 4, "nbformat_minor": 5, "cells": cells,
          "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
                       "language_info": {"name": "python"}}}
    name = s["filename"].removesuffix(".ipynb") + ".ipynb"
    (out / name).write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
    print(name, len(cells), "cells")
