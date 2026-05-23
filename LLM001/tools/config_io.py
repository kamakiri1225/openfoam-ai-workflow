from __future__ import annotations

import ast
import os
from typing import Any


def _strip_comment(line: str) -> str:
    in_quote = False
    quote = ""
    out = []
    for ch in line:
        if ch in ("'", '"'):
            if in_quote and ch == quote:
                in_quote = False
                quote = ""
            elif not in_quote:
                in_quote = True
                quote = ch
        if ch == "#" and not in_quote:
            break
        out.append(ch)
    return "".join(out).rstrip()


def _parse_scalar(text: str) -> Any:
    text = text.strip()
    if text == "":
        return ""
    if text in ("true", "True"):
        return True
    if text in ("false", "False"):
        return False
    if text in ("null", "None", "~"):
        return None
    if text.startswith("[") and text.endswith("]"):
        return ast.literal_eval(text)
    if (text.startswith('"') and text.endswith('"')) or (
        text.startswith("'") and text.endswith("'")
    ):
        return ast.literal_eval(text)
    try:
        if any(ch in text for ch in (".", "e", "E")):
            return float(text)
        return int(text)
    except ValueError:
        return text


def _prepare_lines(path: str) -> list[tuple[int, str]]:
    prepared: list[tuple[int, str]] = []
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = _strip_comment(raw.rstrip("\n"))
            if not line.strip():
                continue
            indent = len(line) - len(line.lstrip(" "))
            prepared.append((indent, line.strip()))
    return prepared


def _parse_block(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(lines):
        return {}, index

    is_list = lines[index][0] == indent and lines[index][1].startswith("- ")
    if is_list:
        result = []
        while index < len(lines):
            line_indent, text = lines[index]
            if line_indent < indent:
                break
            if line_indent != indent or not text.startswith("- "):
                break

            item_text = text[2:].strip()
            index += 1
            if item_text == "":
                child, index = _parse_block(lines, index, indent + 2)
                result.append(child)
                continue

            if ":" in item_text:
                key, value = item_text.split(":", 1)
                item = {key.strip(): _parse_scalar(value)}
                if index < len(lines) and lines[index][0] > indent:
                    child, index = _parse_block(lines, index, lines[index][0])
                    if isinstance(child, dict):
                        item.update(child)
                result.append(item)
            else:
                result.append(_parse_scalar(item_text))
        return result, index

    result: dict[str, Any] = {}
    while index < len(lines):
        line_indent, text = lines[index]
        if line_indent < indent:
            break
        if line_indent > indent:
            break
        if text.startswith("- "):
            break
        key, value = text.split(":", 1)
        key = key.strip()
        value = value.strip()
        index += 1
        if value == "":
            child, index = _parse_block(lines, index, indent + 2)
            result[key] = child
        else:
            result[key] = _parse_scalar(value)
    return result, index


def load_config(path: str | None = None) -> dict[str, Any]:
    if path is None:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(root, "config", "LLM001.yaml")

    try:
        import yaml  # type: ignore

        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except ModuleNotFoundError:
        lines = _prepare_lines(path)
        data, _ = _parse_block(lines, 0, 0)
        return data
