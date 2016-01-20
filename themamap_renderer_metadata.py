# -*- coding: utf-8 -*-
"""
ThemaMap
"""

from qgis.core import QgsRendererV2AbstractMetadata
from PyQt4.QtGui import *

from themamap_renderer import ThemaMapRenderer
from themamap_widget import ThemaMapWidget
import resources

class ThemaMapRendererMetadata(QgsRendererV2AbstractMetadata):
    def __init__(self):
        print "ThemaMapRendererMetadata.__init__"
        QgsRendererV2AbstractMetadata.__init__(
            self, ThemaMapRenderer.rendererName, "Thematic map",
            QIcon(QPixmap(':plugins/ThemaMap/icon.png', 'png'))
        )
    
    def createRenderer(self, element):
        print "ThemaMapRendererMetadata.createRenderer"
        tm_renderer = ThemaMapRenderer()
        if element: tm_renderer.reload(element)
        return tm_renderer
    
    def createRendererWidget(self, layer, style, renderer):
        print "ThemaMapRendererMetadata.createRendererWidget"
        print ThemaMapWidget
        return ThemaMapWidget(layer, style, renderer)

