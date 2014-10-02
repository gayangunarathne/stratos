import ConfigParser
import logging
import os

from ..util.log import LogFactory


class CartridgeAgentConfiguration:
    """
    Handles the configuration information of the particular Cartridge Agent
    """
    class __CartridgeAgentConfiguration:
        def __init__(self):
            # set log level
            self.log = LogFactory().get_log(__name__)

            self.payload_params = {}
            self.properties = None

            self.service_group = None
            """ :type : str  """
            self.is_clustered = False
            """ :type : bool  """
            self.service_name = None
            """ :type : str  """
            self.cluster_id = None
            """ :type : str  """
            self.network_partition_id = None
            """ :type : str  """
            self.partition_id = None
            """ :type : str  """
            self.member_id = None
            """ :type : str  """
            self.cartridge_key = None
            """ :type : str  """
            self.app_path = None
            """ :type : str  """
            self.repo_url = None
            """ :type : str  """
            self.ports = []
            """ :type : list[str]  """
            self.log_file_paths = []
            """ :type : list[str]  """
            self.is_multitenant = False
            """ :type : bool  """
            self.persistence_mappings = None
            """ :type : str  """
            self.is_commits_enabled = False
            """ :type : bool  """
            self.is_checkout_enabled = False
            """ :type : bool  """
            self.listen_address = None
            """ :type : str  """
            self.is_internal_repo = False
            """ :type : bool  """
            self.tenant_id = None
            """ :type : str  """
            self.lb_cluster_id = None
            """ :type : str  """
            self.min_count = None
            """ :type : str  """
            self.lb_private_ip = None
            """ :type : str  """
            self.lb_public_ip = None
            """ :type : str  """
            self.tenant_repository_path = None
            """ :type : str  """
            self.super_tenant_repository_path = None
            """ :type : str  """
            self.deployment = None
            """ :type : str  """
            self.manager_service_name = None
            """ :type : str  """
            self.worker_service_name = None
            """ :type : str  """
            self.is_primary = False
            """ :type : bool  """

            self.payload_params = {}
            self.__read_conf_file()
            self.__read_parameter_file()

            try:
                service_group = self.payload_params[cartridgeagentconstants.SERVICE_GROUP] \
                    if cartridgeagentconstants.SERVICE_GROUP in self.payload_params \
                    else None

                if cartridgeagentconstants.CLUSTERING in self.payload_params and \
                        str(self.payload_params[cartridgeagentconstants.CLUSTERING]).strip().lower() == "true":
                    self.is_clustered = True
                else:
                    self.is_clustered = False
                # self.__isClustered = self.payload_params[
                # cartridgeagentconstants.CLUSTERING] if cartridgeagentconstants.CLUSTERING in self.payload_params else None

                self.service_name = self.read_property(cartridgeagentconstants.SERVICE_NAME)
                self.cluster_id = self.read_property(cartridgeagentconstants.CLUSTER_ID)
                self.network_partition_id = self.read_property(cartridgeagentconstants.NETWORK_PARTITION_ID)
                self.partition_id = self.read_property(cartridgeagentconstants.PARTITION_ID)
                self.member_id = self.read_property(cartridgeagentconstants.MEMBER_ID)
                self.cartridge_key = self.read_property(cartridgeagentconstants.CARTRIDGE_KEY)
                self.app_path = self.read_property(cartridgeagentconstants.APP_PATH)
                self.repo_url = self.read_property(cartridgeagentconstants.REPO_URL)
                self.ports = str(self.read_property(cartridgeagentconstants.PORTS)).split("|")

                try:
                    self.log_file_paths = str(
                        self.read_property(cartridgeagentconstants.CLUSTER_ID)).strip().split("|")
                except ParameterNotFoundException as ex:
                    self.log.debug("Cannot read log file path : %r" % ex.get_message())
                    self.log_file_paths = None

                is_multi_str = self.read_property(cartridgeagentconstants.CLUSTER_ID)
                self.is_multitenant = True if str(
                    is_multi_str).lower().strip() == "true" else False

                try:
                    self.persistence_mappings = self.read_property(
                        cartridgeagentconstants.PERSISTENCE_MAPPING)
                except ParameterNotFoundException as ex:
                    self.log.debug("Cannot read persistence mapping : %r" % ex.get_message())
                    self.persistence_mappings = None

                try:
                    is_commit_str = self.read_property(cartridgeagentconstants.COMMIT_ENABLED)
                    self.is_commits_enabled = True if str(
                        is_commit_str).lower().strip() == "true" else False
                except ParameterNotFoundException:
                    try:
                        is_commit_str = self.read_property(cartridgeagentconstants.AUTO_COMMIT)
                        self.is_commits_enabled = True if str(
                            is_commit_str).lower().strip() == "true" else False
                    except ParameterNotFoundException:
                        self.log.info(
                            "%r is not found and setting it to false" % cartridgeagentconstants.COMMIT_ENABLED)
                        self.is_commits_enabled = False

                auto_checkout_str = self.read_property(cartridgeagentconstants.AUTO_CHECKOUT, False)
                self.is_checkout_enabled = True if str(
                    auto_checkout_str).lower().strip() == "true" else False

                self.listen_address = self.read_property(
                    cartridgeagentconstants.LISTEN_ADDRESS, False)

                try:
                    int_repo_str = self.read_property(cartridgeagentconstants.PROVIDER)
                    self.is_internal_repo = True if str(
                        int_repo_str).strip().lower() == cartridgeagentconstants.INTERNAL else False
                except ParameterNotFoundException:
                    self.log.info(" INTERNAL payload parameter is not found")
                    self.is_internal_repo = False

                self.tenant_id = self.read_property(
                    cartridgeagentconstants.TENANT_ID)
                self.lb_cluster_id = self.read_property(
                    cartridgeagentconstants.LB_CLUSTER_ID)
                self.min_count = self.read_property(
                    cartridgeagentconstants.MIN_INSTANCE_COUNT)
                self.lb_private_ip = self.read_property(
                    cartridgeagentconstants.LB_PRIVATE_IP, False)
                self.lb_public_ip = self.read_property(
                    cartridgeagentconstants.LB_PUBLIC_IP, False)
                self.tenant_repository_path = self.read_property(
                    cartridgeagentconstants.TENANT_REPO_PATH, False)
                self.super_tenant_repository_path = self.read_property(
                    cartridgeagentconstants.SUPER_TENANT_REPO_PATH, False)

                try:
                    self.deployment = self.read_property(
                        cartridgeagentconstants.DEPLOYMENT)
                except ParameterNotFoundException:
                    self.deployment = None

                # Setting worker-manager setup - manager service name
                if self.deployment is None:
                    self.manager_service_name = None

                if self.deployment.lower() == cartridgeagentconstants.DEPLOYMENT_MANAGER.lower():
                    self.manager_service_name = self.service_name

                elif self.deployment.lower() == cartridgeagentconstants.DEPLOYMENT_WORKER.lower():
                    self.deployment = self.read_property(
                        cartridgeagentconstants.MANAGER_SERVICE_TYPE)

                elif self.deployment.lower() == cartridgeagentconstants.DEPLOYMENT_DEFAULT.lower():
                    self.deployment = None
                else:
                    self.deployment = None

                # Setting worker-manager setup - worker service name
                if self.deployment is None:
                    self.worker_service_name = None

                if self.deployment.lower() == cartridgeagentconstants.DEPLOYMENT_WORKER.lower():
                    self.manager_service_name = self.service_name

                elif self.deployment.lower() == cartridgeagentconstants.DEPLOYMENT_MANAGER.lower():
                    self.deployment = self.read_property(
                        cartridgeagentconstants.WORKER_SERVICE_TYPE)

                elif self.deployment.lower() == cartridgeagentconstants.DEPLOYMENT_DEFAULT.lower():
                    self.deployment = None
                else:
                    self.deployment = None

                try:
                    self.is_primary = self.read_property(
                        cartridgeagentconstants.CLUSTERING_PRIMARY_KEY)
                except ParameterNotFoundException:
                    self.is_primary = None
            except ParameterNotFoundException as ex:
                raise RuntimeError(ex)

            self.log.info("Cartridge agent configuration initialized")

            self.log.debug("service-name: %r" % self.service_name)
            self.log.debug("cluster-id: %r" % self.cluster_id)
            self.log.debug(
                "network-partition-id: %r" % self.network_partition_id)
            self.log.debug("partition-id: %r" % self.partition_id)
            self.log.debug("member-id: %r" % self.member_id)
            self.log.debug("cartridge-key: %r" % self.cartridge_key)
            self.log.debug("app-path: %r" % self.app_path)
            self.log.debug("repo-url: %r" % self.repo_url)
            self.log.debug("ports: %r" % str(self.ports))
            self.log.debug("lb-private-ip: %r" % self.lb_private_ip)
            self.log.debug("lb-public-ip: %r" % self.lb_public_ip)

        def __read_conf_file(self):
            """
            Reads and stores the agent's configuration file
            :return: void
            """

            conf_file_path = os.path.abspath(os.path.dirname(__file__)).split("modules")[0] + "agent.conf"
            self.log.debug("Config file path : %r" % conf_file_path)
            self.properties = ConfigParser.SafeConfigParser()
            self.properties.read(conf_file_path)

        def __read_parameter_file(self):
            """
            Reads the payload file of the cartridge and stores the values in a dictionary
            :return: void
            """

            param_file = self.read_property(cartridgeagentconstants.PARAM_FILE_PATH, False)

            try:
                if param_file is not None:
                    metadata_file = open(param_file)
                    metadata_payload_content = metadata_file.read()
                    for param in metadata_payload_content.split(","):
                        if param.strip() != "":
                            param_value = param.strip().split("=")
                            self.payload_params[param_value[0]] = param_value[1]

                    # self.payload_params = dict(
                    #     param.split("=") for param in metadata_payload_content.split(","))
                    metadata_file.close()
                else:
                    self.log.error("File not found: %r" % param_file)
            except:
                self.log.exception(
                    "Could not read launch parameter file, hence trying to read from System properties.")

        def read_property(self, property_key, critical=True):
            """
            Returns the value of the provided property
            :param str property_key: the name of the property to be read
            :return: Value of the property,
            :rtype: str
            :exception: ParameterNotFoundException if the provided property cannot be found
            """

            if self.properties.has_option("agent", property_key):
                self.log.debug("Has key: %r" % property_key)
                temp_str = self.properties.get("agent", property_key)
                if temp_str != "" and temp_str is not None:
                    return temp_str

            if property_key in self.payload_params:
                temp_str = self.payload_params[property_key]
                if temp_str != "" and temp_str is not None:
                    return temp_str

            if critical:
                raise ParameterNotFoundException("Cannot find the value of required parameter: %r" % property_key)

    instance = None

    def __new__(cls, *args, **kwargs):
        if not CartridgeAgentConfiguration.instance:
            CartridgeAgentConfiguration.instance = CartridgeAgentConfiguration.__CartridgeAgentConfiguration()

        return CartridgeAgentConfiguration.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


from ..exception.parameternotfoundexception import ParameterNotFoundException
from ..util import cartridgeagentconstants
