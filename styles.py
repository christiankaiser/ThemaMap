# -*- coding: utf-8 -*-
"""
ThemaMap
"""

from PyQt4.QtGui import QColor      # super bad design, please hit me


class FillStyle:
    
    def __init__(self, fill=None, stroke=None, strokeWidth=0.3, opacity=1.):
        self.fill = fill or QColor(255, 0, 0)
        self.stroke = stroke or QColor(0, 0, 0)
        self.strokeWidth = strokeWidth
        self.opacity = opacity
    
    def __str__(self):
        return 'FillStyle[fill=[%i,%i,%i], stroke=[%i,%i,%i], strokeWidth=%f]' % (
            self.fill.red(), self.fill.green(), self.fill.blue(), 
            self.stroke.red(), self.stroke.green(), self.stroke.blue(), 
            self.strokeWidth
        )
    
    def clone(self):
        c = FillStyle(self.fill, self.stroke, self.strokeWidth, self.opacity)
        return c
    
    def fillColor(self, clr=None):
        """
        Returns the fill color as QColor if clr is None.
        If clr contains a QColor, it sets the color instead.
        """
        if clr is None: return self.fill
        self.fill = clr
    
    def strokeColor(self, clr=None):
        if clr is None: return self.stroke
        self.stroke = clr


class ProportionalSymbolStyle:
    
    def __init__(self, attr, calib_value, calib_size, bias=0):
        self.attr = attr
        self.calib_value = calib_value
        self.calib_size = calib_size
        self.bias = bias
        self.style = FillStyle()
        self.symbol = 'square'   # can also be 'circle'
        self.flannery = False    # Flannery appearance compensation for circles
    
    def __str__(self):
        return 'ProportionalSymbolStyle[attr=%s, calib_value=%s, calib_size=%s, bias=%s, style=%s, symbol=%s, flannery=%i]' % (
            self.attr, str(self.calib_value), str(self.calib_size), 
            str(self.bias), str(self.style), self.symbol, int(self.flannery)
        )
    
    def clone(self):
        c = ProportionalSymbolStyle(self.attr, self.calib_value, self.calib_size, self.bias)
        c.style = self.style.clone()
        c.symbol = self.symbol
        c.flannery = self.flannery
        return c
    
    def sizeForValue(self, value):
        v = float(value) + float(self.bias)
        if self.flannery and self.symbol == 'circle':   # flannery is only for circles
            s = 1.003 * (v / float(self.calib_value))**0.5716 * float(self.calib_size)
        else:
            s = (v / float(self.calib_value))**0.5 * float(self.calib_size)
        return s
    


class ChoroplethStyle:
    
    def __init__(self, attr, limits, colors):
        self.attr = attr
        self.limits = limits
        self.colors = colors
        self.type = 'sequential'       # can also be 'divergent' or 'qualitative'
        self.critical_value = None     # for divergent color scheme
        self.style = FillStyle()
        self.nodata_value = None
    
    def clone(self):
        c = ChoroplethStyle(self.attr, self.limits, self.colors)
        c.type = self.type
        c.critical_value = self.critical_value
        c.style = self.style.clone()
        c.nodata_value = self.nodata_value
        return c




