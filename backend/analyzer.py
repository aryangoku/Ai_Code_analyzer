import os
import re
from radon.complexity import cc_visit

def analyze_code(repo_path):

    total_lines = 0
    file_count = 0
    largest_file = ""
    max_lines = 0
    complexity_total = 0
    functions = 0

    js_function_pattern = r'function\s+\w+\(|\w+\s*=\s*\(?.*\)?\s*=>'

    for root, dirs, files in os.walk(repo_path):

        for file in files:

            if file.endswith((".py",".js",".ts")):

                file_path = os.path.join(root,file)

                try:

                    with open(file_path,"r",errors="ignore") as f:

                        code = f.read()

                        lines = code.count("\n")

                        total_lines += lines
                        file_count += 1

                        if lines > max_lines:
                            max_lines = lines
                            largest_file = file

                        if file.endswith(".py"):
                            blocks = cc_visit(code)
                            complexity_total += sum(b.complexity for b in blocks)
                            functions += len(blocks)

                        if file.endswith(".js") or file.endswith(".ts"):
                            matches = re.findall(js_function_pattern, code)
                            functions += len(matches)

                except:
                    continue

    avg_complexity = 0

    if functions > 0:
        avg_complexity = complexity_total / functions

    return {
        "total_lines": total_lines,
        "file_count": file_count,
        "largest_file": largest_file,
        "avg_complexity": round(avg_complexity,2),
        "functions": functions
    }