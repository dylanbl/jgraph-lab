#!/bin/bash

# Error check arguments 
if [[ $# -gt 2 ]]; then
    echo "Usage: $0 <KEY> [output_filename]"
    echo "  KEY   : note name, e.g.  G  C#  Bb  F"
    echo "  output_filename (optional): filename stem, default '<key>_major_scale'"
    exit 1
fi

# Read scale key 
KEY="$1"

# Build a filesystem-safe default output name
SAFE_KEY=$(echo "$KEY" | tr '#' 's' | tr '/' '_')
OUTPUT_FILENAME="${3:-${SAFE_KEY}_major_scale}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JGR_FILE="${OUTPUT_FILENAME}.jgr"
EPS_FILE="${OUTPUT_FILENAME}.eps"
PNG_FILE="${OUTPUT_FILENAME}.png"

# Generate JGraph source file by calling 2 Python scripts 
echo "Generating Jgraph source as ${JGR_FILE}"

{
    # Generate fretboard
    python3 "${SCRIPT_DIR}/fretboard.py"

    # Generate scale notes, legend, etc. 
    python3 "${SCRIPT_DIR}/scale.py" --key "${KEY}"

} > "${JGR_FILE}"

echo "Jgraph source written to ${JGR_FILE}"

# Write JGraph as .eps 
echo "Running jgraph into ${EPS_FILE}"
jgraph "${JGR_FILE}" > "${EPS_FILE}"
echo "EPS written to ${EPS_FILE}"

# Convert .eps to .png 
echo "Converting EPS to PNG"
convert -density 300 -background white -flatten "${EPS_FILE}" "${PNG_FILE}"
echo "PNG written to ${PNG_FILE}"