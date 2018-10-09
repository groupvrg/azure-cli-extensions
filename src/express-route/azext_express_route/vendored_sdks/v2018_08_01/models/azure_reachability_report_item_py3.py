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


class AzureReachabilityReportItem(Model):
    """Azure reachability report details for a given provider location.

    :param provider: The Internet service provider.
    :type provider: str
    :param azure_location: The Azure region.
    :type azure_location: str
    :param latencies: List of latency details for each of the time series.
    :type latencies:
     list[~azure.mgmt.network.v2018_08_01.models.AzureReachabilityReportLatencyInfo]
    """

    _attribute_map = {
        'provider': {'key': 'provider', 'type': 'str'},
        'azure_location': {'key': 'azureLocation', 'type': 'str'},
        'latencies': {'key': 'latencies', 'type': '[AzureReachabilityReportLatencyInfo]'},
    }

    def __init__(self, *, provider: str=None, azure_location: str=None, latencies=None, **kwargs) -> None:
        super(AzureReachabilityReportItem, self).__init__(**kwargs)
        self.provider = provider
        self.azure_location = azure_location
        self.latencies = latencies
