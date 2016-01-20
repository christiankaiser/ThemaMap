# -*- coding: utf-8 -*-
"""
ThemaMap
"""

from qgis.core import *
from qgis import utils
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from styles import *
from propsymbol import PropSymbolMarker

class ThemaMapRenderer(QgsFeatureRendererV2):
    rendererName = "ThemaMapRenderer"
    
    def __init__(self):
        #print "ThemaMapRenderer.__init__"
        #print str(self)
        QgsFeatureRendererV2.__init__(self, ThemaMapRenderer.rendererName)
        self.propsymbol = ProportionalSymbolStyle(attr=None, calib_value=10, calib_size=1)
        self.choropleth = ChoroplethStyle(
            attr=None, limits=[25,50,75], 
            colors='blues4'
        )
        # setup the marker symbol
        self.symbol = QgsMarkerSymbolV2()
        while self.symbol.symbolLayerCount(): self.symbol.deleteSymbolLayer(0)
        self.symbol.appendSymbolLayer(PropSymbolMarker())
    
    def save(self, doc):
        print "ThemaMapRenderer.save"
        return doc
    
    def reload(self, element):
        print "ThemaMapRenderer.reload"
        pass
    
    def startRender(self, context, layer):
        #print "ThemaMapRenderer.startRender"
        #print str(self.propsymbol)
        self.symbol.startRender(context)
    
    def stopRender(self, context):
        #print "ThemaMapRenderer.stopRender"
        self.symbol.stopRender(context)
    
    def usedAttributes(self):
        #print "ThemaMapRenderer.usedAttributes"
        attrs = []
        if self.propsymbol.attr: attrs.append(self.propsymbol.attr)
        if self.choropleth.attr: attrs.append(self.choropleth.attr)
        self.usedAttrs = attrs
        return attrs
    
    def symbolForFeature(self, feature):
        #print "ThemaMapRenderer.symbolForFeature"
        # Calculate the value based on calibration value, size, and bias
        try:
            attrs = feature.attributeMap()
            propval = attrs[self.usedAttrs.index(self.propsymbol.attr)].toDouble()[0]
            s = self.propsymbol.sizeForValue(propval)
        except:
            s = 0
        self.symbol.symbolLayer(0).size = s
        self.symbol.symbolLayer(0).stroke = self.propsymbol.style.stroke
        self.symbol.symbolLayer(0).fill = self.propsymbol.style.fill
        self.symbol.symbolLayer(0).strokeWidth = self.propsymbol.style.strokeWidth
        self.symbol.symbolLayer(0).symbol = self.propsymbol.symbol
        return self.symbol
    
    def clone(self):
        print "ThemaMapRenderer.clone"
        print str(self)
        cl = ThemaMapRenderer()
        cl.propsymbol = self.propsymbol.clone()
        cl.choropleth = self.choropleth.clone()
        return cl
