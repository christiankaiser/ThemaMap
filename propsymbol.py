

from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class PropSymbolMarker(QgsMarkerSymbolLayerV2):
    
    symbolLayerName = "PropSymbolMarker"
    
    def __init__(self):
        print "PropSymbolMarker.__init__"
        QgsMarkerSymbolLayerV2.__init__(self)
        self.size = 10
        self.stroke = QColor(0, 0, 0)
        self.fill = QColor(255, 0, 0)
        self.strokeWidth = 0.4
        self.symbol = 'square'
    
    def layerType(self):
        return self.symbolLayerName
    
    def properties(self):
        print "PropSymbolMarker.properties"
        return {
            'size': str(self.size),
            'stroke': self.stroke,
            'fill': self.fill,
            'strokeWidth': str(self.strokeWidth),
            'symbol': self.symbol,
        }
    
    def startRender(self, context):
        #print "PropSymbolMarker.startRender"
        pass
    
    def stopRender(self, context):
        #print "PropSymbolMarker.stopRender"
        pass
    
    def renderPoint(self, point, context):
        #print "PropSymbolMarker.renderPoint"
        #print "   [size=%i, stroke=[%i,%i,%i], fill=[%i,%i,%i], strokeWidth=%f, symbol=%s]" % (
        #    self.size, self.stroke.red(), self.stroke.green(), self.stroke.blue(),
        #    self.fill.red(), self.fill.green(), self.fill.blue(), self.strokeWidth,
        #    self.symbol
        #)
        if self.size <= 0: return
        if self.symbol == 'square': return self.renderSquare(point, context)
        if self.symbol == 'circle': return self.renderCircle(point, context)
    
    def setupRenderContext(self, context):
        p = context.renderContext().painter()
        # fill color
        if self.fill:
            c = context.selectionColor() if context.selected() else self.fill
            p.setBrush(QBrush(self.fill))
        # stroke
        if self.stroke:
            c = context.selectionColor() if context.selected() else self.stroke
            pen = QPen()
            pen.setWidth(self.strokeWidth)
            pen.setBrush(self.stroke)
            p.setPen(pen)
        return p
        
    def renderSquare(self, point, context):
        p = self.setupRenderContext(context)
        if self.fill or self.stroke:
            p.drawRect(
                point.x() - (self.size / 2.), point.y() - (self.size / 2.), 
                self.size, self.size
            )
    
    def renderCircle(self, point, context):
        p = self.setupRenderContext(context)
        if self.fill or self.stroke:
            p.drawEllipse(
                point.x() - (self.size / 2.), point.y() - (self.size / 2.), 
                self.size, self.size
            )
    
    def clone(self):
        print "PropSymbolMarker.clone"
        cl = PropSymbolMarker()
        cl.size = self.size
        cl.stroke = self.stroke
        cl.fill = self.fill
        cl.strokeWidth = self.strokeWidth
        cl.symbol = self.symbol
        return cl


