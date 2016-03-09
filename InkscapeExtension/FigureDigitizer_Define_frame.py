#!/usr/bin/env python

import inkex

class DefineFrame(inkex.Effect):
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
		self.OptionParser.add_option('-a', '--Notebook', action = 'store',
		  type = 'string', dest = 'Notebook', default = '',
		  help = 'Dummy')
	def effect(self):
		"""
		Effect behaviour.
		Overrides base class' method and inserts custom attributes to selected line element
		"""
		for id, node in self.selected.iteritems():
			node.set(inkex.addNS("Type","TimeAnalysis"), "Frame")
		
effect = DefineFrame()
effect.affect()