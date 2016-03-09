# -*- coding: utf-8 -*-
from digitizeFigure.parsesvg import LoadCrossSection
from digitizeFigure.visualize import DrawModel

path = "./simpleTest.svg"
crossSection = LoadCrossSection(path)
DrawModel(crossSection)

# To see what facies are stored:
print(crossSection.Facies)

# To see what surfaces are stored:
print(crossSection.Surfaces)
# This crossSection.Surfaces returns a dictionary with surface label as key and returns an object of "Surface"-class. 
# See surfaces.py to see how this class works. 
# Surface.Line returns a Linestring or multilinestring object.

# To store the coordinates in a surface as a list;
Coordinates = list(crossSection.Surfaces['Topography'].Line.coords)