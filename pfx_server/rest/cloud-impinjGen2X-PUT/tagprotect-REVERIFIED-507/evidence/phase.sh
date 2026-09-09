#!/bin/bash
# phase.sh <label> <mode_json> <start_body> <outdir>
TARGET=e28011b0a5050076c4d7530a
CONTROL=e28011b0a505007698ca0895
LABEL=$1; MODEF=$2; SB=$3; OUTDIR=$4
mkdir -p "$OUTDIR"
TH=0; CH=0
for i in 1 2 3 4 5; do
  /tmp/scan.sh "$MODEF" 10 "$OUTDIR/run$i.ndjson" "$SB" > "$OUTDIR/run$i.log" 2>&1
  T=$(grep -c "$TARGET"  "$OUTDIR/run$i.ndjson" 2>/dev/null | head -1)
  C=$(grep -c "$CONTROL" "$OUTDIR/run$i.ndjson" 2>/dev/null | head -1)
  T=${T:-0}; C=${C:-0}
  if [ "$T" -gt 0 ]; then TH=$((TH+1)); TS=SEEN; else TS=MISS; fi
  if [ "$C" -gt 0 ]; then CH=$((CH+1)); CS=SEEN; else CS=MISS; fi
  printf "  run%d: target=%-4s (%3d ev)  control=%-4s (%3d ev)\n" $i "$TS" "$T" "$CS" "$C"
done
echo "  >>> $LABEL : target $TH/5   control $CH/5"
echo "$LABEL,$TH,$CH" >> /tmp/results.csv
