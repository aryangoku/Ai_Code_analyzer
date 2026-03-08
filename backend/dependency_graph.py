import os
import re
import ast


def _module_id(file_path: str, base_path: str) -> str:
    """Convert file path to module id (e.g. repo/main/foo -> main.foo)."""
    rel = os.path.relpath(file_path, base_path)
    rel = rel.replace("\\", "/").replace(".py", "").replace("/", ".")
    return rel or "root"


def _parse_imports(code: str) -> list[str]:
    """Extract top-level module names from import statements."""
    modules = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name:
                        modules.append(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    modules.append(node.module.split(".")[0])
    except SyntaxError:
        # Fallback: simple regex for "import x" and "from x import"
        for m in re.finditer(r"\bimport\s+([\w.]+)", code):
            modules.append(m.group(1).split(".")[0])
        for m in re.finditer(r"\bfrom\s+([\w.]+)\s+import", code):
            modules.append(m.group(1).split(".")[0])
    return list(dict.fromkeys(modules))


def build_graph(repo_path: str) -> dict:
    """
    Build dependency graph from Python files in repo_path.
    Returns { "nodes": [{"id", "label"}], "edges": [{"source", "target"}] }.
    """
    nodes_map = {}
    edges = []

    python_files = []
    for root, dirs, files in os.walk(repo_path):
        for f in files:
            if f.endswith(".py"):
                python_files.append(os.path.join(root, f))

    for file_path in python_files:
        node_id = _module_id(file_path, repo_path)
        nodes_map[node_id] = {"id": node_id, "label": os.path.basename(file_path).replace(".py", "")}
        try:
            with open(file_path, "r", errors="ignore") as f:
                code = f.read()
        except Exception:
            continue
        for imp in _parse_imports(code):
            if imp in ("ast", "re", "os", "sys", "json", "time", "uuid", "shutil", "subprocess"):
                continue
            target_id = imp
            if target_id not in nodes_map:
                nodes_map[target_id] = {"id": target_id, "label": imp}
            edges.append({"source": node_id, "target": target_id})

    return {
        "nodes": list(nodes_map.values()),
        "edges": edges,
    }
