import logging
import os
import subprocess
import time

from .. config.cartridgeagentconfiguration import CartridgeAgentConfiguration
from .. topology.topologycontext import *

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def execute_copy_artifact_extension(source, destination):
    try:
        log.debug("Executing artifacts copy extension")
        script_name = cartridgeagentconstants.ARTIFACTS_COPY_SCRIPT
        command = prepare_command(script_name)

        output, errors = execute_command(command + " " + source + " " + destination)
        log.debug("Artifacts copy script returned: %r" % output)
    except:
        log.exception("Could not execute artifacts copy extension")


def execute_instance_started_extension(env_params):
    try:
        log.debug("Executing instance started extension")

        script_name = cartridgeagentconstants.INSTANCE_STARTED_SCRIPT
        command = prepare_command(script_name)
        env_params = add_payload_parameters(env_params)
        env_params = clean_process_parameters(env_params)

        output, errors = execute_command(command, env_params)
        log.debug("Instance started script returned: %r" % output)
    except:
        log.exception("Could not execute instance started extension")


def execute_instance_activated_extension():
    try:
        log.debug("Executing instance activated extension")
        script_name = cartridgeagentconstants.INSTANCE_ACTIVATED_SCRIPT
        command = prepare_command(script_name)

        output, errors = execute_command(command)
        log.debug("Instance activated script returned: %r" % output)
    except:
        log.exception("Could not execute instance activated extension")


def execute_artifacts_updated_extension(env_params):
    try:
        log.debug("Executing artifacts updated extension")

        script_name = cartridgeagentconstants.ARTIFACTS_UPDATED_SCRIPT
        command = prepare_command(script_name)
        env_params = add_payload_parameters(env_params)
        env_params = clean_process_parameters(env_params)

        output, errors = execute_command(command, env_params)
        log.debug("Artifacts updated script returned: %r" % output)
    except:
        log.exception("Could not execute artifacts updated extension")


def execute_subscription_domain_added_extension(env_params):
    try:
        log.debug("Executing subscription domain added extension")

        script_name = cartridgeagentconstants.SUBSCRIPTION_DOMAIN_ADDED_SCRIPT
        command = prepare_command(script_name)
        env_params = add_payload_parameters(env_params)
        env_params = clean_process_parameters(env_params)

        output, errors = execute_command(command, env_params)
        log.debug("Subscription domain added script returned: %r" % output)
    except:
        log.exception("Could not execute subscription domain added extension")


def execute_subscription_domain_removed_extension(env_params):
    try:
        log.debug("Executing subscription domain removed extension")

        script_name = cartridgeagentconstants.SUBSCRIPTION_DOMAIN_REMOVED_SCRIPT
        command = prepare_command(script_name)
        env_params = add_payload_parameters(env_params)
        env_params = clean_process_parameters(env_params)

        output, errors = execute_command(command, env_params)
        log.debug("Subscription domain removed script returned: %r" % output)
    except:
        log.exception("Could not execute subscription domain removed extension")


def execute_start_servers_extension(env_params):
    try:
        log.debug("Executing start servers extension")

        script_name = cartridgeagentconstants.START_SERVERS_SCRIPT
        command = prepare_command(script_name)
        env_params = add_payload_parameters(env_params)
        env_params = clean_process_parameters(env_params)

        output, errors = execute_command(command, env_params)
        log.debug("Start servers script returned: %r" % output)
    except:
        log.exception("Could not execute start servers extension")


def execute_complete_topology_extension(env_params):
    try:
        log.debug("Executing complete topology extension")

        script_name = cartridgeagentconstants.COMPLETE_TOPOLOGY_SCRIPT
        command = prepare_command(script_name)
        env_params = add_payload_parameters(env_params)
        env_params = clean_process_parameters(env_params)

        output, errors = execute_command(command, env_params)
        log.debug("Complete topology script returned: %r" % output)
    except:
        log.exception("Could not execute complete topology extension")


def execute_complete_tenant_extension(env_params):
    try:
        log.debug("Executing complete tenant extension")

        script_name = cartridgeagentconstants.COMPLETE_TENANT_SCRIPT
        command = prepare_command(script_name)
        env_params = add_payload_parameters(env_params)
        env_params = clean_process_parameters(env_params)

        output, errors = execute_command(command, env_params)
        log.debug("Complete tenant script returned: %r" % output)
    except:
        log.exception("Could not execute complete tenant extension")


def execute_tenant_subscribed_extension(env_params):
    try:
        log.debug("Executing tenant subscribed extension")

        script_name = cartridgeagentconstants.TENANT_SUBSCRIBED_SCRIPT
        command = prepare_command(script_name)
        env_params = add_payload_parameters(env_params)
        env_params = clean_process_parameters(env_params)

        output, errors = execute_command(command, env_params)
        log.debug("Tenant subscribed script returned: %r" % output)
    except:
        log.exception("Could not execute tenant subscribed extension")


