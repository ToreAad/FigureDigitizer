# -*- coding: utf-8 -*-
from digitizeFigure.parsesvg import LoadCrossSection
from digitizeFigure.visualize import DrawModel

path = "./simpleTest.svg"
crossSection = LoadCrossSection(path)
DrawModel(crossSection)

print(crossSection.Facies)
print(crossSection.Surfaces)