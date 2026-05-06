#!/usr/bin/env python3

"""
Dylan Lewis 
CS594 @ UTK 
5/6/26

Outputs Jgraph commands that draw a blank guitar fretboard (standard 6-string, 12 frets).

The fret positions are spaced proportionally using the equal temperament
formula so the fretboard looks realistic 
    - x(n) = SCALE_LENGTH * (1 - 1/2^(n/12))
"""

# Define the fretboard layout 
NUM_FRETS   = 12          
NUM_STRINGS = 6
SCALE_LEN   = 10.0        
STRING_SEP  = 0.55         
BOARD_PAD_Y_BOTTOM = 0.35  
BOARD_PAD_Y_TOP    = 0.55  
NUT_WIDTH          = 0.10  
AXIS_PAD_Y_TOP     = 0.40

# X position of string-name labels
STRING_LABEL_X = -0.25

# Axis bounds extend beyond the board so nothing drawn in the margins gets clipped 
AXIS_X_MIN = STRING_LABEL_X - 0.20   
AXIS_X_MAX = SCALE_LEN + 1.1        

# Colors  (r g b)
COLOR_BOARD  = "0.18 0.10 0.04"  
COLOR_FRET   = "0.75 0.72 0.60"   
COLOR_STRING = "0.85 0.82 0.70"   
COLOR_NUT    = "0.90 0.87 0.75"   
COLOR_BORDER = "0.10 0.06 0.02"   

def fret_x(n, total_frets=NUM_FRETS, width=SCALE_LEN):
    """
    Return the X position of fret n 
    """

    if n == 0:
        return 0.0
    
    # position on a scale length normalised to `width`
    pos = width * (1.0 - 1.0 / (2 ** (n / 12)))

    # re-scale so fret `total_frets` maps exactly to `width`
    max_pos = width * (1.0 - 1.0 / (2 ** (total_frets / 12)))

    return pos / max_pos * width


def string_y(s):
    """
    Return Y position of string s (1=high-e, 6=low-E)
    """

    # string 1 at bottom, string 6 at top 
    return (NUM_STRINGS - s) * STRING_SEP

def board_extents():
    """
    Returns the corner points of the board  
    """

    x0 = 0.0
    x1 = SCALE_LEN
    y0 = string_y(NUM_STRINGS) - BOARD_PAD_Y_BOTTOM
    y1 = string_y(1)           + BOARD_PAD_Y_TOP
    return x0, x1, y0, y1
 
 
def axis_extents():
    """
    Returns the full axis bounds
    """

    _, _, y0, y1 = board_extents()
    return AXIS_X_MIN, AXIS_X_MAX, y0, y1 + AXIS_PAD_Y_TOP

def emit_axes():
    """
    Draw the axes for the full plot including padding around board 
    """

    ax0, ax1, ay0, ay1 = axis_extents()
    axis_w = ax1 - ax0
    axis_h = ay1 - ay0

    print(f"newgraph")
    print(f"  xaxis min {ax0:.4f} max {ax1:.4f} size {axis_w:.4f}")
    print(f"    nodraw")
    print(f"  yaxis min {ay0:.4f} max {ay1:.4f} size {axis_h:.4f}")
    print(f"    nodraw")
 
 
def emit_board_background(x0, x1, y0, y1):
    """
    Draw the fretboard  
    """

    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    w  = x1 - x0
    h  = y1 - y0

    print(f"newcurve marktype box marksize {w:.4f} {h:.4f}")
    print(f"  cfill {COLOR_BOARD}  color {COLOR_BOARD}")
    print(f"  pts {cx:.4f} {cy:.4f}")

def emit_nut(y0, y1):
    """
    Place the nut (vertical rectangle)
    """

    cx = NUT_WIDTH / 2
    cy = (y0 + y1) / 2
    h  = y1 - y0

    print(f"newcurve marktype box marksize {NUT_WIDTH:.4f} {h:.4f}")
    print(f"  cfill {COLOR_NUT}  color {COLOR_BORDER}")
    print(f"  pts {cx:.4f} {cy:.4f}")


def emit_frets(y0, y1):
    """
    Overlay frets on fretboard
    """

    fret_h = y1 - y0 + 0.04

    for n in range(1, NUM_FRETS + 1):
        x = fret_x(n)
        cy = (y0 + y1) / 2

        print(f"newcurve marktype box marksize 0.04 {fret_h:.4f}")
        print(f"  cfill {COLOR_FRET}  color {COLOR_FRET}")
        print(f"  pts {x:.4f} {cy:.4f}")

def emit_strings():
    """
    Place the strings as horizontal lines on the fretboard
    """

    x0 = 0.0
    x1 = SCALE_LEN

    # high-e to low-E
    thicknesses = [1.0, 1.2, 1.5, 2.0, 2.5, 3.0] 
    for s in range(1, NUM_STRINGS + 1):
        y = string_y(s)
        t = thicknesses[s - 1]

        print(f"newline color {COLOR_STRING} linethickness {t:.1f}")
        print(f"  pts {x0:.4f} {y:.4f}  {x1:.4f} {y:.4f}")

def emit_fret_numbers():
    """
    Add the fret-number labels below the board
    """
   
    _, _, y0, _ = board_extents()
    label_y = y0 - 0.20
    for n in range(1, NUM_FRETS + 1):
        x_left  = fret_x(n - 1)
        x_right = fret_x(n)
        cx      = (x_left + x_right) / 2
        
        print(f"newstring hjc vjt fontsize 8 font Helvetica")
        print(f"  x {cx:.4f} y {label_y:.4f} : {n}")

def main():
    x0, x1, y0, y1 = board_extents()

    emit_axes()
    emit_board_background(x0, x1, y0, y1)
    emit_nut(y0, y1)
    emit_frets(y0, y1)
    emit_strings()
    emit_fret_numbers()

if __name__ == "__main__":
    main()