#MenuTitle: FIX bot anchors
# -*- coding: utf-8 -*-
__doc__="""
if there is a "bot" anchor delete "bottom" anchor and name "bot" anchor "bottom"


"""

from itertools import cycle
import math, cmath

def renameAnchors(layer, old, new):
    keys = [ a.name for a in layer.anchors]
    if old not in keys:
        return
    if new in keys:
        del layer.anchors[new]
    layer.anchors[new] = layer.anchors[old]
    del layer.anchors[old]

@processAllLayersMain
@wrapLayerProcessor
def main( layer ):
    renameAnchors(layer, 'bot', 'bottom')
    renameAnchors(layer, '_bot', '_bottom')

if __name__ == '__main__':
    import GlyphsApp
    main(Glyphs)
