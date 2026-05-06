#!/usr/bin/env python3

"""
Dylan Lewis 
CS594 @ UTK 
5/6/26

Computes which frets on each string belong to the major scale of the
given key, then outputs Jgraph commands to overlay coloured dots and
note-name labels on top of the fretboard produced by fretboard.py.
"""

import argparse
import sys
import os

# Allow importing from the same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fretboard import fret_x, string_y, board_extents
from fretboard import SCALE_LEN, NUM_FRETS, NUM_STRINGS, SCALE_LEN, STRING_LABEL_X

# Sorted order of notes starting from C 
CHROMATIC = ["C", "C#", "D", "D#", "E", "F",
             "F#", "G", "G#", "A", "A#", "B"]

# Enharmonic aliases (flats and sharps that are the same note, i.e. Db and C#)
ENHARMONIC = {
    "Db": "C#", "Eb": "D#", "Fb": "E",  "Gb": "F#",
    "Ab": "G#", "Bb": "A#", "Cb": "B",
    "C": "C",   "C#": "C#", "D": "D",   "D#": "D#",
    "E": "E",   "F": "F",   "F#": "F#", "G": "G",
    "G#": "G#", "A": "A",   "A#": "A#", "B": "B",
}

# Major scale intervals (offset from root)
MAJOR_INTERVALS = [0, 2, 4, 5, 7, 9, 11]

# Map strings to notes for open strings in scale (assumes standard tuning)
OPEN_NOTES = {1: "E", 2: "B", 3: "G", 4: "D", 5: "A", 6: "E"}

# Flat keys should use flat symbols in note labels
FLAT_KEYS     = {"F", "Bb", "Eb", "Ab", "Db", "Gb"}
SHARP_TO_FLAT = {"C#": "Db", "D#": "Eb", "F#": "Gb", "G#": "Ab", "A#": "Bb"}

# Scale dot size 
DOT_SIZE    = 0.22

# Red dot for root notes
ROOT_COLOR  = "0.95 0.20 0.15"   
# Blue dot for the other scale tones 
SCALE_COLOR = "0.20 0.55 0.90"   

FONT_SIZE   = 8

def note_index(note: str) -> int:
    """
    Convert a note into one that appears in the chromatic scale 
    """

    canonical = ENHARMONIC.get(note)
    return CHROMATIC.index(canonical)

def major_scale_indices(key: str) -> set:
    """
    Given a root, return a set containing the notes in that scale 
    """

    root = note_index(key)
    return {(root + i) % 12 for i in MAJOR_INTERVALS}

def note_at_fret(string_num: int, fret: int) -> str:
    """
    Determine the note at a given fret 
    """

    open_idx = note_index(OPEN_NOTES[string_num])
    return CHROMATIC[(open_idx + fret) % 12]

def display_name(note: str, key: str) -> str:
    """
    Return note name using flat symols for flat keys 
    """

    if key in FLAT_KEYS and note in SHARP_TO_FLAT:
        return SHARP_TO_FLAT[note]
    
    return note

def emit_scale_dots(key: str):
    """
    Draw scale dots on fretted notes, and handle open strings
    """

    scale_indices = major_scale_indices(key)
    root_idx      = note_index(key)
 
    # Open strings: 
    # - Only plot an open note if it's in the scale 
    for s in range(1, NUM_STRINGS + 1):
        y    = string_y(s)
        note = note_at_fret(s, 0)
        note_idx = note_index(note)
 
        if note_idx in scale_indices:
            is_root   = (note_idx == root_idx)
            dot_color = ROOT_COLOR if is_root else SCALE_COLOR
            label     = display_name(note, key)

            print(f"newcurve marktype circle marksize {DOT_SIZE:.3f} {DOT_SIZE:.3f}")
            print(f"  cfill {dot_color}  color {dot_color}")
            print(f"  pts {STRING_LABEL_X:.4f} {y:.4f}")
            print(f"newstring hjc vjc fontsize {FONT_SIZE} font Helvetica-Bold")
            print(f"  lcolor 1 1 1")
            print(f"  x {STRING_LABEL_X:.4f} y {y:.4f} : {label}")
        
    # Plot a scale not that's not on an open string 
    for s in range(1, NUM_STRINGS + 1):
        y = string_y(s)
        for fret in range(1, NUM_FRETS + 1):
            note     = note_at_fret(s, fret)
            note_idx = note_index(note)
 
            if note_idx not in scale_indices:
                continue
 
            x         = (fret_x(fret - 1) + fret_x(fret)) / 2
            is_root   = (note_idx == root_idx)
            dot_color = ROOT_COLOR if is_root else SCALE_COLOR
            label     = display_name(note, key)
 
            print(f"newcurve marktype circle marksize {DOT_SIZE:.3f} {DOT_SIZE:.3f}")
            print(f"  cfill {dot_color}  color {dot_color}")
            print(f"  pts {x:.4f} {y:.4f}")
            print(f"newstring hjc vjc fontsize {FONT_SIZE} font Helvetica-Bold")
            print(f"  lcolor 1 1 1")
            print(f"  x {x:.4f} y {y:.4f} : {label}")


def emit_legend(key: str):
    """
    Add the legend to the JGrpaph 
    """

    _, _, _, y1 = board_extents()
    r   = DOT_SIZE / 2

    lx  = SCALE_LEN + 0.25
    ly  = y1 - 0.18
    ly2 = ly - 0.32
 
    print(f"newcurve marktype circle marksize {DOT_SIZE:.3f} {DOT_SIZE:.3f}")
    print(f"  cfill {ROOT_COLOR}  color {ROOT_COLOR}")
    print(f"  pts {lx:.4f} {ly:.4f}")
    print(f"newstring hjl vjc fontsize 9 font Helvetica")
    print(f"  x {lx + r + 0.05:.4f} y {ly:.4f} : Root ({key.upper()})")
 
    print(f"newcurve marktype circle marksize {DOT_SIZE:.3f} {DOT_SIZE:.3f}")
    print(f"  cfill {SCALE_COLOR}  color {SCALE_COLOR}")
    print(f"  pts {lx:.4f} {ly2:.4f}")
    print(f"newstring hjl vjc fontsize 9 font Helvetica")
    print(f"  x {lx + r + 0.05:.4f} y {ly2:.4f} : Scale tone")

def emit_title(key: str):
    """
    Add the title to the bottom of the graph 
    """

    _, _, y0, _ = board_extents()

    print(f"newstring hjc vjt fontsize 14 font Helvetica-Bold")
    print(f"  x {SCALE_LEN / 2:.4f} y {y0 - 0.4:.4f} : {key} Major Scale")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--key", required=True)
    args = p.parse_args()

    key = args.key.capitalize()

    if key not in ENHARMONIC:
        print(f"Error: unknown key '{key}'.", file=sys.stderr)
        print(f"Valid keys: {', '.join(sorted(ENHARMONIC))}", file=sys.stderr)
        sys.exit(1)

    emit_scale_dots(key)
    emit_legend(key)
    emit_title(key)

if __name__ == "__main__":
    main()