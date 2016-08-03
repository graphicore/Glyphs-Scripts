#MenuTitle: Set First Points
# -*- coding: utf-8 -*-
__doc__="""
Sort points and make the first point the first in the path.

If Correct Path Correction broke it, this may be able to repair it again.
Also, in some fringe cases this breaks interpolation, but, it never breaks
interpolation compatibility.

In cases where there is an ambiguity between compatible choices, this may
pick the wrong one, then the interpolation is twisted and scrambled.

This is NOT save to run on all glyphs. You'll have to check for interpolation
problems. But, it can greatly help in cases where starting points are
positioned badly to restore interpolation.


TODO:
If we run this and "Sort Paths" we could then do an inter layer analysis
on the ambiguous paths and come up with ways to make them compatible.
Shouldn't be that hard then. This assumes that we have fully compatible
layers.


"""

from itertools import cycle
import math, cmath

# It's quite ironic that we need boilerplate code to import boilerplate.py:
import sys, os
parentDir = os.path.abspath('..')
if parentDir not in sys.path:
    sys.path.insert(0, parentDir)
from boilerplate import wrapLayerProcessor, processAllLayersMain


class NodesInfo(object):
    def __init__(self, path):
        self.cycle = cycle(path.nodes)
        self._signatures = {}

    def getSignature(self, node):
        signature = self._signatures.get(node, None)
        if signature is None:
            signature = self._getSignature(node)
            self._signatures[node] = signature
        return signature

    def _getSignature(self, node):
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
        for current in self.cycle:
            if not signature:
                if current is not node:
                    continue
                # start at node
            elif current is node:
                # stop when node is there the second time
                break
            signature.append(types[current.type])
        return tuple(signature)

def unifyStartPoint(path):
    nodesInfo = NodesInfo(path)
    nodes = allNodes = sorted([n for n in path.nodes if n.type != OFFCURVE] \
                                            , key=nodesInfo.getSignature)
    if not nodes:
        return True

    # check if there is an unambiguous node:
    # remember, nodes is sorted by signature, so we will get the same
    # signatures subsequently
    countSignatures = {}
    currentSignature = nodesInfo.getSignature(nodes[0])
    currentNode = nodes[0]
    count = 0
    for node in nodes[1:]:
        signature = nodesInfo.getSignature(node)
        if signature == currentSignature:
            count += 1
        elif count == 0:
            found = True
            break
        else:
            count = 0
            currentSignature = signature
            currentNode = node
    if count == 0:
        # first unambiguous choice
        currentNode.makeNodeFirst()
        return True

    # So far all attempts I made in choosing from ambiguous nodes where
    # prone to errors in relation to the other paths. But, with compatible
    # paths, we'll pick nodes in a way that they will interpolate.
    # Could be scrambled, though.

    # get the least ambiguous signature first
    signatureNodes = {}
    # cluster by signature
    for node in nodes:
        signature = nodesInfo.getSignature(node)
        if signature not in signatureNodes:
            signatureNodes[signature] = []
        signatureNodes[signature].append(node)

    nodes = sorted(signatureNodes.values(), \
            key=lambda nodes: (len(nodes), nodesInfo.getSignature(nodes[0])))
    # This may have only two nodes, but it may also have all the
    # non-off-curve points of the path. Unfortunately, when sorting
    # by node position, it is not in all interpolation cases guaranteed
    # that the nodes meet their equivalent on the other layers.
    # if we would compare between the layers, we may find it easier to
    # make a good choice. Of course, we'd need to have some trust into the
    # path order of the other layer, and that is hard without having a
    # definite, correct point order ;-)
    nodes = nodes[0];

    # I tried *a lot* also much more complex key functions here and
    # the most stable I could come up with was rounded coordinates.
    # -y is a preference on having first nodes at the top.
    # Depending on the path, this may be a better or worse choice.
    nodes = sorted(nodes, key=lambda node: (-round(node.y), round(node.x)))
    nodes[0].makeNodeFirst()
    return False


@processAllLayersMain
@wrapLayerProcessor
def main( layer ):
    for i, path in enumerate(layer.paths):
        sucess = unifyStartPoint(path)
        if not sucess:
            print 'WARNING: The picked node was ambigous, please check', \
                    layer.parent.name, 'Layer', layer.name, 'Path:', i

if __name__ == '__main__':
    import GlyphsApp
    main(Glyphs)
