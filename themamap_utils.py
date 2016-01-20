# -*- coding: utf-8 -*-
"""
ThemaMap
"""


def layer_attributes(lyr):
    """
    Returns the names of the attributes of a provided vector layer.
    """
    provider = lyr.dataProvider()
    attrs = provider.fields()
    return [attr.name() for attr in attrs]