def execute_tenant_unsubscribed_extension(env_params):
    try:
        log.debug("Executing tenant unsubscribed extension")

        script_name = cartridgeagentconstants.TENANT_UNSUBSCRIBED_SCRIPT
        command = prepare_command(script_name)
        env_params = add_payload_parameters(env_params)
        env_params = clean_process_parameters(env_params)

        output, errors = execute_command(command, env_params)
        log.debug("Tenant unsubscribed script returned: %r" % output)
    except:
        log.exception("Could not execute tenant unsubscribed extension")


def execute_member_terminated_extension(env_params):
    try:
        log.debug("Executing member terminated extension")

        script_name = cartridgeagentconstants.MEMBER_TERMINATED_SCRIPT
        command = prepare_command(script_name)
        env_params = add_payload_parameters(env_params)
        env_params = clean_process_parameters(env_params)

        output, errors = execute_command(command, env_params)
        log.debug("Member terminated script returned: %r" % output)
    except:
        log.exception("Could not execute member terminated extension")


def execute_member_suspended_extension(env_params):
    try:
        log.debug("Executing member suspended extension")

        script_name = cartridgeagentconstants.MEMBER_SUSPENDED_SCRIPT
        command = prepare_command(script_name)
        env_params = add_payload_parameters(env_params)
        env_params = clean_process_parameters(env_params)

        output, errors = execute_command(command, env_params)
        log.debug("Member suspended script returned: %r" % output)
    except:
        log.exception("Could not execute member suspended extension")

def execute_member_started_extension(env_params):
    try:
        log.debug("Executing member started extension")

        script_name = cartridgeagentconstants.MEMBER_STARTED_SCRIPT
        command = prepare_command(script_name)
        env_params = add_payload_parameters(env_params)
        env_params = clean_process_parameters(env_params)

        output, errors = execute_command(command, env_params)
        log.debug("Member started script returned: %r" % output)
    except:
        log.exception("Could not execute member started extension")


def wait_for_complete_topology():
    while not TopologyContext.topology.initialized:
        log.info("Waiting for complete topology event...")
        time.sleep(5)


def check_topology_consistency(service_name, cluster_id, member_id):
    topology = TopologyContext.get_topology()
    service = topology.get_service(service_name)
    if service is None:
        log.error("Service not found in topology [service] %r" % service_name)
        return False

    cluster = service.get_cluster(cluster_id)
    if cluster is None:
        log.error("Cluster id not found in topology [cluster] %r" % cluster_id)
        return False

    activated_member = cluster.get_member(member_id)
    if activated_member is None:
        log.error("Member id not found in topology [member] %r" % member_id)
        return False

    return True


def is_relevant_member_event(service_name, cluster_id, lb_cluster_id):
    cluster_id_in_payload = CartridgeAgentConfiguration.cluster_id
    if cluster_id_in_payload is None:
        return False

    topology = TopologyContext.get_topology()
    if topology is None or not topology.initialized:
        return False

    if cluster_id_in_payload == cluster_id:
        return True

    if cluster_id_in_payload == lb_cluster_id:
        return True

    service_group_in_payload = CartridgeAgentConfiguration.service_group
    if service_group_in_payload is not None:
        service_properties = topology.get_service(service_name).properties
        if service_properties is None:
            return False

        member_service_group = service_properties[cartridgeagentconstants.SERVICE_GROUP_TOPOLOGY_KEY]
        if member_service_group is not None and member_service_group == service_group_in_payload:
            if service_name == CartridgeAgentConfiguration.service_name:
                log.debug("Service names are same")
                return True
            elif "apistore" == CartridgeAgentConfiguration.service_name and service_name == "publisher":
                log.debug("Service name in payload is [store]. Serivce name in event is [%r] " % service_name)
                return True
            elif "publisher" == CartridgeAgentConfiguration.service_name and service_name == "apistore":
                log.debug("Service name in payload is [publisher]. Serivce name in event is [%r] " % service_name)
                return True
            elif cartridgeagentconstants.DEPLOYMENT_WORKER == CartridgeAgentConfiguration.deployment and service_name == CartridgeAgentConfiguration.manager_service_name:
                log.debug("Deployment is worker. Worker's manager service name & service name in event are same")
                return True
            elif cartridgeagentconstants.DEPLOYMENT_MANAGER == CartridgeAgentConfiguration.deployment  and service_name == CartridgeAgentConfiguration.worker_service_name:
                log.debug("Deployment is manager. Manager's worker service name & service name in event are same")
                return True

    return False


def execute_volume_mount_extension(persistance_mappings_payload):
    try:
        log.debug("Executing volume mounting extension: [payload] %r" % persistance_mappings_payload)
        script_name = cartridgeagentconstants.MOUNT_VOLUMES_SCRIPT
        command = prepare_command(script_name)

        output, errors = execute_command(command + " " + persistance_mappings_payload)
        log.debug("Volume mount script returned: %r" % output)
    except:
        log.exception("Could not execute Volume mount extension")


def execute_cleanup_extension():
    try:
        log.debug("Executing cleanup extension")
        script_name = cartridgeagentconstants.CLEAN_UP_SCRIPT
        command = prepare_command(script_name)

        output, errors = execute_command(command)
        log.debug("Cleanup script returned: %r" % output)
    except:
        log.exception("Could not execute Cleanup extension")


