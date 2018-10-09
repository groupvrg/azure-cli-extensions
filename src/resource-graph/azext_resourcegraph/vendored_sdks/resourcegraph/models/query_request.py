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


class QueryRequest(Model):
    """Describes a query to be executed.

    All required parameters must be populated in order to send to Azure.

    :param subscriptions: Required. Azure subscriptions against which to
     execute the query.
    :type subscriptions: list[str]
    :param query: Required. The resources query.
    :type query: str
    :param options: The query evaluation options
    :type options: ~azure.mgmt.resourcegraph.models.QueryRequestOptions
    :param facets: An array of facet requests to be computed against the query
     result.
    :type facets: list[~azure.mgmt.resourcegraph.models.FacetRequest]
    """

    _validation = {
        'subscriptions': {'required': True},
        'query': {'required': True},
    }

    _attribute_map = {
        'subscriptions': {'key': 'subscriptions', 'type': '[str]'},
        'query': {'key': 'query', 'type': 'str'},
        'options': {'key': 'options', 'type': 'QueryRequestOptions'},
        'facets': {'key': 'facets', 'type': '[FacetRequest]'},
    }

    def __init__(self, **kwargs):
        super(QueryRequest, self).__init__(**kwargs)
        self.subscriptions = kwargs.get('subscriptions', None)
        self.query = kwargs.get('query', None)
        self.options = kwargs.get('options', None)
        self.facets = kwargs.get('facets', None)
