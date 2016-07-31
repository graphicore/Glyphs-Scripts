#MenuTitle: Delete Stray Points in all Layers
# -*- coding: utf-8 -*-
__doc__="""
Delete stray nodes in all layers of selected glyphs.
"""

# It's quite ironic that we need boilerplate code to import boilerplate.py:
import sys, os
parentDir = os.path.abspath('..')
if parentDir not in sys.path:
    sys.path.insert(0, parentDir)
from boilerplate import wrapLayerProcessor, processAllLayersMain


# taken from @mekkablue
# https://github.com/mekkablue/Glyphs-Scripts/blob/master/Paths/Delete%20Stray%20Points.py
def process( thisLayer ):
    strayPoints = 0
    for i in range(len(thisLayer.paths))[::-1]:
        thisPath = thisLayer.paths[i]
        if len(thisPath) == 1:
            thisLayer.removePathAtIndex_(i)
            strayPoints += 1
    return strayPoints

@processAllLayersMain
@wrapLayerProcessor
def main( layer ):
    deleted = process(layer)
    if(deleted):
        print 'Glyph', layer.parent.name, 'Layer', layer.name,'deleted' \
                , deleted, 'stray', 'points' if deleted > 1 else 'point'
        return layer.parent.name
    return None


if __name__ == '__main__':
    import GlyphsApp
    glyphs = set(main(Glyphs))
    glyphs.remove(None)
    glyphs = sorted(glyphs)
    if glyphs:
        print 'WARNING:\nStray nodes can be used as a hack to disable automatic alignment. It may be a good idea to check these glyphs for unwanted shifts, and undo if necessary:\n\n/%s\n' % '/'.join(glyphs)
        Glyphs.showMacroWindow()
