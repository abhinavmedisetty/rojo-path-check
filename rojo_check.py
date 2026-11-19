"""Check filesystem mappings in a Rojo JSON project file."""

import argparse
import json
import sys
from pathlib import Path


def check_tree(tree, project_folder):
    """Yield problems with a node or its descendants."""
    pending = [("tree", tree)]
    while pending:
        location, node = pending.pop()
        if not isinstance(node, dict):
            yield f"{location}: expected an instance object"
            continue

        if "$path" in node:
            mapping = node["$path"]
            optional = isinstance(mapping, dict)
            target = mapping.get("optional") if optional else mapping
            if not isinstance(target, str) or not target or "\0" in target:
                yield f'{location}.$path: expected a path or {{"optional": "path"}}'
            else:
                try:
                    (project_folder / target).stat()
                except (FileNotFoundError, NotADirectoryError):
                    if not optional:
                        yield f"{location}.$path: missing {target!r}"
                except OSError as error:
                    yield f"{location}.$path: could not check {target!r}: {error.strerror}"

        pending.extend(
            (f"{location}[{name!r}]", child)
            for name, child in reversed(list(node.items()))
            if not name.startswith("$")
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, nargs="?", default=Path("default.project.json"))
    project = parser.parse_args().project

    try:
        config = json.loads(project.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError, RecursionError) as error:
        print(f"{project}: {error}", file=sys.stderr)
        return 2

    if not isinstance(config, dict) or not isinstance(config.get("tree"), dict):
        print(f"{project}: expected a top-level 'tree' object", file=sys.stderr)
        return 2

    problems = list(check_tree(config["tree"], project.parent))
    if problems:
        for problem in problems:
            print(f"{project}: {problem}", file=sys.stderr)
        return 1

    print(f"{project}: all required mapped paths exist")
    return 0


if __name__ == "__main__":
    sys.exit(main())
