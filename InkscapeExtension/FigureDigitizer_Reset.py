#!/usr/bin/env python

import inkex
import sys

class ResetDocument(inkex.Effect):
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
		self.OptionParser.add_option('-o', '--Notebook', action = 'store',
		  type = 'string', dest = 'Notebook', default = '',
		  help = 'Dummy')
	def effect(self):
		"""
		Effect behaviour.
		Overrides base class' method and inserts custom attributes to selected line element
		"""
		svg = self.document.getroot()
		
		for node in svg.iter(): 
		# TODO: All nodes in document
			#Check if the node is a path ( "svg:path" node in XML )
			sys.stderr.write(str(node)+"\n")
			for item in node.items():
				if inkex.NSS['TimeAnalysis'] in str(item[0]):
					# sys.stderr.write("\t" + str(item[0]))
					# sys.stderr.write("\t\t" + str("Found!")+"\n")
					del node.attrib[item[0]]

		
effect = ResetDocument()
effect.affect()