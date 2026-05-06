My JGraph lab plots the notes of a specified major scale on top of a guitar fretboard. The major scale is a set of 7 musical notes
from a certain key, for example the major scale notes in the key of C are C, D, E, F, G, A, B. These notes exist in a variety of places 
on a guitar, and the scale can be played in order in different locations on the guitar by learning patterns. My program uses JGraph 
to visualize these patterns. An example of one of my images is `G_major_scale.png`.

My code uses 2 Python scripts to generate JGraph data which is then converted to a .png. These Python files have no dependencies outisde
of Python's standard libraries, and ran with no issues using Python3.11 on the Hydra machines. 

Running `sh plot.sh [key]` where key is a capital letter (A-G) or one of these letters followed by a 'b' or '#' to denote a flat or sharp key.
For example, 'A#' is the key of A sharp, which is also the key of "Bb" or B flat. 

Running `sh run.sh` calls `plot.sh` 5 times with 5 different keys. For each key, 3 files are output. A .jgr file that conatins the 
JGraph data, a .eps file that contains raw Postscript, and a .png file showing the JGraph. 
