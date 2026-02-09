#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: ./run_extraction.sh --schema <schema.json> --document <file> [options]

Arguments:
  --schema     Path to a JSON Schema file.
  --document   Path to a document file (PDF or image).
  --endpoint   Optional extract endpoint (default: https://api.dillydally.dev/v1/extract).
EOF
}

endpoint="${KIE_API_URL:-https://api.dillydally.dev/v1/extract}"
schema_path=""
document_path=""
model_id=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --schema)
      schema_path="$2"
      shift 2
      ;;
    --document)
      document_path="$2"
      shift 2
      ;;
    --endpoint)
      endpoint="$2"
      shift 2
      ;;
    --model)
      model_id="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$schema_path" || -z "$document_path" ]]; then
  echo "Error: --schema and --document are required." >&2
  usage
  exit 1
fi

if [[ ! -f "$schema_path" ]]; then
  echo "Error: schema file not found: $schema_path" >&2
  exit 1
fi

if [[ ! -f "$document_path" ]]; then
  echo "Error: document file not found: $document_path" >&2
  exit 1
fi

python3 - "$schema_path" "$document_path" "$model_id" <<'PY' | curl -sS -X POST \
  -H "Content-Type: application/json" \
  --data-binary @- \
  "$endpoint" | python3 -m json.tool
import base64
import json
import sys
from pathlib import Path

schema_path = Path(sys.argv[1])
document_path = Path(sys.argv[2])
model_id = sys.argv[3] if len(sys.argv) > 3 else ""

schema = json.loads(schema_path.read_text(encoding="utf-8"))
document_bytes = document_path.read_bytes()
document_base64 = base64.b64encode(document_bytes).decode("ascii")

document_type = "pdf" if document_bytes.startswith(b"%PDF") else "image"

payload = {
    "document": {"content": document_base64, "type": document_type},
    "schema": schema,
}

if model_id:
    payload["options"] = {"model": model_id}

print(json.dumps(payload))
PY
