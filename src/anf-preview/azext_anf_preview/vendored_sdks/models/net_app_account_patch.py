# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class NetAppAccountPatch(Model):
    """NetApp account patch resource.

    :param tags: Resource tags
    :type tags: object
    """

    _attribute_map = {
        'tags': {'key': 'tags', 'type': 'object'},
    }

    def __init__(self, **kwargs):
        super(NetAppAccountPatch, self).__init__(**kwargs)
        self.tags = kwargs.get('tags', None)
