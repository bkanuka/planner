planner
=======

Custom Planner with LaTeX and Python.  Originally from http://bkanuka.com/2011/11/custom-planner/

Use
=======
Open `page1.svg` with Inkscape.  Save file as pdf. 
 * Check the box "PDF+LaTeX: Omit text in PDF and create LaTeX file". 
 * Check the box "Export area is page". 
 * Unchecked "Export area is drawing".
 * Press OK
 * Do the same for `page2.svg`

Now run `python planner.py`

Errors will most likely be caused by an incomplete LaTeX installation. Install missing packages and try again.

(you can always try to get in contact if you're stuck!)

Right to Left
=======


    python planner.py && xelatex planner.tex
    pdftk planner.pdf cat 1-endsouth output planner-rev.pdf
    pdftops -level3 planner-rev.pdf - | psbook | psnup -s1 -2 -W7.0in -H8.5in -w8.5in -h14.0in -plegal | ps2pdf - planner-fa-book.pdf
    zathura planner-fa-book.pdf

papersize is currently chosen with `/etc/papersize` but there might be a better way
