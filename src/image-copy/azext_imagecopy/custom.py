# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from multiprocessing import Pool, Manager

from azext_imagecopy.cli_utils import run_cli_command, prepare_cli_command
from azext_imagecopy.create_target import create_target_image

from knack.util import CLIError
from knack.log import get_logger
import json, pprint
logger = get_logger(__name__)


# pylint: disable=too-many-statements
# pylint: disable=too-many-locals


def imagecopy(source_resource_group_name, source_object_name, target_location,
              target_resource_group_name, temporary_resource_group_name, source_type='image',
              cleanup='false', parallel_degree=-1, tags=None, target_name=None,
              target_subscription=None, timeout=3600, verify=False, manifest_file=None):


    # get the os disk id from source vm/image
    logger.warn("Getting os disk id of the source vm/image")
    cli_cmd = prepare_cli_command([source_type, 'show',
                                   '--name', source_object_name,
                                   '--resource-group', source_resource_group_name])

    json_cmd_output = run_cli_command(cli_cmd, return_as_json=True)

    if json_cmd_output['storageProfile']['dataDisks']:
        logger.warn(
            "Data disks in the source detected, but are ignored by this extension!")

    source_os_disk_id = None
    source_os_disk_type = None

    try:
        source_os_disk_id = json_cmd_output['storageProfile']['osDisk']['managedDisk']['id']
        if source_os_disk_id is None:
            raise TypeError
        source_os_disk_type = "DISK"
        logger.debug("found %s: %s", source_os_disk_type, source_os_disk_id)
    except TypeError:
        try:
            source_os_disk_id = json_cmd_output['storageProfile']['osDisk']['blobUri']
            if source_os_disk_id is None:
                raise TypeError
            source_os_disk_type = "BLOB"
            logger.debug("found %s: %s", source_os_disk_type, source_os_disk_id)
        except TypeError:
            try:  # images created by e.g. image-copy extension
                source_os_disk_id = json_cmd_output['storageProfile']['osDisk']['snapshot']['id']
                if source_os_disk_id is None:
                    raise TypeError
                source_os_disk_type = "SNAPSHOT"
                logger.debug("found %s: %s", source_os_disk_type, source_os_disk_id)
            except TypeError:
                pass

    if source_os_disk_type is None or source_os_disk_id is None:
        logger.error(
            'Unable to locate a supported os disk type in the provided source object')
        raise CLIError('Invalid OS Disk Source Type')

    source_os_type = json_cmd_output['storageProfile']['osDisk']['osType']
    logger.debug("source_os_disk_type: %s. source_os_disk_id: %s. source_os_type: %s",
                 source_os_disk_type, source_os_disk_id, source_os_type)

    # create source snapshots
    # TODO: skip creating another snapshot when the source is a snapshot
    logger.warn("Creating source snapshot")
    source_os_disk_snapshot_name = source_object_name + '_os_disk_snapshot'
    cli_cmd = prepare_cli_command(['snapshot', 'create',
                                   '--name', source_os_disk_snapshot_name,
                                   '--resource-group', source_resource_group_name,
                                   '--source', source_os_disk_id])

    run_cli_command(cli_cmd)

    # Get SAS URL for the snapshotName
    logger.warn("Getting sas url for the source snapshot with timeout seconds: %d", timeout)
    if timeout < 3600:
        logger.warn("Timeout should be greater than 3600")
        raise CLIError('Inavlid Timeout')

    cli_cmd = prepare_cli_command(['snapshot', 'grant-access',
                                   '--name', source_os_disk_snapshot_name,
                                   '--resource-group', source_resource_group_name,
                                   '--duration-in-seconds', str(timeout)])

    json_output = run_cli_command(cli_cmd, return_as_json=True)

    source_os_disk_snapshot_url = json_output['accessSas']
    logger.debug("source os disk snapshot url: %s",
                 source_os_disk_snapshot_url)

    # Start processing in the target locations

    transient_resource_group_name = temporary_resource_group_name
    logger.info("temp resource group name is %s", transient_resource_group_name)

    # pick the first location for the temp group
    transient_resource_group_location = target_location[0].strip()
    create_resource_group(transient_resource_group_name,
                          transient_resource_group_location,
                          target_subscription)

    target_locations_count = len(target_location)
    logger.warn("Target location count: %s", target_locations_count)

    create_resource_group(target_resource_group_name,
                          target_location[0].strip(),
                          target_subscription)

    try:

        # try to get a handle on arm's 409s
        azure_pool_frequency = 5
        if target_locations_count >= 5:
            azure_pool_frequency = 15
        elif target_locations_count >= 3:
            azure_pool_frequency = 10

        pool = init_process_pool(parallel_degree, target_locations_count)

        tasks = []
        m = Manager()
        manifest = m.dict()
        for location in target_location:
            logger.warn("Creating task for location: %s", location)
            location = location.strip()
            tasks.append((location, transient_resource_group_name, source_type,
                          source_object_name, source_os_disk_snapshot_name, source_os_disk_snapshot_url,
                          source_os_type, target_resource_group_name, azure_pool_frequency,
                          tags, target_name, target_subscription, timeout, manifest))

        logger.warn("Starting async process of %d tasks for all locations", len(tasks))

        for task in tasks:
            pool.apply_async(create_target_image, task)

        pool.close()
        pool.join()
    except KeyboardInterrupt:
        logger.warn('User cancelled the operation')
        if cleanup:
            logger.warn('To cleanup temporary resources look for ones tagged with "image-copy-extension". \n'
                        'You can use the following command: az resource list --tag created_by=image-copy-extension')
        pool.terminate()
        return

    # Cleanup
    if cleanup:
        logger.warn('Deleting transient resources')

        # Delete resource group
        cli_cmd = prepare_cli_command(['group', 'delete', '--no-wait', '--yes',
                                       '--name', transient_resource_group_name],
                                      subscription=target_subscription)
        run_cli_command(cli_cmd)

        # Revoke sas for source snapshot
        cli_cmd = prepare_cli_command(['snapshot', 'revoke-access',
                                       '--name', source_os_disk_snapshot_name,
                                       '--resource-group', source_resource_group_name])
        run_cli_command(cli_cmd)

        # Delete source snapshot
        # TODO: skip this if source is snapshot and not creating a new one
        cli_cmd = prepare_cli_command(['snapshot', 'delete',
                                       '--name', source_os_disk_snapshot_name,
                                       '--resource-group', source_resource_group_name])
        run_cli_command(cli_cmd)

    if manifest_file is not None:
        dict_manifest = dict(manifest)
        logger.warn("Writing manifest %s to %s", pprint.pformat(dict_manifest), manifest_file)
        with open(manifest_file, "w+") as f:
            f.write(json.dumps(dict_manifest))

    #Verify
    if verify:
        logger.warn("verifying images created on all regions")
        dict_manifest = dict(manifest)
        for location in target_location:
            location = location.strip()
            if location not in manifest:
                logger.error("location: %s not found in manifest", location)
                logger.error("verification failed try to delete all images")
                delete_all_created_images(dict_manifest, parallel_degree, target_locations_count, target_resource_group_name)
                exit(1)


