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


class EventsAiInfo(Model):
    """AI related application info for an event result.

    :param i_key: iKey of the app
    :type i_key: str
    :param app_name: Name of the application
    :type app_name: str
    :param app_id: ID of the application
    :type app_id: str
    :param sdk_version: SDK version of the application
    :type sdk_version: str
    """

    _attribute_map = {
        'i_key': {'key': 'iKey', 'type': 'str'},
        'app_name': {'key': 'appName', 'type': 'str'},
        'app_id': {'key': 'appId', 'type': 'str'},
        'sdk_version': {'key': 'sdkVersion', 'type': 'str'},
    }

    def __init__(self, *, i_key: str=None, app_name: str=None, app_id: str=None, sdk_version: str=None, **kwargs) -> None:
        super(EventsAiInfo, self).__init__(**kwargs)
        self.i_key = i_key
        self.app_name = app_name
        self.app_id = app_id
        self.sdk_version = sdk_version
