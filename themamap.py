# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ThemaMap
                                 A QGIS plugin
 A renderer for thematic maps, especially proportional symbols
                              -------------------
        begin                : 2016-01-19
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Christian Kaiser
        email                : christian.kaiser@unil.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
#from themamap_dialog import ThemaMapDialog
from .themamap_renderer_metadata import ThemaMapRendererMetadata
from .themamap_renderer import ThemaMapRenderer
from .themamap_controller import ThemaMapController
import os.path


class ThemaMap:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        print 'ThemaMap.__init__'
        self.iface = iface
        ThemaMapRenderer.iface = iface
        ThemaMapRenderer.plugin = self
        self.plugin_dir = os.path.dirname(__file__)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        print 'ThemaMap.initGui'
        self.metadata = ThemaMapRendererMetadata()
        QgsRendererV2Registry.instance().addRenderer(self.metadata)
        self.controller = ThemaMapController(self.iface)


    def unload(self):
        print 'ThemaMap.unload'
        self.controller.unload()
    
    
    def canBeUninstalled(self):
        print 'ThemaMap.canBeUninstalled'
        return self.controller.canBeUninstalled()

    def run(self):
        print 'ThemaMap.run'
        pass

