# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ThemaMap
                                 A QGIS plugin
 A renderer for thematic maps, especially proportional symbols
                             -------------------
        begin                : 2016-01-19
        copyright            : (C) 2016 by Christian Kaiser
        email                : christian.kaiser@unil.ch
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ThemaMap class from file ThemaMap.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .thema_map import ThemaMap
    return ThemaMap(iface)
