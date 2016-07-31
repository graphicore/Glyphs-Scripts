#MenuTitle: Set First Points
# -*- coding: utf-8 -*-
__doc__="""
Sort points and make the first point the first in the path.
"""

from itertools import cycle
from functools import partial
import math, cmath

# It's quite ironic that we need boilerplate code to import boilerplate.py:
import sys, os
parentDir = os.path.abspath('..')
if parentDir not in sys.path:
    sys.path.insert(0, parentDir)
from boilerplate import wrapLayerProcessor, processAllLayersMain


def getSignature(nodesCycle, node):
    """ Signature is relative to the node, so it stays the same, no matter
    what the start point of the contour is
    we take this as an arbitrary sort factor
    """
    types = {
        CURVE: 0
      , LINE: 1
      , OFFCURVE: 2
    }
    signature = []
    for current in nodesCycle:
        if not signature:
            if current is not node:
                continue
            # start at node
        elif current is node:
            # stop when node is there the second time
            break
        signature.append(types[current.type])
    return tuple(signature)

def getRelativeChange(nodesCycle, node):
    last = complex(node.x, node.y);
    changes = []
    for current in nodesCycle:
        if not changes:
            if current is not node:
                continue
            # start at node
        elif current is node:
            # stop when node is there the second time
            break
        currentVector = complex(current.x, current.y) - last;
        changes.append( ( abs(currentVector), cmath.phase(currentVector) ) )
        last = currentVector;
    return changes;

def getQuadrants(bounds, node, p=False):
    quadrants = []
    vector = complex(node.x, node.y)
    size = complex(bounds.size.width, bounds.size.height)
    center = complex(bounds.origin.x, bounds.origin.y)
    quaterCircle = cmath.pi * 0.5
    fullCircle = 2 * cmath.pi
    # quadrant:
    # 1|0
    # ---
    # 2|3
    ql = (
        (0, 3)
      , (1, 2)

    )

    if p:
        print 'initial center', center, 'first center:', center + size
        print 'size', size, abs(size), cmath.phase(size)
        print 'vector', vector

    quadrant = 0
    for frac in range(10): # 1/1 1/2 1/3 1/4
        size = complex(size.real * .5, size.imag * .5)
        offset = size = complex(
            size.real * (1 if quadrant in (0, 3) else -1)
          , size.imag * (1 if quadrant in (0, 1) else -1)
        )

        center += offset


        posToCenter = vector - center;
        if p:
            print  'offset', offset, abs(offset), cmath.phase(offset)
            print 'center', center
            print quadrant, 'postocenter', posToCenter, cmath.phase(posToCenter)
            a  = (cmath.phase(posToCenter) + fullCircle) % fullCircle
            b = a / quaterCircle
            c = round(b)
            d = int(c)
            print a, b, c, d
        quadrant = ql[0 if posToCenter.real >= 0 else 1][0 if posToCenter.imag >= 0 else 1]
        if p:
            print 'quadrant', quadrant
        quadrants.append(quadrant);
    return tuple(quadrants)


def nodeSortKey (bounds, nodesCycle, node):
    """ Note: when the signature is identical for different nodes, it is
    very hard to find a meaningful order. If we don't find it the interpolation
    is broken. even worse, it will look OK for glyphs, there will be no
    warning!

    What we do for now is printing a message that there are ambigous options
    for first points.
    """
    signature = getSignature(nodesCycle, node)
    # relativeChange = getRelativeChange(nodesCycle, node)
    vector = complex(node.y, node.x)

    quadrants = getQuadrants(bounds, node)

    return (signature, quadrants, abs(vector), cmath.phase(vector), node.x, node.y)



def unifyStartPoint(path):
    nodesCycle = cycle(path.nodes)
    sortKeyFunc = partial(nodeSortKey, path.bounds, nodesCycle)
    nodes = sorted([n for n in path.nodes if n.type != OFFCURVE], key=sortKeyFunc)

    #for i, node in enumerate(nodes):
    #    print i, '######\n', getRelativeChange(nodesCycle, node)

    if len(path.nodes) <= 14:
        node = nodes[0]
        print node.x, node.y, path.bounds
        print getQuadrants(path.bounds, nodes[0], True)

    if nodes:
        nodes[0].makeNodeFirst()
        if len(nodes) > 1 and getSignature(nodesCycle, nodes[0]) == getSignature(nodesCycle, nodes[0]):
            return True
    return False


@processAllLayersMain
@wrapLayerProcessor
def main( layer ):
    print layer.name, '\n____________________'
    for i, path in enumerate(layer.paths):
        ambigous = unifyStartPoint(path)
        if ambigous:
            print 'WARNING: Ambigous first node. Please check:', layer.parent.name, 'Layer', layer.name, 'Path:', i

if __name__ == '__main__':
    import GlyphsApp
    main(Glyphs)
