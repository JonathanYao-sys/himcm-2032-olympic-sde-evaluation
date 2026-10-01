#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CANDIDATES=(
  "python3"
  "/opt/homebrew/bin/python3"
  "/usr/local/bin/python3"
  "/usr/bin/python3"
)

for PYTHON in "${CANDIDATES[@]}"; do
  if command -v "$PYTHON" >/dev/null 2>&1 \
    && "$PYTHON" -c 'import numpy, matplotlib' >/dev/null 2>&1; then
    echo "Using: $PYTHON"
    exec "$PYTHON" "$SCRIPT_DIR/make_figures.py"
  fi
done

cat >&2 <<'EOF'
No Python interpreter with numpy and matplotlib was found.

Recommended fix:
  /opt/homebrew/bin/python3 -m pip install -r requirements.txt
  /opt/homebrew/bin/python3 make_figures.py
EOF
exit 1
