#!/usr/bin/env python

import inkex

class DefineFacies(inkex.Effect):
    """
    Inkscape extension to define properties of polygon representing a facies.
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
        self.OptionParser.add_option('-l', '--FaciesLabel', action = 'store',
          type = 'string', dest = 'FaciesLabel', default = '',
          help = 'Which facies is represented by your polygons?')
        self.OptionParser.add_option('-f', '--FaciesType', action = 'store',
          type = 'string', dest = 'FaciesType', default = '',
          help = 'What kind of facies is it?')
        self.OptionParser.add_option('-a', '--Notebook', action = 'store',
          type = 'string', dest = 'Notebook', default = '',
          help = 'Dummy')
    def effect(self):
        """
        Effect behaviour.
        Overrides base class' method and inserts custom attributes to selected line element
        """
        FaciesLabel = self.options.FaciesLabel
        FaciesType = self.options.FaciesType

        for id, node in self.selected.iteritems():
            #Check if the node is a path ( "svg:path" node in XML )
            if node.tag == inkex.addNS('path','svg'):
                polygon = node #TODO: This selection should be further tested
                polygon.set(inkex.addNS("Type","TimeAnalysis"), "Facies")
                polygon.set(inkex.addNS("FaciesLabel","TimeAnalysis"), FaciesLabel)
                polygon.set(inkex.addNS("FaciesType","TimeAnalysis"), FaciesType)
        
effect = DefineFacies()
effect.affect()
        