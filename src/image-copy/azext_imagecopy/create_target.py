# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import datetime
import time
from azext_imagecopy.cli_utils import run_cli_command, prepare_cli_command
from knack.util import CLIError

from knack.log import get_logger
import pprint
logger = get_logger(__name__)

STORAGE_ACCOUNT_NAME_LENGTH = 24


# pylint: disable=too-many-locals
def create_target_image(location, transient_resource_group_name, source_type, source_object_name,
                        source_os_disk_snapshot_name, source_os_disk_snapshot_url, source_os_type,
                        target_resource_group_name, azure_pool_frequency, tags, target_name, target_subscription,
                        timeout, manifest):


    random_string = get_random_string(STORAGE_ACCOUNT_NAME_LENGTH - len(location))

    # create the target storage account. storage account name must be lowercase.
    logger.warn(
        "%s - Creating target storage account (can be slow sometimes)", location)
    target_storage_account_name = location.lower() + random_string
    cli_cmd = prepare_cli_command(['storage', 'account', 'create',
                                   '--name', target_storage_account_name,
                                   '--resource-group', transient_resource_group_name,
                                   '--location', location,
                                   '--sku', 'Standard_LRS'],
                                  subscription=target_subscription)

    json_output = run_cli_command(cli_cmd, return_as_json=True)
    target_blob_endpoint = json_output['primaryEndpoints']['blob']

    # Setup the target storage account
    cli_cmd = prepare_cli_command(['storage', 'account', 'keys', 'list',
                                   '--account-name', target_storage_account_name,
                                   '--resource-group', transient_resource_group_name],
                                  subscription=target_subscription)

    json_output = run_cli_command(cli_cmd, return_as_json=True)

    target_storage_account_key = json_output[0]['value']
    logger.debug("storage account key: %s", target_storage_account_key)

    expiry_format = "%Y-%m-%dT%H:%MZ"
    expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=timeout)
    logger.debug("create target storage sas using timeout seconds: %d", timeout)

    cli_cmd = prepare_cli_command(['storage', 'account', 'generate-sas',
                                   '--account-name', target_storage_account_name,
                                   '--account-key', target_storage_account_key,
                                   '--expiry', expiry.strftime(expiry_format),
                                   '--permissions', 'aclrpuw', '--resource-types',
                                   'sco', '--services', 'b', '--https-only'],
                                  output_as_json=False,
                                  subscription=target_subscription)

    sas_token = run_cli_command(cli_cmd)
    sas_token = sas_token.rstrip("\n\r")  # STRANGE
    logger.debug("sas token: %s", sas_token)

    # create a container in the target blob storage account
    logger.warn(
        "%s - Creating container in the target storage account", location)
    target_container_name = 'snapshots'
    cli_cmd = prepare_cli_command(['storage', 'container', 'create',
                                   '--name', target_container_name,
                                   '--account-name', target_storage_account_name],
                                  subscription=target_subscription)

    run_cli_command(cli_cmd)

    # Copy the snapshot to the target region using the SAS URL
    blob_name = source_os_disk_snapshot_name + '.vhd'
    logger.warn(
        "%s - Copying blob to target storage account", location)
    cli_cmd = prepare_cli_command(['storage', 'blob', 'copy', 'start',
                                   '--source-uri', source_os_disk_snapshot_url,
                                   '--destination-blob', blob_name,
                                   '--destination-container', target_container_name,
                                   '--account-name', target_storage_account_name,
                                   '--sas-token', sas_token],
                                  subscription=target_subscription)

    run_cli_command(cli_cmd)

    # Wait for the copy to complete
    start_datetime = datetime.datetime.now()
    wait_for_blob_copy_operation(blob_name, target_container_name, target_storage_account_name,
                                 azure_pool_frequency, location, target_subscription)
    msg = "{0} - Copy time: {1}".format(
        location, datetime.datetime.now() - start_datetime)
    logger.warn(msg)


    # Create the snapshot in the target region from the copied blob
    logger.warn(
        "%s - Creating snapshot in target region from the copied blob", location)
    target_blob_path = target_blob_endpoint + \
        target_container_name + '/' + blob_name
    target_snapshot_name = source_os_disk_snapshot_name + '-' + location
    cli_cmd = prepare_cli_command(['snapshot', 'create',
                                   '--resource-group', transient_resource_group_name,
                                   '--name', target_snapshot_name,
                                   '--location', location,
                                   '--source', target_blob_path],
                                  subscription=target_subscription)

    logger.warn("%s -Sleeping for 30 seconds", location)

    create_snapshot_retry_count = 0
    while create_snapshot_retry_count < 10:
        create_snapshot_retry_count += 1
        try:
            logger.warn("%s - Trying to create snapshot from vhd, try %d/10",location, create_snapshot_retry_count)
            json_output = create_snapshot_from_vhd(location, target_blob_path, target_snapshot_name,
                                                   transient_resource_group_name)
            break
        except Exception as ex:
            logger.warn("%s - Failed to create snapshot, ex: %s", location, str(ex))
            logger.warn("%s - Sleeping for 30 seconds", location)
            time.sleep(30)

    target_snapshot_id = json_output['id']

    # Create the final image
    logger.warn("%s - Creating final image", location)
    if target_name is None:
        target_image_name = source_object_name
        if source_type != 'image':
            target_image_name += '-image'
        target_image_name += '-' + location
    else:
        target_image_name = target_name


    cli_cmd = prepare_cli_command(['image', 'create',
                                   '--resource-group', target_resource_group_name,
                                   '--name', target_image_name,
                                   '--location', location,
                                   '--source', target_blob_path,
                                   '--os-type', source_os_type,
                                   '--source', target_snapshot_id],
                                  tags=tags,
                                  subscription=target_subscription)

    run_cli_command(cli_cmd)

    logger.warn("%s - Updating manifest object", location)
    manifest[location] = target_image_name
    logger.warn("%s - Manifest object state: %s",location, pprint.pformat(manifest))



