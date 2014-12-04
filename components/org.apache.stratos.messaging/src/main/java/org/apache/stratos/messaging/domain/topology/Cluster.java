/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

package org.apache.stratos.messaging.domain.topology;

import org.apache.commons.lang.StringUtils;
import org.apache.stratos.messaging.domain.instance.ClusterInstance;
import org.apache.stratos.messaging.util.Util;
import org.apache.stratos.messaging.util.bean.type.map.MapAdapter;

import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;
import java.io.Serializable;
import java.util.*;

/**
 * Defines a cluster of a service.
 * Key: serviceName, clusterId
 */
@XmlRootElement
public class Cluster implements Serializable {

    private static final long serialVersionUID = -361960242360176077L;

    private final String serviceName;
    private final String clusterId;
    private final String autoscalePolicyName;
    private final String deploymentPolicyName;

    private List<String> hostNames;
    private String tenantRange;
    private boolean isLbCluster;
    private boolean isKubernetesCluster; // TODO fix properly with an Enum
    // Key: Member.memberId
    @XmlJavaTypeAdapter(MapAdapter.class)
    private Map<String, Member> memberMap;

    //private ClusterStatus status;

    private String appId;

    private String parentId;

    private String loadBalanceAlgorithmName;
    @XmlJavaTypeAdapter(MapAdapter.class)
    private Properties properties;
    private Map<String, ClusterInstance> instanceIdToInstanceContextMap;
    //private LifeCycleStateManager<ClusterStatus> clusterStateManager;

    public Cluster(String serviceName, String clusterId, String deploymentPolicyName,
                   String autoscalePolicyName, String appId) {
        this.serviceName = serviceName;
        this.clusterId = clusterId;
        this.deploymentPolicyName = deploymentPolicyName;
        this.autoscalePolicyName = autoscalePolicyName;
        this.setHostNames(new ArrayList<String>());
        this.memberMap = new HashMap<String, Member>();
        this.appId = appId;
        this.setInstanceIdToInstanceContextMap(new HashMap<String, ClusterInstance>());
        //this.clusterStateManager = new LifeCycleStateManager<ClusterStatus>(ClusterStatus.Created, clusterId);
        // temporary; should be removed
        //this.status = ClusterStatus.Created;
    }

    public String getServiceName() {
        return serviceName;
    }

    public String getClusterId() {
        return clusterId;
    }

    public List<String> getHostNames() {
        return hostNames;
    }

    public void addHostName(String hostName) {
        this.hostNames.add(hostName);
    }

    public String getTenantRange() {
        return tenantRange;
    }

    public void setTenantRange(String tenantRange) {
        Util.validateTenantRange(tenantRange);
        this.tenantRange = tenantRange;
    }

    public Collection<Member> getMembers() {
        return memberMap.values();
    }

    public boolean hasMembers() {
        return memberMap.isEmpty();
    }


    public void addMember(Member member) {
        memberMap.put(member.getMemberId(), member);
    }

    public void removeMember(Member member) {
        memberMap.remove(member.getMemberId());
    }

    public Member getMember(String memberId) {
        return memberMap.get(memberId);
    }

    public boolean memberExists(String memberId) {
        return this.memberMap.containsKey(memberId);
    }

    public Properties getProperties() {
        return properties;
    }

    public void setProperties(Properties properties) {
        this.properties = properties;
    }

    public String getAutoscalePolicyName() {
        return autoscalePolicyName;
    }

    public String getDeploymentPolicyName() {
        return deploymentPolicyName;
    }

    public String getLoadBalanceAlgorithmName() {
        return loadBalanceAlgorithmName;
    }

    public void setLoadBalanceAlgorithmName(String loadBalanceAlgorithmName) {
        this.loadBalanceAlgorithmName = loadBalanceAlgorithmName;
    }

    public boolean isLbCluster() {
        return isLbCluster;
    }

    public void setLbCluster(boolean isLbCluster) {
        this.isLbCluster = isLbCluster;
    }
        
    public boolean isKubernetesCluster() {
		return isKubernetesCluster;
	}

	public void setKubernetesCluster(boolean isKubernetesCluster) {
		this.isKubernetesCluster = isKubernetesCluster;
	}

