/*
 * Licensed to the Apache Software Foundation (ASF) under one 
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 * 
 *  http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY 
 * KIND, either express or implied.  See the License for the 
 * specific language governing permissions and limitations
 * under the License.
 */
package org.apache.stratos.autoscaler.api;

import org.apache.commons.lang.StringUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.stratos.autoscaler.applications.ApplicationHolder;
import org.apache.stratos.autoscaler.applications.parser.ApplicationParser;
import org.apache.stratos.autoscaler.applications.parser.DefaultApplicationParser;
import org.apache.stratos.autoscaler.applications.pojo.ApplicationContext;
import org.apache.stratos.autoscaler.applications.topic.ApplicationBuilder;
import org.apache.stratos.autoscaler.client.CloudControllerClient;
import org.apache.stratos.autoscaler.context.AutoscalerContext;
import org.apache.stratos.autoscaler.exception.AutoScalerException;
import org.apache.stratos.autoscaler.exception.InvalidArgumentException;
import org.apache.stratos.autoscaler.exception.application.ApplicationDefinitionException;
import org.apache.stratos.autoscaler.exception.kubernetes.*;
import org.apache.stratos.autoscaler.exception.partition.PartitionValidationException;
import org.apache.stratos.autoscaler.exception.policy.InvalidPolicyException;
import org.apache.stratos.autoscaler.interfaces.AutoScalerServiceInterface;
import org.apache.stratos.autoscaler.kubernetes.KubernetesManager;
import org.apache.stratos.autoscaler.monitor.cluster.AbstractClusterMonitor;
import org.apache.stratos.autoscaler.pojo.Dependencies;
import org.apache.stratos.autoscaler.pojo.ServiceGroup;
import org.apache.stratos.autoscaler.pojo.policy.PolicyManager;
import org.apache.stratos.autoscaler.pojo.policy.autoscale.AutoscalePolicy;
import org.apache.stratos.autoscaler.pojo.policy.deployment.ChildPolicy;
import org.apache.stratos.autoscaler.pojo.policy.deployment.DeploymentPolicy;
import org.apache.stratos.autoscaler.pojo.policy.deployment.partition.network.ApplicationLevelNetworkPartition;
import org.apache.stratos.autoscaler.pojo.policy.deployment.partition.network.ChildLevelNetworkPartition;
import org.apache.stratos.autoscaler.pojo.policy.deployment.partition.network.ChildLevelPartition;
import org.apache.stratos.autoscaler.pojo.policy.deployment.partition.network.Partition;
import org.apache.stratos.autoscaler.registry.RegistryManager;
import org.apache.stratos.autoscaler.util.AutoscalerUtil;
import org.apache.stratos.common.Properties;
import org.apache.stratos.common.Property;
import org.apache.stratos.common.kubernetes.KubernetesGroup;
import org.apache.stratos.common.kubernetes.KubernetesHost;
import org.apache.stratos.common.kubernetes.KubernetesMaster;
import org.apache.stratos.messaging.domain.applications.Application;
import org.apache.stratos.messaging.domain.applications.ClusterDataHolder;
import org.apache.stratos.messaging.domain.applications.Group;
import org.apache.stratos.metadata.client.defaults.DefaultMetaDataServiceClient;
import org.apache.stratos.metadata.client.defaults.MetaDataServiceClient;
import org.apache.stratos.metadata.client.exception.MetaDataServiceClientException;
import org.wso2.carbon.registry.api.RegistryException;

import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;

//import org.apache.stratos.autoscaler.NetworkPartitionLbHolder;
//import org.apache.stratos.autoscaler.pojo.policy.deployment.partition.PartitionManager;

/**
 * Auto Scaler Service API is responsible getting Partitions and Policies.
 */
public class AutoScalerServiceImpl implements AutoScalerServiceInterface {

