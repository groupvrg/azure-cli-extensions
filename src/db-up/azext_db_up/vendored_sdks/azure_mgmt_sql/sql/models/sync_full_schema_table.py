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


class SyncFullSchemaTable(Model):
    """Properties of the table in the database full schema.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar columns: List of columns in the table of database full schema.
    :vartype columns: list[~azure.mgmt.sql.models.SyncFullSchemaTableColumn]
    :ivar error_id: Error id of the table.
    :vartype error_id: str
    :ivar has_error: If there is error in the table.
    :vartype has_error: bool
    :ivar name: Name of the table.
    :vartype name: str
    :ivar quoted_name: Quoted name of the table.
    :vartype quoted_name: str
    """

    _validation = {
        'columns': {'readonly': True},
        'error_id': {'readonly': True},
        'has_error': {'readonly': True},
        'name': {'readonly': True},
        'quoted_name': {'readonly': True},
    }

    _attribute_map = {
        'columns': {'key': 'columns', 'type': '[SyncFullSchemaTableColumn]'},
        'error_id': {'key': 'errorId', 'type': 'str'},
        'has_error': {'key': 'hasError', 'type': 'bool'},
        'name': {'key': 'name', 'type': 'str'},
        'quoted_name': {'key': 'quotedName', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(SyncFullSchemaTable, self).__init__(**kwargs)
        self.columns = None
        self.error_id = None
        self.has_error = None
        self.name = None
        self.quoted_name = None
