#!/usr/bin/env python

import inkex
import uuid

class DefineSurface(inkex.Effect):
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
		
		#Generate unique ID for surfaces
		UniqueSurfaceLabel = str(uuid.uuid1())
		
		#Define string options
		self.OptionParser.add_option('-l', '--SurfaceLabel', action = 'store',
		  type = 'string', dest = 'SurfaceLabel', default = UniqueSurfaceLabel,
		  help = 'Which facies is represented by your polygons?')
		self.OptionParser.add_option('-t', '--SurfaceType', action = 'store',
		  type = 'string', dest = 'SurfaceType', default = '',
		  help = 'Which surface is represented by your polyline?')		 
		self.OptionParser.add_option('-o', '--Notebook', action = 'store',
		  type = 'string', dest = 'Notebook', default = '',
		  help = 'Dummy')
	def effect(self):
		"""
		Effect behaviour.
		Overrides base class' method and inserts custom attributes to selected line element
		"""
		#TODO: Should test that label is unique.
		SurfaceLabel = self.options.SurfaceLabel
		SurfaceType = self.options.SurfaceType

		for id, node in self.selected.iteritems():
			#Check if the node is a path ( "svg:path" node in XML )
			if node.tag == inkex.addNS('path','svg'):
				surface = node #TODO: This selection should be further tested
				surface.set(inkex.addNS("Type","TimeAnalysis"), "Surface")
				surface.set(inkex.addNS("SurfaceLabel","TimeAnalysis"), SurfaceLabel)
				surface.set(inkex.addNS("SurfaceType","TimeAnalysis"), SurfaceType)
		
effect = DefineSurface()
effect.affect()