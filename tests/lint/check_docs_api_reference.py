# Copyright (c) PyPTO Contributors.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.
# -----------------------------------------------------------------------------------------------------------
"""Check that public API docs cover the HTTP and generation schemas."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SERVER_PY = ROOT / "pypto_serving" / "serving" / "server" / "server.py"
CONFIG_TYPES_PY = ROOT / "pypto_serving" / "config" / "types.py"
COMPAT_DOC = ROOT / "docs" / "user-guide" / "vllm-compatibility.md"
CLI_DOC = ROOT / "docs" / "cli-reference" / "pypto-serving.md"


def _module(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _class_fields(module: ast.Module, class_name: str) -> list[str]:
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            fields = []
            for statement in node.body:
                if isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
                    fields.append(statement.target.id)
            return fields
    raise ValueError(f"class {class_name!r} not found")


def _route_paths(module: ast.Module) -> list[str]:
    paths = []
    for node in ast.walk(module):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (
            isinstance(func, ast.Attribute)
            and func.attr == "add_api_route"
            and isinstance(func.value, ast.Attribute)
            and func.value.attr == "app"
        ):
            continue
        if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
            paths.append(node.args[0].value)
    return paths


def _backticked_terms(markdown: str) -> set[str]:
    return set(re.findall(r"(?<!`)`([^`\n]+)`(?!`)", markdown))


def _require_terms(path: Path, terms: list[str], label: str) -> list[str]:
    text = path.read_text(encoding="utf-8")
    backticked = _backticked_terms(text)
    return [
        f"{path.relative_to(ROOT)}: missing documented {label}: `{term}`"
        for term in terms
        if term not in backticked
    ]


def main() -> int:
    server_module = _module(SERVER_PY)
    config_module = _module(CONFIG_TYPES_PY)

    completion_fields = _class_fields(server_module, "CompletionRequest")
    chat_fields = _class_fields(server_module, "ChatCompletionRequest")
    generate_fields = _class_fields(config_module, "GenerateConfig")
    routes = _route_paths(server_module)

    failures = []
    failures += _require_terms(COMPAT_DOC, routes, "route")
    failures += _require_terms(COMPAT_DOC, completion_fields, "completion request field")
    failures += _require_terms(COMPAT_DOC, chat_fields, "chat request field")
    failures += _require_terms(CLI_DOC, generate_fields, "GenerateConfig field")

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1

    print(
        "Validated docs coverage for "
        f"{len(routes)} routes, "
        f"{len(completion_fields)} completion fields, "
        f"{len(chat_fields)} chat fields, and "
        f"{len(generate_fields)} GenerateConfig fields."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
