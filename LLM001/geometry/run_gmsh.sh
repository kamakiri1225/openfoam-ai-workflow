#!/bin/sh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CASE_DIR="$SCRIPT_DIR/../case"
CONFIG_FILE="$SCRIPT_DIR/../config/LLM001.yaml"

echo "========================================"
echo "  LLM001 - Step 1: gmsh mesh generation"
echo "========================================"

python3 "$SCRIPT_DIR/LLM001_pumpA.py" --config "$CONFIG_FILE" "$@"

echo ""
echo "========================================"
echo "  LLM001 - Step 2: OpenFOAM mesh conversion"
echo "========================================"

if command -v gmshToFoam >/dev/null 2>&1; then
    (cd "$CASE_DIR" && ./Allmesh)
else
    echo "gmshToFoam not found."
    echo "Source OpenFOAM, then run:"
    echo "  cd $CASE_DIR"
    echo "  ./Allmesh"
fi

echo ""
echo "========================================"
echo "  Done"
echo "========================================"
