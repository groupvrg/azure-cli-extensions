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


class PerformanceLevelCapability(Model):
    """The performance level capability.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar value: Performance level value.
    :vartype value: float
    :ivar unit: Unit type used to measure performance level. Possible values
     include: 'DTU', 'VCores'
    :vartype unit: str or ~azure.mgmt.sql.models.PerformanceLevelUnit
    """

    _validation = {
        'value': {'readonly': True},
        'unit': {'readonly': True},
    }

    _attribute_map = {
        'value': {'key': 'value', 'type': 'float'},
        'unit': {'key': 'unit', 'type': 'str'},
    }

    def __init__(self, **kwargs) -> None:
        super(PerformanceLevelCapability, self).__init__(**kwargs)
        self.value = None
        self.unit = None