def delete_all_created_images(dict_manifest, parallel_degree, target_locations_count, target_resource_group_name):
    pool = init_process_pool(parallel_degree, target_locations_count)

    image_delete_cmds = []
    for location, image in dict_manifest.items():
        logger.warn("create delete image command for image: %s, location: %s", image, location)
        image_delete_cmds.append(prepare_cli_command(['image', 'delete', '--name', image, '--resource-group', target_resource_group_name]))

    for delete_cmd in image_delete_cmds:
        pool.apply_async(run_cli_command, delete_cmd)

    pool.close()
    pool.join()


def init_process_pool(parallel_degree, target_locations_count):
    if parallel_degree == -1:
        logger.warn("using pool size: %d", target_locations_count)
        return Pool(target_locations_count)
    else:
        poolsize = min(parallel_degree, target_locations_count)
        logger.warn("using pool size: %d", poolsize)
        return Pool(poolsize)


def create_resource_group(resource_group_name, location, subscription=None):
    # check if target resource group exists
    cli_cmd = prepare_cli_command(['group', 'exists',
                                   '--name', resource_group_name],
                                  output_as_json=False,
                                  subscription=subscription)

    cmd_output = run_cli_command(cli_cmd)

    if 'true' in cmd_output:
        return

    # create the target resource group
    logger.warn("Creating resource group: %s", resource_group_name)
    cli_cmd = prepare_cli_command(['group', 'create',
                                   '--name', resource_group_name,
                                   '--location', location],
                                  subscription=subscription)

    run_cli_command(cli_cmd)
