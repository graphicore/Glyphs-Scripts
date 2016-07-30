#MenuTitle: Correct Path Direction in all Layers
# -*- coding: utf-8 -*-
__doc__="""
Runs Correct Path Direction in all layers of selected glyphs.
"""

# It's quite ironic that we need boilerplate code to import boilerplate.py:
import sys, os
parentDir = os.path.abspath('..')
if parentDir not in sys.path:
	sys.path.insert(0, parentDir)
from boilerplate import wrapLayerProcessor, processAllLayersMain

@processAllLayersMain
@wrapLayerProcessor
def main( layer ):
	return layer.correctPathDirection()

if __name__ == '__main__':
    import GlyphsApp
    main(Glyphs)
