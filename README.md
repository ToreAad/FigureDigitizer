# FigureDigitizer
Some simple scripts to load figures drawn in inkscape in python

Sample image from: https://commons.wikimedia.org/wiki/File:Geologic_cross_section_of_Capitol_Reef_NP.png

Work in progress. Poorly documented and buggy! Might be useful for some.

Place files in \InkscapeExtension in \Inkscape\share\extensions\ folder.

\digitizeFigure\ is a python library. Non-standard dependencies are:
shapely - To represent polygons of inkscape as geometries.
lxml - To efficiently go through xml structure of svg
descartes - For plotting of shapely geometries.