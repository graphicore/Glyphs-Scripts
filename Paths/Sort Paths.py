#MenuTitle: Sort Paths
# -*- coding: utf-8 -*-
__doc__="""
Sort Paths on all layers to make master compatible again
"""

# It's quite ironic that we need boilerplate code to import boilerplate.py:
import sys, os
parentDir = os.path.abspath('..')
if parentDir not in sys.path:
    sys.path.insert(0, parentDir)
from boilerplate import wrapLayerProcessor, processAllLayersMain


def magnitude(path):
    counts = {
        CURVE: 0
      , LINE: 0
      , OFFCURVE: 0
    }
    for n in path.nodes:
        counts[n.type] += 1;

    signature = tuple(len(s) for s in path.segments)

    return (
        0 - len(path) # most points
      , 0 - counts[CURVE] # most curve points
      , 0 - counts[LINE] # most line poinst
      , 0 - counts[OFFCURVE] # most offcurve points
      , signature
      , path.direction
      , path.bounds.origin.x # left most
      , 0 - path.bounds.origin.y # top most
      , 0 - path.bounds.size.width # widest
      , 0 - path.bounds.size.height # highest
    )

@processAllLayersMain
@wrapLayerProcessor
def main( layer ):
    layer.paths = sorted(layer.paths, key=magnitude)

if __name__ == '__main__':
    import GlyphsApp
    main(Glyphs)