    private static final Log log = LogFactory.getLog(AutoScalerServiceImpl.class);
    //    PartitionManager partitionManager = PartitionManager.getInstance();
    KubernetesManager kubernetesManager = KubernetesManager.getInstance();
//
//    public Partition[] getAllAvailablePartitions() {
//        return partitionManager.getAllPartitions();
//    }

    public DeploymentPolicy[] getAllDeploymentPolicies() {
        return PolicyManager.getInstance().getDeploymentPolicyList();
    }

    public AutoscalePolicy[] getAllAutoScalingPolicy() {
        return PolicyManager.getInstance().getAutoscalePolicyList();
    }

    @Override
    public DeploymentPolicy[] getValidDeploymentPoliciesforCartridge(String cartridgeType) {
        ArrayList<DeploymentPolicy> validPolicies = new ArrayList<DeploymentPolicy>();

        for (DeploymentPolicy deploymentPolicy : this.getAllDeploymentPolicies()) {
            /*try {
                // call CC API
                //CloudControllerClient.getInstance().validateDeploymentPolicy(cartridgeType, deploymentPolicy);
                // if this deployment policy is valid for this cartridge, add it.
                validPolicies.add(deploymentPolicy);
            } catch (PartitionValidationException ignoredException) {
                // if this policy doesn't valid for the given cartridge, add a debug log.
                if (log.isDebugEnabled()) {
                    log.debug("Deployment policy [id] " + deploymentPolicy.getId()
                            + " is not valid for Cartridge [type] " + cartridgeType, ignoredException);
                }
            }*/
        }
        return validPolicies.toArray(new DeploymentPolicy[0]);
    }

//    @Override
//    public boolean addPartition(Partition partition) throws InvalidPartitionException {
//        return partitionManager.addNewPartition(partition);
//    }

    @Override
    public String addDeploymentPolicy(DeploymentPolicy deploymentPolicy) throws InvalidPolicyException {
        String policyId = PolicyManager.getInstance().deployDeploymentPolicy(deploymentPolicy);
        //Need to start the application Monitor after validation of the deployment policies.
        //FIXME add validation
        validateDeploymentPolicy(deploymentPolicy);
        //Check whether all the clusters are there
        ApplicationHolder.acquireReadLock();
        boolean allClusterInitialized = false;
        String appId = deploymentPolicy.getApplicationId();
        try {
            Application application = ApplicationHolder.getApplications().
                    getApplication(deploymentPolicy.getApplicationId());
            if (application != null) {

                allClusterInitialized = AutoscalerUtil.allClustersInitialized(application);
            }
        } finally {
            ApplicationHolder.releaseReadLock();
        }

        if (!AutoscalerContext.getInstance().containsPendingMonitor(appId)
                                    || !AutoscalerContext.getInstance().monitorExists(appId)) {
            if(allClusterInitialized) {
                AutoscalerUtil.getInstance().
                        startApplicationMonitor(appId);
            } else {
                log.info("The application clusters are not yet created. " +
                        "Waiting for them to be created");
            }
        } else {
            log.info("The application Monitor has already been created for [Application] " + appId);
        }
        return policyId;
    }

    private boolean validateDeploymentPolicy(DeploymentPolicy deploymentPolicy) {

        for(ChildPolicy childPolicy : deploymentPolicy.getChildPolicies()) {
            String alias = childPolicy.getId();
            ApplicationHolder.acquireReadLock();
            List<Partition> partitionList = new ArrayList<Partition>();
            for(ChildLevelNetworkPartition networkPartition : childPolicy.getChildLevelNetworkPartitions()) {
                Partition[] partitions = deploymentPolicy.getApplicationLevelNetworkPartition(
                                                    networkPartition.getId()).getPartitions();
                for(Partition partition : partitions) {
                    partitionList.add(partition);
                }
            }
            try {
                Application application = ApplicationHolder.getApplications().
                                getApplication(deploymentPolicy.getApplicationId());
                Partition[] partitions = new Partition[partitionList.size()];
                Group group = application.getGroupRecursively(alias);
                if(group != null) {
                    Set<ClusterDataHolder> clusterDataHolders = group.getClusterDataHoldersOfGroup();
                    //validating the group deployment policy against the leaf cartridges
                    for(ClusterDataHolder clusterDataHolder : clusterDataHolders) {
                        CloudControllerClient.getInstance().validateDeploymentPolicy(
                                clusterDataHolder.getServiceType(), partitionList.toArray(partitions));
                    }
                } else {
                    //Validating the cartridge level deployment policy
                    ClusterDataHolder clusterDataHolder = application.
                            getClusterDataHolderRecursivelyByAlias(alias);
                    if(clusterDataHolder != null) {
                        CloudControllerClient.getInstance().validateDeploymentPolicy(
                                clusterDataHolder.getServiceType(), partitionList.toArray(partitions));
                    }
                }
            } catch (PartitionValidationException e) {
                log.error("Error while validating the deployment policy", e);
            } finally {
                ApplicationHolder.releaseReadLock();
            }

        }

        return true;
    }

