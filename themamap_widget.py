# -*- coding: utf-8 -*-
"""
ThemaMap
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from .themamap_renderer import ThemaMapRenderer
from .themamap_utils import layer_attributes
from .ui_themamap import Ui_ThemaMapWidget
from .colortables import colortables as ct

import resources


# ColorButton class from VectorFieldRenderer plugin
# http://plugins.qgis.org/plugins/VectorFieldRenderer/
# https://github.com/ccrook/QGIS-VectorFieldRenderer-Plugin
class ColorButton( QObject ):

   def __init__(self, button):
      QObject.__init__(self)
      self.button = button
      button.clicked.connect(self.clicked)

   def color(self):
      return self.button.color()

   def setColor(self, color):
      if color.isValid():
         self.button.setColor(color)

   def clicked(self):
      self.setColor(QColorDialog.getColor(self.color()))


def string2list(s):
    s = s.replace('/',' ')
    s = s.replace(';',' ')
    s = s.replace(',',' ')
    s = s.replace('  ', ' ')
    l = []
    for el in s.split(' '):
        if len(el) > 0: l.append(el)
    return l


class ThemaMapWidget(QgsRendererV2Widget, Ui_ThemaMapWidget):
    
    choroplethSchemeTypes = ['sequential', 'divergent', 'qualitative']
    
    def __init__(self, layer, style, renderer):
        print "ThemaMapWidget.__init__"
        QgsRendererV2Widget.__init__(self, layer, style)
        if renderer is None or renderer.type() != ThemaMapRenderer.rendererName:
            self.r = ThemaMapRenderer()
        else:
            self.r = renderer
        self.valid = True       # can the layer be rendered?
        self.layer = layer
        self.setupUi(self)
        self.buildWidget()
        self.loadUi()
    
    def renderer(self):
        print "ThemaMapWidget.renderer"
        if self.valid: self.applyUi()
        return self.r
    
    def buildWidget(self):
        print "ThemaMapWidget.buildWidget"
        self.symbolStyleFillColor = ColorButton(self.uSymbolStyleFillColor)
        self.symbolStyleStrokeColor = ColorButton(self.uSymbolStyleStrokeColor)
        self.choroplethFillColor = ColorButton(self.uChoroplethFillColor)
        self.choroplethStrokeColor = ColorButton(self.uChoroplethStrokeColor)
    
    def loadUi(self):
        """
        Fills the UI using the values in the renderer.
        """
        print "ThemaMapWidget.loadUi"
        # prop symbol tab
        self.uPropSymbAttrMenu.clear()
        self.uPropSymbAttrMenu.addItem('<none>')
        for attr in layer_attributes(self.layer):
            self.uPropSymbAttrMenu.addItem(attr)
            if attr == self.r.propsymbol.attr:
                self.uPropSymbAttrMenu.setCurrentIndex(self.uPropSymbAttrMenu.count()-1)
        self.uCalibrationSize.setText(str(self.r.propsymbol.calib_size))
        self.uCalibrationValue.setText(str(self.r.propsymbol.calib_value))
        self.uBias.setText(str(self.r.propsymbol.bias))
        if self.r.propsymbol.symbol == 'circle':
            self.uSymbolShapeSquare.setChecked(False)
            self.uSymbolShapeCircle.setChecked(True)
        else:
            self.uSymbolShapeSquare.setChecked(True)
            self.uSymbolShapeCircle.setChecked(False)
        self.uSymbolFlannery.setChecked(self.r.propsymbol.flannery)
        self.uSymbolStyleFillColor.setColor(self.r.propsymbol.style.fillColor())
        self.uSymbolStyleStrokeColor.setColor(self.r.propsymbol.style.strokeColor())
        self.uSymbolStyleStrokeWidth.setDecimals(2)
        self.uSymbolStyleStrokeWidth.setMinimum(0.0)
        self.uSymbolStyleStrokeWidth.setSingleStep(0.1)
        self.uSymbolStyleStrokeWidth.setValue(self.r.propsymbol.style.strokeWidth)
        # choropleth tab
        self.uChoroplethAttr.clear()
        self.uChoroplethAttr.addItem('<none>')
        for attr in layer_attributes(self.layer):
            self.uChoroplethAttr.addItem(attr)
        self.uChoroplethNClasses.setMinimum(3)
        self.uChoroplethNClasses.setMaximum(12)
        self.uChoroplethNClasses.setValue(len(self.r.choropleth.colors))
        self.uChoroplethSchemeType.setCurrentIndex(
            max(0, self.choroplethSchemeTypes.index(self.r.choropleth.type))
        )
        self.updateChoroplethScheme()
        self.uChoroplethLimits.setText(' '.join(map(str, self.r.choropleth.limits)))
        self.uChoroplethCriticalValue.setText(str(self.r.choropleth.critical_value))
        self.uChoroplethNoData.setText(str(self.r.choropleth.nodata_value))
        self.uChoroplethFillColor.setColor(self.r.choropleth.style.fillColor())
        self.uChoroplethStrokeColor.setColor(self.r.choropleth.style.strokeColor())
        self.uChoroplethStrokeWidth.setValue(self.r.choropleth.style.strokeWidth)
        self.updateUiElements()
    
    def applyUi(self):
        """
        Applies the values in the UI to the renderer.
        """
        print "ThemaMapWidget.applyUi"
        print str(self.r)
        # prop symbol tab
        self.r.propsymbol.attr = str(self.uPropSymbAttrMenu.currentText())
        if self.r.propsymbol.attr == '<none>': self.r.propsymbol.attr = None
        self.r.propsymbol.calib_size = str(self.uCalibrationSize.text())
        self.r.propsymbol.calib_value = str(self.uCalibrationValue.text())
        self.r.propsymbol.bias = str(self.uBias.text())
        if self.uSymbolShapeSquare.isChecked():
            self.r.propsymbol.symbol = 'square'
        else:
            self.r.propsymbol.symbol = 'circle'
        self.r.propsymbol.flannery = self.uSymbolFlannery.isChecked()
        self.r.propsymbol.style.fillColor(self.uSymbolStyleFillColor.color())
        self.r.propsymbol.style.strokeColor(self.uSymbolStyleStrokeColor.color())
        self.r.propsymbol.style.strokeWidth = self.uSymbolStyleStrokeWidth.value()
        # choropleth tab
        self.r.choropleth.attr = str(self.uChoroplethAttr.currentText())
        if self.r.choropleth.attr == '<none>': self.r.choropleth.attr = None
        self.r.choropleth.type = str(self.uChoroplethSchemeType.currentText()).lower()
        # colors are missing here
        self.r.choropleth.limits = string2list(str(self.uChoroplethLimits.text()))
        self.r.choropleth.critical_value = str(self.uChoroplethCriticalValue.text())
        self.r.choropleth.nodata_value = str(self.uChoroplethNoData.text())
        self.r.choropleth.style.fillColor(self.uChoroplethFillColor.color())
        self.r.choropleth.style.strokeColor(self.uChoroplethStrokeColor.color())
        self.r.choropleth.style.strokeWidth = self.uChoroplethStrokeWidth.value()
    
    def updateUiElements(self):
        print "ThemaMapWidget.updateUiElements"
        pass
    
    def updateChoroplethScheme(self):
        print "ThemaMapWidget.updateChoroplethScheme"
        schemetype = self.r.choropleth.type.lower()[0:3]
        nclasses = len(self.r.choropleth.colors)
        # remove all current color tables
        while self.uChoroplethScheme.count() > 0:
            self.uChoroplethScheme.removeItem(0)
        for k in ct:    # loop over all available color tables
            # create the color scheme icon
            ncols = len(ct[k]['colors'])
            # Impossible to create icons on the fly for some unknown 
            # reason. We generate images and load them through the 
            # Qt resources file.
            #img = QImage(12*ncols, 24, QImage.Format_RGB32)
            #p = QPainter()
            #p.begin(img)
            #for i in range(ncols):
            #    c = ct[k]['colors'][i]
            #    p.fillRect(i*12, 0, 12, 24, QColor(c[0], c[1], c[2]))
            #p.end()
            #img.save('/home/ck/src/qgis-themamap/ThemaMap/colortables_icons/'+k+'.png')
            if ncols == nclasses and ct[k]['type'].lower()[0:3] == schemetype:
                ico = QIcon(QPixmap(':plugins/ThemaMap/'+k+'.png', 'png'))
                self.uChoroplethScheme.addItem(ico, ct[k]['name'])




