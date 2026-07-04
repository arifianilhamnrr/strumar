#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MP="$ROOT/vendor/mediapipe/hands"
MP_VER="0.4.1646424915"
CU_VER="0.3.1640029074"

mkdir -p "$MP" "$ROOT/vendor/mediapipe/camera_utils"

MIN_BYTES=(
  "hands_solution_packed_assets.data:4000000"
  "hand_landmark_full.tflite:5000000"
  "hand_landmark_lite.tflite:2000000"
  "hands_solution_simd_wasm_bin.wasm:6000000"
  "hands_solution_wasm_bin.wasm:6000000"
)

min_for() {
  local name="$1" entry key val
  for entry in "${MIN_BYTES[@]}"; do
    key="${entry%%:*}"
    val="${entry#*:}"
    if [ "$key" = "$name" ]; then
      echo "$val"
      return 0
    fi
  done
  echo 0
}

download_file() {
  local dest="$1"
  shift
  local url tmp size min max name
  name="$(basename "$dest")"
  tmp="${dest}.part"
  min="$(min_for "$name")"
  max=0
  case "$name" in
    hand_landmark_full.tflite) max=6000000 ;;
    hands.binarypb) max=5000 ;;
    hands.js|hands_solution_packed_assets_loader.js) max=100000 ;;
  esac

  rm -f "$tmp"

  for url in "$@"; do
    echo "  → $url"
    if curl -fSL \
      --retry 8 --retry-delay 2 --retry-all-errors \
      --connect-timeout 20 --max-time 600 \
      "$url" -o "$tmp"; then
      size="$(wc -c < "$tmp")"
      if [ "$min" -gt 0 ] && [ "$size" -lt "$min" ]; then
        echo "  ! terlalu kecil ($size < $min), coba mirror berikutnya..."
        rm -f "$tmp"
        continue
      fi
      if [ "$max" -gt 0 ] && [ "$size" -gt "$max" ]; then
        echo "  ! terlalu besar ($size > $max), kemungkinan korup — coba mirror berikutnya..."
        rm -f "$tmp"
        continue
      fi
      mv -f "$tmp" "$dest"
      echo "  ok $name ($size bytes)"
      return 0
    fi
    echo "  ! gagal dari mirror ini"
    rm -f "$tmp"
  done

  echo "ERROR: gagal download $name" >&2
  return 1
}

JS_DELIVR="https://cdn.jsdelivr.net/npm/@mediapipe"
UNPKG="https://unpkg.com/@mediapipe"

echo "== MediaPipe Hands =="
HANDS_FILES=(
  hands.js
  hands.binarypb
  hands_solution_packed_assets.data
  hands_solution_packed_assets_loader.js
  hands_solution_simd_wasm_bin.js
  hands_solution_simd_wasm_bin.wasm
  hands_solution_wasm_bin.js
  hands_solution_wasm_bin.wasm
  hand_landmark_full.tflite
  hand_landmark_lite.tflite
)

for f in "${HANDS_FILES[@]}"; do
  echo "[$f]"
  download_file "$MP/$f" \
    "$JS_DELIVR/hands@$MP_VER/$f" \
    "$UNPKG/hands@$MP_VER/$f"
done

echo "== MediaPipe Camera Utils =="
download_file "$ROOT/vendor/mediapipe/camera_utils/camera_utils.js" \
  "$JS_DELIVR/camera_utils@$CU_VER/camera_utils.js" \
  "$UNPKG/camera_utils@$CU_VER/camera_utils.js"

echo "== Tone.js =="
download_file "$ROOT/Tone.js" \
  "https://cdn.jsdelivr.net/npm/tone@14.8.49/build/Tone.js" \
  "https://unpkg.com/tone@14.8.49/build/Tone.js"

echo ""
echo "Done. Semua vendor file siap."