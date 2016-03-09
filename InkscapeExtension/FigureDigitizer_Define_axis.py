#!/usr/bin/env python

import inkex
import sys

class DefineAxis(inkex.Effect):
    """
    Inkscape extension to define properties of axis of a stratigraphic cross section.
    """
    def __init__(self):
        """
        Constructor.
        Defines the options of the script.
        """
        #Call the base class constructor
        inkex.Effect.__init__(self)
        
        #Define custom namespace
        inkex.NSS['TimeAnalysis'] = 'http://www.arcex.no/workpackage/basin-analysis/'
        
        #Define string options
        self.OptionParser.add_option('-t', '--AxisType', action = 'store',
        type = 'string', dest = 'AxisType', default = '',
        help = 'Which axis would you like to define?')
        self.OptionParser.add_option('-s', '--AxisScale', action = 'store',
        type = 'string', dest = 'AxisScale', default = '',
        help = 'Is the axis logaritmic or linear?')
        self.OptionParser.add_option('-d', '--AxisDescription', action = 'store',
        type = 'string', dest = 'AxisDescription', default = '',
        help = 'How would you the describe the axis?')
        self.OptionParser.add_option('-u', '--AxisUnit', action = 'store',
        type = 'string', dest = 'AxisUnit', default = '',
        help = 'What unit is represented by you axis?')
        self.OptionParser.add_option('-l', '--AxisLabel', action = 'store',
        type = 'string', dest = 'AxisLabel', default = '',
        help = 'What would you like to call your axis')
        self.OptionParser.add_option('-x', '--AxisMaxValue', action = 'store',
        type = 'string', dest = 'AxisMaxValue', default = '',
        help = 'What is the maximum value represented by you axis?')
        self.OptionParser.add_option('-i', '--AxisMinValue', action = 'store',
        type = 'string', dest = 'AxisMinValue', default = '',
        help = 'What is the minimum value represented by you axis?')
        self.OptionParser.add_option('-a', '--Notebook', action = 'store',
        type = 'string', dest = 'Notebook', default = '',
        help = 'What is the minimum value represented by you axis?')
    def effect(self):
        """
        Effect behaviour.
        Overrides base class' method and inserts custom attributes to selected line element
        """
        AxisType = self.options.AxisType
        AxisDescription = self.options.AxisDescription
        AxisUnit = self.options.AxisUnit
        AxisLabel = self.options.AxisLabel
        AxisMaxValue = self.options.AxisMaxValue
        AxisMinValue = self.options.AxisMinValue
        AxisScale = self.options.AxisScale
        
        
        for id, node in self.selected.iteritems():
            axis = node #TODO: This selection should be further tested
            axis.set(inkex.addNS("Type","TimeAnalysis"), "Axis")
            axis.set(inkex.addNS("AxisType","TimeAnalysis"), AxisType)
            axis.set(inkex.addNS("AxisDescription","TimeAnalysis"), AxisDescription)
            #TODO: The label should be unique.
            axis.set(inkex.addNS("AxisLabel","TimeAnalysis"), AxisLabel) 
            axis.set(inkex.addNS("AxisUnit","TimeAnalysis"), AxisUnit)
            axis.set(inkex.addNS("AxisMaxValue","TimeAnalysis"), AxisMaxValue)
            axis.set(inkex.addNS("AxisMinValue","TimeAnalysis"), AxisMinValue)
            axis.set(inkex.addNS("AxisScale","TimeAnalysis"), AxisScale)
            # sys.stderr.write("The max value of the axis is: " + str(axis.get(inkex.addNS("AxisMaxValue","TimeAnalysis"))))
		
effect = DefineAxis()
effect.affect()
		