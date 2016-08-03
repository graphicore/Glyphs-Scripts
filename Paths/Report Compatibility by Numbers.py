#MenuTitle: Report Compatibility by Numbers
# -*- coding: utf-8 -*-
__doc__="""
Outputs count of nodes, node types, paths, "segment signature", anchors

Inspired by Tosches scrip.
"""

# It's quite ironic that we need boilerplate code to import boilerplate.py:
import sys, os
import GlyphsApp

parentDir = os.path.abspath('..')
if parentDir not in sys.path:
	sys.path.insert(0, parentDir)
from boilerplate import wrapLayerProcessor, processAllLayersMain


class Counter(object):
    def __init__(self, name):
        self.name = name
        self.total = 0
        self.offcurve = 0
        self.curve = 0
        self.line = 0

    def count_node(self, node):
        self.total += 1
        if node.type == CURVE:
            self.curve += 1
        elif node.type == LINE:
            self.line += 1
        if node.type == OFFCURVE:
            self.offcurve += 1


@processAllLayersMain
@wrapLayerProcessor
def main( layer ):
    counters = []
    layerCounter = Counter('{0} Layer {1} Paths {2} Anchors {3} {4}'.format(
                                    layer.parent.name
                                  , layer.name
                                  , len(layer.paths)
                                  , len(layer.anchors)
                                  , ' '.join(layer.anchors.keys())
                        ))
    counters.append(layerCounter)
    for i, path in enumerate(layer.paths):
        signature = ['{0}'.format(len(s)) for s in path.segments]
        counter = Counter('Path {0} segment signature ({1})'.format(i, ' '.join(signature)))
        counters.append(counter)
        for node in path.nodes:
            counter.count_node(node)
            layerCounter.count_node(node)
    print ''
    for counter in counters:
        print counter.name
        print '    total: {0} curve: {1} line: {2} offcurve: {3}'.format(
                counter.total, counter.curve, counter.line, counter.offcurve)
        print ''

if __name__ == '__main__':
    import GlyphsApp
    main(Glyphs)
