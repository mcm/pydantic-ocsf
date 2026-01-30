#!/bin/bash

jq=$(command -v jq || true)
[ -z "$jq" ] && "Install jq to use this hook" && exit 1

contextJson = $(< /dev/stdin)
filePath = $(echo ${contextJson} | jq .tool_input.file_path )

[[ "$filePath" == *".py" ]] || exit 0

ruff check --fix $filePath
ruff format $filePath
mypy $filePath --ignore-missing-imports