    @Override
    public boolean undeployDeploymentPolicy(String applicationId) {
        return ApplicationBuilder.handleApplicationPolicyUndeployed(applicationId);
    }

    @Override
    public boolean updateDeploymentPolicy(DeploymentPolicy deploymentPolicy) throws InvalidPolicyException {
        return PolicyManager.getInstance().updateDeploymentPolicy(deploymentPolicy);
    }

    @Override
    public boolean addAutoScalingPolicy(AutoscalePolicy autoscalePolicy) throws InvalidPolicyException {
        return PolicyManager.getInstance().deployAutoscalePolicy(autoscalePolicy);
    }

    @Override
    public boolean updateAutoScalingPolicy(AutoscalePolicy autoscalePolicy) throws InvalidPolicyException {
        return PolicyManager.getInstance().updateAutoscalePolicy(autoscalePolicy);
    }

//    @Override
//    public Partition getPartition(String partitionId) {
//        return partitionManager.getPartitionById(partitionId);
//    }

    @Override
    public DeploymentPolicy getDeploymentPolicy(String deploymentPolicyId) {
        return PolicyManager.getInstance().getDeploymentPolicy(deploymentPolicyId);
    }

    @Override
    public AutoscalePolicy getAutoscalingPolicy(String autoscalingPolicyId) {
        return PolicyManager.getInstance().getAutoscalePolicy(autoscalingPolicyId);
    }

    @Override
    public ApplicationLevelNetworkPartition[] getNetworkPartitions(String deploymentPolicyId) {
        return PolicyManager.getInstance().getDeploymentPolicy(deploymentPolicyId).getApplicationLevelNetworkPartitions();
    }

    /*public Partition[] getPartitionsOfDeploymentPolicy(String deploymentPolicyId) {
        DeploymentPolicy depPol = this.getDeploymentPolicy(deploymentPolicyId);
        if (null == depPol) {
            return null;
        }

        return depPol.getAllPartitions();
    }*/

    @Override
    public KubernetesGroup[] getAllKubernetesGroups() {
        return kubernetesManager.getKubernetesGroups();
    }

    @Override
    public KubernetesGroup getKubernetesGroup(String kubernetesGroupId) throws NonExistingKubernetesGroupException {
        return kubernetesManager.getKubernetesGroup(kubernetesGroupId);
    }

    @Override
    public KubernetesMaster getMasterForKubernetesGroup(String kubernetesGroupId) throws NonExistingKubernetesGroupException {
        return kubernetesManager.getKubernetesMasterInGroup(kubernetesGroupId);
    }

    @Override
    public KubernetesHost[] getHostsForKubernetesGroup(String kubernetesGroupId) throws NonExistingKubernetesGroupException {
        return kubernetesManager.getKubernetesHostsInGroup(kubernetesGroupId);
    }


    @Override
    public boolean addKubernetesGroup(KubernetesGroup kubernetesGroup) throws InvalidKubernetesGroupException {
        return kubernetesManager.addNewKubernetesGroup(kubernetesGroup);
    }

