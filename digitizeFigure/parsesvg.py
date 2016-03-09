# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 14:10:06 2015

@author: taa009
"""
import re
import collections
from lxml import etree
from inkexlib import inkex
import numpy as np

from digitizeFigure.surfaces import Surface
from digitizeFigure.facies import Facies

X = 0
Y = 1

#Define custom namespace
inkex.NSS['TimeAnalysis'] = 'http://www.arcex.no/workpackage/basin-analysis/'

class LoadSVG(object):
    """
    """
    def __init__(self, path):
#        self.path = path        
        self.svg = etree.parse(path).getroot()
        self.Xaxis, self.Yaxis = self._GetAxis()
     
     
    def _GetAxis(self):
        """
        goes through every node of SVG file, check if they represent the x
        or y axis. when found sends node to self.ParseAxis()
        returns two dictionaries: Xaxis, Yaxis
        """
        XaxisCounter = 0
        YaxisCounter = 0
        
        for node in self.svg.iter(): 
            if node.get(inkex.addNS("AxisType","TimeAnalysis")) == "Yaxis":
                Yaxis = self._ParseAxis(node)
                YaxisCounter += 1
            elif node.get(inkex.addNS("AxisType","TimeAnalysis")) == "Xaxis":
                Xaxis = self._ParseAxis(node)
                XaxisCounter += 1
                
        assert (XaxisCounter == 1 and YaxisCounter == 1), "Wrong number of X or Y axis in document"
        
        return Xaxis, Yaxis
        
        
    def _ParseAxis(self, node):
        """
        Input: A node representing a axis.
        Output: A dictionary with axis properties.
        """
        self.node = node
        d_strng = self.node.get("d")
        Points = self._ParseD(d_strng)[0]

        Axis = {}
        Axis["x1"] = float(Points[0][X])
        Axis["x2"] = float(Points[1][X])
        Axis["y1"] = float(Points[0][Y])
        Axis["y2"] = float(Points[1][Y])
        Axis["MaxValue"] = float(node.get(inkex.addNS("AxisMaxValue","TimeAnalysis")))
        Axis["MinValue"] = float(node.get(inkex.addNS("AxisMinValue","TimeAnalysis")))
        Axis["AxisDescription"] = node.get(inkex.addNS("AxisDescription","TimeAnalysis"))
        Axis["AxisLabel"] = node.get(inkex.addNS("AxisLabel","TimeAnalysis"))
        Axis["AxisScale"] = node.get(inkex.addNS("AxisScale","TimeAnalysis"))
        Axis["AxisUnit"] = node.get(inkex.addNS("AxisUnit","TimeAnalysis"))
        
        if node.get(inkex.addNS("AxisType","TimeAnalysis")) == "Xaxis": 
            A_x = [[1,Axis["x1"]],[1,Axis["x2"]]]
            B_x = [[Axis["MinValue"]],[Axis["MaxValue"]]]
            A_x_inv = np.linalg.inv(A_x)
            # Xreal = a + b*Xread
            Axis["ab"] = np.dot(A_x_inv, B_x)
            
        if node.get(inkex.addNS("AxisType","TimeAnalysis")) == "Yaxis":
            A_y = [[1,Axis["y1"]],[1,Axis["y2"]]]
            B_y = [[Axis["MinValue"]],[Axis["MaxValue"]]]
            A_y_inv = np.linalg.inv(A_y)
            # Yreal = a + b*Yread
            Axis["ab"] = np.dot(A_y_inv, B_y)
            
        return Axis
    
    
    def _ParseD(self, d_str):
        """
        takes a string with d attribute of path as input. Assumes that 
        nodes are represented by M, L, Z and z elements. Splits string
        according to these identifiers. Returns: [(x,y),...]
        
        make sure that you select all nodes in Inkscape and make them to
        edges.
        """
        #PATH_IDENTIFIERS = "ML"
        chars_to_remove = "z|Z"

        self.d_str = d_str
        self.d_str = re.sub(chars_to_remove, '', self.d_str)
        self.d_str = re.sub(" +", ' ', self.d_str).strip()
        
        ListOfPaths = list(filter(None, self.d_str.split("M")))       
        ListOfPoints = []     
        for path in ListOfPaths:
            Points = []
            StringsWCoordinates = path.split("L")
            for string in StringsWCoordinates:
                try:
                    x,y = re.split("," ,string)
                except ValueError:
                    print("!!! Tried to unpack: " + string + " !!!")
                    raise
                Points.append((float(x),float(y)))
            ListOfPoints.append(Points)            
        return ListOfPoints

            
    def _GetPoints(self, node):
        """ 
        This function takes a node representing a path as input and returns 
        the spatial coordinates of the nodes of the path 
        """
        ListofCoordinates = []
        d_str = node.get("d")
       
        assert ("C" not in d_str),"Error the node{} has C element in it. That means that not all of the points in a path was corners, but could be smooth bezier curves or something.".format(etree.tostring(node, method='html', pretty_print=True))
        
        ListOfPoints = self._ParseD(d_str)
        for points in ListOfPoints:
            ListofCoordinates.append(self._GetSpatialCoordinates(points))
    
        return ListofCoordinates    
        
        
    def _GetSpatialCoordinates(self, points):
        """ 
        input: [(x,y),...] of SVG coordinates.
        output: [(x,y),...] of spatial coordinates.
        
        This function takes a list of x and y coordinates representing SVG 
        coordinates of path and transforms it to the spatial coordinates
        implied by the axis of the model.
        """
        self.points = points
        xData = []
        yData = []

        for SVGcoordinate in points:
            x,y = SVGcoordinate
            xData.append([1,x])
            yData.append([1,y])
        xData = np.dot(xData, self.Xaxis["ab"])
        yData = np.dot(yData, self.Yaxis["ab"])
        Coordinates = np.column_stack((xData,yData)).tolist()
        Coordinates = [tuple(l) for l in Coordinates]
        return Coordinates
    
    def _GetFrame(self):
        """
        goes through SVG file to find node with frame attributes.
        define the min and max values represented by the frame.
        """
        for node in self.svg.iter(): 
            if node.get(inkex.addNS("Type","TimeAnalysis")) == "Frame":
                frame = node
        Coordinates = self._GetPoints(frame)[0]
#        print("Coordinates: ", Coordinates)
        Xvalues = []
        Yvalues = []
        for element in Coordinates:
            Xvalues.append(element[X])
            Yvalues.append(element[Y])
        xrange = (min(Xvalues),max(Xvalues))
        yrange = (min(Yvalues),max(Yvalues))
        return xrange,yrange



class LoadCrossSection(LoadSVG):
    """
     This class takes the path of an SVG file as input, reads it and parses 
     the required information to make a virtual representation of the 
     stratigraphic cross section
     """
    def __init__(self, path, vertical_resulution = 10.0, horisontal_resolution = 10.0, Label = ""):
                     
        assert (type(vertical_resulution) == float)
        assert (type(horisontal_resolution) == float)
        
        # Assign attributes associated with specific model
        self.path = path

        self.svg = etree.parse(self.path).getroot()
        self.Xaxis, self.Yaxis = self._GetAxis()
        
        # Get attributes relevant for the virtual representation of model
        self.xrange, self.yrange = self._GetFrame()
        self.Surfaces = self._GetSurfaces()
        self.Facies = self._GetFacies()
        self.VRES = vertical_resulution
        self.HRES = (max(self.xrange)-min(self.xrange))/horisontal_resolution
        self.Label = Label
        
        
    def _GetSurfaces(self):
        """ 
        goes through every node of SVG file, check if they have surface
        string in path attribute. sends node to self.ParseSurface()
        returns a list of parsed surfaces.
        """
        Surfaces = {}
        
        for node in self.svg.iter():         
            if node.get(inkex.addNS("Type","TimeAnalysis")) == "Surface":
                a_surface = self._ParseSurface(node)
                a_label = a_surface.Label
                Surfaces[a_label] = a_surface
        return Surfaces
        
    def _ParseSurface(self,node):
        """  
        Function that takes a node of lxml with surface data parses it
        and returns dictionary 
        """
        SurfaceDic = {}
        SurfaceDic["Label"] = node.get(inkex.addNS("Label","TimeAnalysis"))
        SurfaceDic["SurfaceType"] = node.get(inkex.addNS("SurfaceType","TimeAnalysis"))
        SurfaceDic["XYcoo"] = self._GetPoints(node)
        ParSurface = Surface(SurfaceDic)
        return ParSurface

        
        
    def _GetFacies(self):
        """
        goes through every node of SVG file, check if they have Facies
        string in path attribute. sends node to self.ParseFacies()
        returns a list of parsed surfaces.
        """
        FaciesDic = {}
        for node in self.svg.iter():
            if node.get(inkex.addNS("Type","TimeAnalysis")) == "Facies":
                Facies = self._ParseFacies(node)
                f_label = Facies.Label
                FaciesDic[f_label] = Facies
        return FaciesDic
        
        
    def _ParseFacies(self,node):
        """ 
        Function that takes a node of lxml with facies data parses it 
        as a dictionary and returns an object of the Facies class
        """
        FaciesDic = {}
        FaciesDic["Label"] = node.get(inkex.addNS("Label","TimeAnalysis"))
        FaciesDic["FaciesType"] = node.get(inkex.addNS("FaciesType","TimeAnalysis"))
        FaciesDic["XYcoo"] = self._GetPoints(node) 
        ParFacies = Facies(FaciesDic)
        return ParFacies


class LoadData(LoadSVG):
    """
    TODO:
    """
    def __init__(self, path):
#        self.path = path     
        self.svg = etree.parse(path).getroot()
        self.Xaxis, self.Yaxis = None, None
        self.Data = self._GetData()

    def _GetData(self):
        """ 
        goes through every node of SVG file, check if they have data
        string in path attribute. sends node to self.ParseData()
        returns a dictionary of parsed datasets.
        """
        DataList = []
        
        for node in self.svg.iter():         
            if node.get(inkex.addNS("Type","TimeAnalysis")) == "Data":
                RefXaxis = node.get(inkex.addNS("RefXaxis","TimeAnalysis"))
                RefYaxis = node.get(inkex.addNS("RefYaxis","TimeAnalysis"))
                assert (RefXaxis and RefYaxis), "Data not associated with axis"
                self.Xaxis, self.Yaxis = self._GetAxis(RefXaxis, RefYaxis)
                data = self._ParseData(node)
                self.Xaxis, self.Yaxis = None, None
                DataList.append(data)
        
        Set_of_labels = set([dic["Label"] for dic in DataList])
        
        result = {}
        for label in Set_of_labels:
            data_dictionary = collections.defaultdict(list)
            
            for dic in DataList:
                if dic["Label"] == label:
                    val = dic["DataValue"]
                    for xy in dic["xy"]:
                        data_dictionary[val].append(xy)
#                    data_dictionary["xaxis"] = dic["xaxis"]
#                    data_dictionary["yaxis"] = dic["yaxis"]
            result[label] = data_dictionary
                
        return result
    
    def _ParseData(self,node):
        """  
        Function that takes a node of lxml with surface data parses it
        and returns dictionary 
        """
        
        data = {}
        data["Label"] = node.get(inkex.addNS("Label","TimeAnalysis"))
        data["DataValue"] = node.get(inkex.addNS("DataValue","TimeAnalysis"))
        data["xy"] = self._GetPoints(node)
        data["DataMaxValue"] = node.get(inkex.addNS("DataMaxValue","TimeAnalysis"))
        data["DataMinValue"] = node.get(inkex.addNS("DataMinValue","TimeAnalysis"))
        data["xaxis"] = self.Xaxis
        data["yaxis"] = self.Yaxis

        return data
        
        
    def _GetAxis(self, RefXaxis, RefYaxis):
        """
        goes through every node of SVG file, check if they represent the x
        or y axis. when found sends node to self.ParseAxis()
        returns two dictionaries: Xaxis, Yaxis
        """

        for node in self.svg.iter(): 
            if node.get(inkex.addNS("Type","TimeAnalysis")) == "Axis":
                if node.get(inkex.addNS("AxisLabel","TimeAnalysis")) == RefYaxis:
                    Yaxis = self._ParseAxis(node)
                elif node.get(inkex.addNS("AxisLabel","TimeAnalysis")) == RefXaxis:
                    Xaxis = self._ParseAxis(node)
        
        return Xaxis, Yaxis
        
