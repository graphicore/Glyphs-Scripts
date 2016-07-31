# -*- coding: utf-8 -*-

from functools import wraps

def wrapLayerProcessor(func):
	@wraps(func)
	def wrapper(layer, *args, **kwds):
		glyph = layer.parent
		glyph.beginUndo() # begin undo grouping
		try:
			return func(layer, *args, **kwds)
		finally:
			glyph.endUndo()   # end undo grouping
	return wrapper

def getAllLayers(font, selected=True):
	if selected:
		glyphs = [l.parent for l in font.selectedLayers]
	else:
		glyphs = font.glyphs

	allLayers = []
	for glyph in glyphs:
		allLayers += glyph.layers

	return allLayers

def wrapMain(func):
	@wraps(func)
	def wrapper(Glyphs, *args, **kwds):
		font = Glyphs.font; # frontmost font
		font.disableUpdateInterface() # suppresses UI updates in Font View
		try:
			return func(font, *args, **kwds)
		finally:
			font.enableUpdateInterface() # re-enables UI updates in Font View
	return wrapper


def processAllLayersMain(process,  selected=True, *args, **kwds):
	@wraps(process)
	@wrapMain
	def main(font, *args, **kwds):
		allLayers = getAllLayers(font, selected=selected);
		results = []
		for layer in allLayers:
			results.append(process(layer, *args, **kwds))
		return results
	return main