    @Override
    public boolean addKubernetesHost(String groupId, KubernetesHost kubernetesHost) throws
            InvalidKubernetesHostException, NonExistingKubernetesGroupException {
        return kubernetesManager.addNewKubernetesHost(groupId, kubernetesHost);
    }

    @Override
    public boolean removeKubernetesGroup(String groupId) throws NonExistingKubernetesGroupException {
        return kubernetesManager.removeKubernetesGroup(groupId);
    }

    @Override
    public boolean removeKubernetesHost(String hostId) throws NonExistingKubernetesHostException {
        return kubernetesManager.removeKubernetesHost(hostId);
    }

    @Override
    public boolean updateKubernetesMaster(KubernetesMaster kubernetesMaster)
            throws InvalidKubernetesMasterException, NonExistingKubernetesMasterException {
        return kubernetesManager.updateKubernetesMaster(kubernetesMaster);
    }

    @Override
    public boolean updateKubernetesHost(KubernetesHost kubernetesHost) throws
            InvalidKubernetesHostException, NonExistingKubernetesHostException {
        return kubernetesManager.updateKubernetesHost(kubernetesHost);
    }

    //    @Override
    public Partition[] getPartitionsOfGroup(String deploymentPolicyId, String groupId) {
        DeploymentPolicy depPol = this.getDeploymentPolicy(deploymentPolicyId);
        if (null == depPol) {
            return null;
        }

        ApplicationLevelNetworkPartition group = depPol.getApplicationLevelNetworkPartition(groupId);

        if (group == null) {
            return null;
        }

        return group.getPartitions();
    }

//    public void checkLBExistenceAgainstPolicy(String lbClusterId, String deploymentPolicyId) throws NonExistingLBException {
//
//        boolean exist = false;
//        for (NetworkPartition networkPartition : PolicyManager.getInstance().getDeploymentPolicy(deploymentPolicyId).getChildLevelNetworkPartitions()) {
//
//            NetworkPartitionLbHolder nwPartitionLbHolder = partitionManager.getNetworkPartitionLbHolder(networkPartition.getId());
//
//            if (nwPartitionLbHolder.isLBExist(lbClusterId)) {
//                exist = true;
//                break;
//            }
//        }
//
//        if (!exist) {
//            String msg = "LB with [cluster id] " + lbClusterId +
//                    " does not exist in any network partition of [Deployment Policy] " + deploymentPolicyId;
//            log.error(msg);
//            throw new NonExistingLBException(msg);
//        }
//    }

//    public boolean checkDefaultLBExistenceAgainstPolicy(String deploymentPolicyId) {
//
//        for (NetworkPartition networkPartition : PolicyManager.getInstance().getDeploymentPolicy(deploymentPolicyId).getChildLevelNetworkPartitions()) {
//
//            NetworkPartitionLbHolder nwPartitionLbHolder = partitionManager.getNetworkPartitionLbHolder(networkPartition.getId());
//
//            if (!nwPartitionLbHolder.isDefaultLBExist()) {
//                if (log.isDebugEnabled()) {
//                    log.debug("Default LB does not exist in [network partition] " +
//                            nwPartitionLbHolder.getNetworkPartitionId() + " of [Deployment Policy] " +
//                            deploymentPolicyId);
//
//                }
//                return false;
//            }
//
//        }
//
//        return true;
//
//    }

//    public String getDefaultLBClusterId(String deploymentPolicyName) {
//        if (log.isDebugEnabled()) {
//            log.debug("Default LB Cluster Id for Deployment Policy [" + deploymentPolicyName + "] ");
//        }
//        for (NetworkPartition networkPartition : PolicyManager.getInstance().getDeploymentPolicy(deploymentPolicyName).getChildLevelNetworkPartitions()) {
//
//            NetworkPartitionLbHolder nwPartitionLbHolder = partitionManager.getNetworkPartitionLbHolder(networkPartition.getId());
//
//            if (nwPartitionLbHolder.isDefaultLBExist()) {
//                if (log.isDebugEnabled()) {
//                    log.debug("Default LB does not exist in [network partition] " +
//                            nwPartitionLbHolder.getNetworkPartitionId() + " of [Deployment Policy] " +
//                            deploymentPolicyName);
//
//                }
//                return nwPartitionLbHolder.getDefaultLbClusterId();
//            }
//
//        }
//
//        return null;
//    }

