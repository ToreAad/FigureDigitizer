# -*- coding: utf-8 -*-
from shapely.geometry import LineString, MultiLineString


class Surface(object):
    """
    A representation of a stratigraphic surface.
    """
    #Might want to have this inherit from line of shapely?
    def __init__(self, SurDi):
        self._SurDi = SurDi
        self.Line = self._GetGeometri()
        self.Label = self._SurDi["Label"]
        self.Type = self._SurDi["SurfaceType"]
        self.Color = 'black'
        
    
    def __repr__(self):
        return "{} (surface)".format(self.Label)
            
    
    def __str__(self):
        return str(self.Label)
            
            
    def _GetGeometri(self):
        """
        use dictionary from model as input, Get geometrical representation
        of surface.
        """
        if len(self._SurDi["XYcoo"]) > 1:
            Line = MultiLineString(self._SurDi["XYcoo"])
        elif len(self._SurDi["XYcoo"]) == 1:
            Line = LineString(self._SurDi["XYcoo"][0])
        return Line
        
    
    def addAttribute(self):
        """
        Not Implemented
        """
        pass
    