def execute_member_activated_extension(env_params):
    try:
        log.debug("Executing member activated extension")

        script_name = cartridgeagentconstants.MEMBER_ACTIVATED_SCRIPT
        command = prepare_command(script_name)
        env_params = add_payload_parameters(env_params)
        env_params = clean_process_parameters(env_params)

        output, errors = execute_command(command, env_params)
        log.debug("Member activated script returned: %r" % output)
    except:
        log.exception("Could not execute member activated extension")


def prepare_command(script_name):
    extensions_dir = CartridgeAgentConfiguration.read_property(cartridgeagentconstants.EXTENSIONS_DIR)
    if extensions_dir.strip() == "":
        raise RuntimeError("System property not found: %r" % cartridgeagentconstants.EXTENSIONS_DIR)

    file_path = extensions_dir + script_name if str(extensions_dir).endswith("/") else extensions_dir + "/" + script_name

    if os.path.isfile(file_path):
        return file_path

    raise IOError("Script file not found : %r" % file_path)


def clean_process_parameters(params):
    """

    :param dict params:
    :return: cleaned parameters
    :rtype: dict
    """
    for key, value in params.items():
        if value is None:
            del params[key]

    return params


def add_payload_parameters(env_params):
    env_params["STRATOS_APP_PATH"] = CartridgeAgentConfiguration.app_path
    env_params["STRATOS_PARAM_FILE_PATH"] = CartridgeAgentConfiguration.read_property(cartridgeagentconstants.PARAM_FILE_PATH)
    env_params["STRATOS_SERVICE_NAME"] = CartridgeAgentConfiguration.service_name
    env_params["STRATOS_TENANT_ID"] = CartridgeAgentConfiguration.tenant_id
    env_params["STRATOS_CARTRIDGE_KEY"] = CartridgeAgentConfiguration.cartridge_key
    env_params["STRATOS_LB_CLUSTER_ID"] = CartridgeAgentConfiguration.lb_cluster_id
    env_params["STRATOS_CLUSTER_ID"] = CartridgeAgentConfiguration.cluster_id
    env_params["STRATOS_NETWORK_PARTITION_ID"] = CartridgeAgentConfiguration.network_partition_id
    env_params["STRATOS_PARTITION_ID"] = CartridgeAgentConfiguration.partition_id
    env_params["STRATOS_PERSISTENCE_MAPPINGS"] = CartridgeAgentConfiguration.persistence_mappings
    env_params["STRATOS_REPO_URL"] = CartridgeAgentConfiguration.repo_url

    lb_cluster_id_in_payload = CartridgeAgentConfiguration.lb_cluster_id
    member_ips = get_lb_member_ip(lb_cluster_id_in_payload)
    if member_ips is not None:
        env_params["STRATOS_LB_IP"] = member_ips[0]
        env_params["STRATOS_LB_PUBLIC_IP"] = member_ips[1]
    else:
        env_params["STRATOS_LB_IP"] = CartridgeAgentConfiguration.lb_private_ip
        env_params["STRATOS_LB_PUBLIC_IP"] = CartridgeAgentConfiguration.lb_public_ip

    topology = TopologyContext.get_topology()
    if topology.initialized:
        service = topology.get_service(CartridgeAgentConfiguration.service_name)
        cluster = service.get_cluster(CartridgeAgentConfiguration.cluster_id)
        member_id_in_payload = CartridgeAgentConfiguration.member_id
        add_properties(service.properties, env_params, "SERVICE_PROPERTY")
        add_properties(cluster.properties, env_params, "CLUSTER_PROPERTY")
        add_properties(cluster.get_member(member_id_in_payload).properties, env_params, "MEMBER_PROPERTY")

    return env_params


def add_properties(properties, params, prefix):
    """
    :param dict properties: service properties
    :param dict params:
    :param str prefix:
    :return:
    """
    if properties is None or properties.items() is None:
        return

    for key in properties:
        params["STRATOS_" + prefix + "_" + key] = properties[key]
        log.debug("Property added: [key] STRATOS_ " + prefix + "_" + key + "[value] " + properties[key])


def get_lb_member_ip(lb_cluster_id):
    topology = TopologyContext.get_topology()
    services = topology.get_services()

    for service in services:
        clusters = service.get_clusters()
        for cluster in clusters:
            members = cluster.get_members()
            for member in members:
                if member.cluster_id == lb_cluster_id:
                    return [member.member_ip, member.member_public_ip]

    return None


def execute_command(command, env_params=None):
    """

    :param str command:
    :param dict env_params:
    :return: output and error tuple
    :rtype: tuple
    """
    os_env = os.environ.copy()
    if env_params is not None:
        os_env.update(env_params)

    p = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os_env)
    output, errors = p.communicate()
    log.debug("output = %r" % output)
    log.debug("error = %r" % errors)
    if len(errors) > 0:
        raise RuntimeError("Command execution failed: \n %r" % errors)

    return output, errors