    @Override
    public void deployApplicationDefinition(ApplicationContext applicationContext)
            throws ApplicationDefinitionException {

        ApplicationParser applicationParser = new DefaultApplicationParser();
        Application application = applicationParser.parse(applicationContext);
        publishMetadata(applicationParser, application.getUniqueIdentifier());
        ApplicationBuilder.handleApplicationCreated(application,
                applicationParser.getApplicationClusterContexts());
    }

    @Override
    public void unDeployApplicationDefinition(String applicationId, int tenantId, String tenantDomain)
            throws ApplicationDefinitionException {

        ApplicationBuilder.handleApplicationUndeployed(applicationId);
    }

//    public boolean checkServiceLBExistenceAgainstPolicy(String serviceName, String deploymentPolicyId) {
//
//        for (NetworkPartition networkPartition : PolicyManager.getInstance().getDeploymentPolicy(deploymentPolicyId).getChildLevelNetworkPartitions()) {
//
//            NetworkPartitionLbHolder nwPartitionLbHolder = partitionManager.getNetworkPartitionLbHolder(networkPartition.getId());
//
//            if (!nwPartitionLbHolder.isServiceLBExist(serviceName)) {
//                if (log.isDebugEnabled()) {
//                    log.debug("Service LB [service name] " + serviceName + " does not exist in [network partition] " +
//                            nwPartitionLbHolder.getNetworkPartitionId() + " of [Deployment Policy] " +
//                            deploymentPolicyId);
//
//                }
//                return false;
//            }
//
//        }
//
//        return true;
//
//    }
//
//    public String getServiceLBClusterId(String serviceType, String deploymentPolicyName) {
//
//        for (NetworkPartition networkPartition : PolicyManager.getInstance().getDeploymentPolicy(deploymentPolicyName).getChildLevelNetworkPartitions()) {
//
//            NetworkPartitionLbHolder nwPartitionLbHolder = partitionManager.getNetworkPartitionLbHolder(networkPartition.getId());
//
//            if (nwPartitionLbHolder.isServiceLBExist(serviceType)) {
//                if (log.isDebugEnabled()) {
//                    log.debug("Service LB [service name] " + serviceType + " does not exist in [network partition] " +
//                            nwPartitionLbHolder.getNetworkPartitionId() + " of [Deployment Policy] " +
//                            deploymentPolicyName);
//
//                }
//                return nwPartitionLbHolder.getLBClusterIdOfService(serviceType);
//            }
//
//        }
//
//        return null;
//    }

//    public boolean checkClusterLBExistenceAgainstPolicy(String clusterId, String deploymentPolicyId) {
//
//        for (NetworkPartition networkPartition : PolicyManager.getInstance().getDeploymentPolicy(deploymentPolicyId).getChildLevelNetworkPartitions()) {
//
//            NetworkPartitionLbHolder nwPartitionLbHolder = partitionManager.getNetworkPartitionLbHolder(networkPartition.getId());
//
//            if (!nwPartitionLbHolder.isClusterLBExist(clusterId)) {
//                if (log.isDebugEnabled()) {
//                    log.debug("Cluster LB [cluster id] " + clusterId + " does not exist in [network partition] " +
//                            nwPartitionLbHolder.getNetworkPartitionId() + " of [Deployment Policy] " +
//                            deploymentPolicyId);
//
//                }
//                return false;
//            }
//
//        }
//
//        return true;
//
//    }

