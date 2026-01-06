#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 /path/to/file.pdf" >&2
  exit 1
fi

pdf="$1"

if ! command -v pdfinfo >/dev/null 2>&1; then
  echo "pdfinfo not found. Install poppler (macOS: brew install poppler)." >&2
  exit 1
fi

size_line="$(pdfinfo "$pdf" | awk -F': ' '/Page size/ {print $2}')"
if [[ -z "$size_line" ]]; then
  echo "Could not read page size from pdfinfo." >&2
  exit 1
fi

width="$(echo "$size_line" | awk '{print $1}')"
height="$(echo "$size_line" | awk '{print $3}')"

echo "Page size: ${width} x ${height} pts"
echo "Aspect ratio (width/height):"
awk -v w="$width" -v h="$height" 'BEGIN { printf "%.6f\n", w/h }'
echo
echo "Embed helper:"
cat <<EOF
<div style="width: 100%; aspect-ratio: ${width} / ${height};">
  <object data="/assets/your.pdf#toolbar=0&view=Fit"
          type="application/pdf"
          style="width: 100%; height: 100%; display: block;">
  </object>
</div>
EOF