    /**
     * Check whether a given tenant id is in tenant range of the cluster.
     *
     * @param tenantId
     * @return
     */
    public boolean tenantIdInRange(int tenantId) {
        if (StringUtils.isEmpty(getTenantRange())) {
            return false;
        }

        if ("*".equals(getTenantRange())) {
            return true;
        } else {
            String[] array = getTenantRange().split("-");
            int tenantStart = Integer.parseInt(array[0]);
            if (tenantStart <= tenantId) {
                String tenantEndStr = array[1];
                if ("*".equals(tenantEndStr)) {
                    return true;
                } else {
                    int tenantEnd = Integer.parseInt(tenantEndStr);
                    if (tenantId <= tenantEnd) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    /**
     * Find partitions used by the cluster and return their ids as a collection.
     *
     * @return
     */
    public Collection<String> findPartitionIds() {
        Map<String, Boolean> partitionIds = new HashMap<String, Boolean>();
        for (Member member : getMembers()) {
            if ((StringUtils.isNotEmpty(member.getPartitionId())) && (!partitionIds.containsKey(member.getPartitionId()))) {
                partitionIds.put(member.getPartitionId(), true);
            }
        }
        return partitionIds.keySet();
    }

    public boolean isStateTransitionValid(ClusterStatus newState, String clusterInstanceId) {
        return getInstanceIdToInstanceContextMap().get(clusterInstanceId).isStateTransitionValid(newState);
    }

    public Stack<ClusterStatus> getTransitionedStates(String clusterInstanceId) {
        return getInstanceIdToInstanceContextMap().get(clusterInstanceId).getTransitionedStates();
    }

    public ClusterStatus getStatus(String applicationInstanceId) {
    	ClusterInstance clusterInstance = getInstanceIdToInstanceContextMap().get(applicationInstanceId);
    	if(clusterInstance != null) {
    		return clusterInstance.getStatus();
    	}
    	return null;
    }

    public boolean setStatus(ClusterStatus newStatus, String applicationInstanceId) {
        return getInstanceIdToInstanceContextMap().get(applicationInstanceId).setStatus(newStatus);
    }

    public void addInstanceContext (String instanceId, ClusterInstance instanceContext) {

        getInstanceIdToInstanceContextMap().put(instanceId, instanceContext);
    }

    public ClusterInstance getInstanceContexts (String instanceId) {
        // if map is empty, return null
        if (getInstanceIdToInstanceContextMap().isEmpty()) {
            return null;
        }

        // if instanceId is null, just get the first InstanceContext
        if (instanceId == null) {
            return getInstanceIdToInstanceContextMap().entrySet().iterator().next().getValue();
        }

        return getInstanceIdToInstanceContextMap().get(instanceId);
    }

    public int getInstanceContextCount () {

        return getInstanceIdToInstanceContextMap().keySet().size();
    }

    public boolean equals(Object other) {
        if (other == null || !(other instanceof Cluster)) {
            return false;
        }

        if (this == other) {
            return true;
        }

        Cluster that = (Cluster) other;
        return this.clusterId.equals(that.clusterId);
    }

    public int hashCode() {
        return clusterId.hashCode();
    }

    public String toString () {

        return " [ Cluster Id: " + clusterId + ", Service Name: " + serviceName + ", Autoscale Policy Name: "
                + autoscalePolicyName + ", Deployment Policy Name: " + deploymentPolicyName +
                ", Tenant Range: " + tenantRange + ", Is a Kubernetes Cluster: " + isKubernetesCluster + " ] ";
    }
    public String getAppId() {
        return appId;
    }

    public void setHostNames(List<String> hostNames) {
        this.hostNames = hostNames;
    }

    public String getParentId() {
        return parentId;
    }

    public void setParentId(String parentId) {
        this.parentId = parentId;
    }

    public Map<String, ClusterInstance> getInstanceIdToInstanceContextMap() {
        return instanceIdToInstanceContextMap;
    }

    public void setInstanceIdToInstanceContextMap(Map<String, ClusterInstance> instanceIdToInstanceContextMap) {
        this.instanceIdToInstanceContextMap = instanceIdToInstanceContextMap;
    }

    public Collection<ClusterInstance> getClusterInstances() {
        return this.instanceIdToInstanceContextMap.values();
    }
//    public ClusterStatus getTempStatus() {
//        return status;
//    }
//
//    public void setTempStatus(ClusterStatus status) {
//        this.status = status;
//    }
}