    public void updateClusterMonitor(String clusterId, Properties properties) throws InvalidArgumentException {
        if (log.isDebugEnabled()) {
            log.debug(String.format("Updating Cluster monitor [Cluster id] %s ", clusterId));
        }
        AutoscalerContext asCtx = AutoscalerContext.getInstance();
        AbstractClusterMonitor monitor = asCtx.getClusterMonitor(clusterId);

        if (monitor != null) {
            monitor.handleDynamicUpdates(properties);
        } else {
            log.debug(String.format("Updating Cluster monitor failed: Cluster monitor [Cluster id] %s not found.",
                    clusterId));
        }
    }

    public void deployServiceGroup(ServiceGroup servicegroup) throws InvalidServiceGroupException {

        if (servicegroup == null || StringUtils.isEmpty(servicegroup.getName())) {
            String msg = "Service group can not be null service name can not be empty.";
            log.error(msg);
            throw new IllegalArgumentException(msg);

        }
        String name = servicegroup.getName();

        if (RegistryManager.getInstance().serviceGroupExist(name)) {
            throw new InvalidServiceGroupException("Service group with the name " + name + " already exist.");
        }

        if (log.isDebugEnabled()) {
            log.debug(MessageFormat.format("Deploying service group {0}", servicegroup.getName()));
        }

        String[] subGroups = servicegroup.getCartridges();

        if (log.isDebugEnabled()) {
            log.debug("SubGroups" + subGroups);
            if (subGroups != null) {
                log.debug("subGroups:size" + subGroups.length);
            } else {
                log.debug("subGroups: are null");
            }
        }


        Dependencies dependencies = servicegroup.getDependencies();

        if (log.isDebugEnabled()) {
            log.debug("Dependencies" + dependencies);
        }

        if (dependencies != null) {
            String[] startupOrders = dependencies.getStartupOrders();

            if (log.isDebugEnabled()) {
                log.debug("StartupOrders " + startupOrders);

                if (startupOrders != null) {
                    log.debug("StartupOrder:size  " + startupOrders.length);
                } else {
                    log.debug("StartupOrder: is null");
                }
            }
            String[] scalingOrders = dependencies.getScalingOrders();

            if (log.isDebugEnabled()) {
                log.debug("ScalingOrders " + scalingOrders);

                if (scalingOrders != null) {
                    log.debug("ScalingOrder:size " + scalingOrders.length);
                } else {
                    log.debug("ScalingOrder: is null");
                }
            }
        }

        RegistryManager.getInstance().persistServiceGroup(servicegroup);
    }

    public ServiceGroup getServiceGroup(String name) {
        if (StringUtils.isEmpty(name)) {
            return null;
        }
        try {
            return RegistryManager.getInstance().getServiceGroup(name);
        } catch (Exception e) {
            throw new AutoScalerException("Error occurred while retrieving service group", e);
        }
    }

    public ServiceGroup[] getServiceGroups() throws AutoScalerException {
        return RegistryManager.getInstance().getServiceGroups();
    }

    public boolean serviceGroupExist(String serviceName) {
        return false;
    }

    public void undeployServiceGroup(String name) throws AutoScalerException {
        try {
            RegistryManager.getInstance().removeServiceGroup(name);
        } catch (RegistryException e) {
            throw new AutoScalerException("Error occurred while removing the service groups", e);
        }

    }

    private void publishMetadata(ApplicationParser applicationParser, String appId) {
        MetaDataServiceClient metaDataServiceClien = null;
        try {
            metaDataServiceClien = new DefaultMetaDataServiceClient();
            for (Map.Entry<String, Properties> entry : applicationParser.getAliasToProperties().entrySet()) {
                String alias = entry.getKey();
                Properties properties = entry.getValue();
                if (properties != null) {
                    for (Property property : properties.getProperties()) {
                        metaDataServiceClien.addPropertyToCluster(appId, alias, property.getName(), property.getValue());
                    }
                }
            }
        } catch (MetaDataServiceClientException e) {
            log.error("Could not publish to metadata service ", e);
        }
    }
}
