# -*- coding: utf-8 -*-
"""
ThemaMap
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from themamap_renderer import ThemaMapRenderer

class ThemaMapController:
    def __init__(self, iface):
        self.iface = iface
        QObject.connect(
            self.iface, SIGNAL('currentLayerChanged(QgsMapLayer*)'),
            self.activeLayerChanged
        )
        QObject.connect(
            self.iface.mainWindow(), SIGNAL('projectRead()'), 
            self.loadProject
        )
        QObject.connect(
            self.iface.mapCanvas(), SIGNAL('renderComplete(QPainter*)'),
            self.renderComplete
        )
        QObject.connect(
            self.iface.mapCanvas(), SIGNAL('renderStarting()'),
            self.renderStarting
        )
    
    def unload(self):
        QObject.disconnect(
            self.iface, SIGNAL('currentLayerChanged(QgsMapLayer*)'),
            self.activeLayerChanged
        )
        QObject.disconnect(
            self.iface.mainWindow(), SIGNAL('projectRead()'), 
            self.loadProject
        )
        QObject.disconnect(
            self.iface.mapCanvas(), SIGNAL('renderComplete(QPainter*)'),
            self.renderComplete
        )
        QObject.disconnect(
            self.iface.mapCanvas(), SIGNAL('renderStarting()'),
            self.renderStarting
        )
    
    def canBeUninstalled(self):
        return False
    
    def loadProject(self):
        pass
    
    def activeLayerChanged(self, layer):
        pass
    
    def renderStarting(self):
        pass
    
    def renderComplete(self, painter):
        pass
    
    def findRenderer(self):
        layer = self.iface.activeLayer()
        return layer, self.findLayerRenderer(layer)
    
    def findLayerRenderer(self, layer):
        if not layer or layer.type() != QgsMapLayer.VectorLayer:
            return None
        renderer = layer.rendererV2()
        if not renderer or renderer.type() != ThemaMapRenderer.rendererName:
            return None
        return renderer
    
    def vectorRendererLayers(self):
        for l in self.iface.mapCanvas().layers():
            r = self.findLayerRenderer(l)
            if r:
                yield l,r
    