def create_snapshot_from_vhd(location, target_blob_path, target_snapshot_name,
                             transient_resource_group_name):
    cli_cmd = prepare_cli_command(['snapshot', 'create',
                                   '--resource-group', transient_resource_group_name,
                                   '--name', target_snapshot_name,
                                   '--location', location,
                                   '--source', target_blob_path])
    json_output = run_cli_command(cli_cmd, return_as_json=True)
    return json_output


def wait_for_blob_copy_operation(blob_name, target_container_name, target_storage_account_name,
                                 azure_pool_frequency, location, subscription):
    copy_status = "pending"
    prev_progress = -1
    retries = 0
    while copy_status == "pending":
        try:
            cli_cmd = prepare_cli_command(['storage', 'blob', 'show',
                                           '--name', blob_name,
                                           '--container-name', target_container_name,
                                           '--account-name', target_storage_account_name],
                                          subscription=subscription)

            json_output = run_cli_command(cli_cmd, return_as_json=True)
            copy_status = json_output["properties"]["copy"]["status"]
            copy_progress_1, copy_progress_2 = json_output["properties"]["copy"]["progress"].split(
                "/")
            current_progress = int(
                int(copy_progress_1) / int(copy_progress_2) * 100)
        except Exception as ex:
            logger.warn("Got exception when trying to get blob: %s state, \n ex %s", blob_name, str(ex))
            if retries < 10:
                time.sleep(20)
                retries += 1
            else:
                raise ex

        if current_progress != prev_progress:
            msg = "{0} - Copy progress: {1}%"\
                .format(location, str(current_progress))
            logger.warn(msg)

        prev_progress = current_progress

        try:
            time.sleep(azure_pool_frequency)
        except KeyboardInterrupt:
            return

    if copy_status != 'success':
        logger.error("The copy operation didn't succeed. Last status: %s", copy_status)
        logger.error("Command run: %s", cli_cmd)
        logger.error("Command output: %s", json_output)

        raise CLIError('Blob copy failed')


def get_random_string(length):
    import string
    import random
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))
