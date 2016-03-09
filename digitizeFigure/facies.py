# -*- coding: utf-8 -*-
from shapely.geometry import Polygon

class Facies(object):
    """
    This might be better represented as a dictionary
    TODO:
    """
    def __init__(self,FacDi):
        self.FacDi = FacDi
        # The naming of these are illogical, but I don't know what changing them will do.
        self.Label = self.FacDi["FaciesType"]
        self.Name = self.FacDi["Label"] 
        self.Polygon = self.GetGeometri()
        # Color information should be extracted by parseSVG
        self.Color = 'gray'
        
        
    def __repr__(self):
        return "{} - Facies".format(self.Label)
            
            
    def __str__(self):
        return "{} - Facies".format(self.Label)
    
    
    def GetGeometri(self):
        """Get geometrical representation of facies.
    
        """
        ext = self.FacDi["XYcoo"][0]
        if len(self.FacDi["XYcoo"]) > 1:
            inte = self.FacDi["XYcoo"][1:]
            polygon = Polygon(ext, inte)
        elif len(self.FacDi["XYcoo"]) == 1:
            polygon = Polygon(ext)
        return polygon
    
    
    def addAttribute(self):
        """
        Not Implemented
        """
        pass
    

