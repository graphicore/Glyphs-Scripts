#MenuTitle: Sort Paths
# -*- coding: utf-8 -*-
__doc__="""
Sort Paths on all layers.

If Correct Path Correction broke it, this may be able to repair it again.
This seems pretty save to run. I.e. if you apply it to all glyphs and all
layers, it seems to not make things worse.

This also sorts by signature, the implication is that, if your contours have
wrong starting points between layers, the sort result may not be interpolation
compatible.

Current Best Practice: run after "Correct Path Direction all Layers"
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
    # by "sorting" the rotations of signature, we become independent from
    # the actual order of the points. It's irrelevant if we pick the biggest
    # signature or the smallest, it's only important that we pick always
    # the same signature. ALSO: some or all rotations may be identical.
    biggestSig = signature
    for i in range(1, len(signature)):
        testSig = signature[i:] + signature[0:i]
        if testSig > biggestSig:
            biggestSig = testSig
    signature = biggestSig

    return (
        0 - len(path) # most points
      , 0 - counts[CURVE] # most curve points
      , 0 - counts[LINE] # most line points
      , 0 - counts[OFFCURVE] # most off-curve points
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
