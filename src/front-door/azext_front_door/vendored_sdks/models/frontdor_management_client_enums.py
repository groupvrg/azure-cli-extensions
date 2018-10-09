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

from enum import Enum


class FrontDoorResourceState(str, Enum):

    creating = "Creating"
    enabling = "Enabling"
    enabled = "Enabled"
    disabling = "Disabling"
    disabled = "Disabled"
    deleting = "Deleting"


class CustomHttpsProvisioningState(str, Enum):

    enabling = "Enabling"
    enabled = "Enabled"
    disabling = "Disabling"
    disabled = "Disabled"
    failed = "Failed"


class CustomHttpsProvisioningSubstate(str, Enum):

    submitting_domain_control_validation_request = "SubmittingDomainControlValidationRequest"
    pending_domain_control_validation_request_approval = "PendingDomainControlValidationREquestApproval"
    domain_control_validation_request_approved = "DomainControlValidationRequestApproved"
    domain_control_validation_request_rejected = "DomainControlValidationRequestRejected"
    domain_control_validation_request_timed_out = "DomainControlValidationRequestTimedOut"
    issuing_certificate = "IssuingCertificate"
    deploying_certificate = "DeployingCertificate"
    certificate_deployed = "CertificateDeployed"
    deleting_certificate = "DeletingCertificate"
    certificate_deleted = "CertificateDeleted"


class FrontDoorCertificateSource(str, Enum):

    azure_key_vault = "AzureKeyVault"
    front_door = "FrontDoor"


class FrontDoorTlsProtocolType(str, Enum):

    server_name_indication = "ServerNameIndication"


class FrontDoorCertificateType(str, Enum):

    dedicated = "Dedicated"


class FrontDoorEnabledState(str, Enum):

    enabled = "Enabled"
    disabled = "Disabled"


class FrontDoorProtocol(str, Enum):

    http = "Http"
    https = "Https"


class FrontDoorForwardingProtocol(str, Enum):

    http_only = "HttpOnly"
    https_only = "HttpsOnly"
    match_request = "MatchRequest"


class FrontDoorQuery(str, Enum):

    strip_none = "StripNone"
    strip_all = "StripAll"


class DynamicCompressionEnabled(str, Enum):

    enabled = "Enabled"
    disabled = "Disabled"


class SessionAffinityEnabledState(str, Enum):

    enabled = "Enabled"
    disabled = "Disabled"


class ResourceType(str, Enum):

    microsoft_networkfront_doors = "Microsoft.Network/frontDoors"
    microsoft_networkfront_doorsfrontend_endpoints = "Microsoft.Network/frontDoors/frontendEndpoints"


class Availability(str, Enum):

    available = "Available"
    unavailable = "Unavailable"


class NetworkOperationStatus(str, Enum):

    in_progress = "InProgress"
    succeeded = "Succeeded"
    failed = "Failed"


class EnabledState(str, Enum):

    disabled = "Disabled"
    enabled = "Enabled"


class Mode(str, Enum):

    prevention = "Prevention"
    detection = "Detection"


class RuleType(str, Enum):

    match_rule = "MatchRule"
    rate_limit_rule = "RateLimitRule"


class MatchCondition(str, Enum):

    remote_addr = "RemoteAddr"
    request_method = "RequestMethod"
    query_string = "QueryString"
    post_args = "PostArgs"
    request_uri = "RequestUri"
    request_header = "RequestHeader"
    request_body = "RequestBody"


class Operator(str, Enum):

    any = "Any"
    ip_match = "IPMatch"
    geo_match = "GeoMatch"
    equal = "Equal"
    contains = "Contains"
    less_than = "LessThan"
    greater_than = "GreaterThan"
    less_than_or_equal = "LessThanOrEqual"
    greater_than_or_equal = "GreaterThanOrEqual"
    begins_with = "BeginsWith"
    ends_with = "EndsWith"


class Action(str, Enum):

    allow = "Allow"
    block = "Block"
    log = "Log"


class Transform(str, Enum):

    lowercase = "Lowercase"
    uppercase = "Uppercase"
    trim = "Trim"
    url_decode = "UrlDecode"
    url_encode = "UrlEncode"
    remove_nulls = "RemoveNulls"
    html_entity_decode = "HtmlEntityDecode"


class RuleGroupOverride(str, Enum):

    sql_injection = "SqlInjection"
    xss = "XSS"
