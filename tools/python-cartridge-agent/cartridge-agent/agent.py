#!/usr/bin/env python
import stomp
import time
import logging
import sys
import random
import os
import threading
import socket
import json
import extensionhandler
import util
import subprocess
import ConfigParser
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


def readProperty(property):
    """
        Read provided property from the properties file
    """
    return properties.get("agent", property)


def runningSuspendScript():
    print "inside thread"
    os.system('./script.sh')


def MyThread2():
    pass


def listeningTopology():
    class MyListener(stomp.ConnectionListener):
        def on_error(self, headers, message):
            print('received an error %s' % message)

        def on_message(self, headers, message):
            # print('received message\n %s'% message)
            for k, v in headers.iteritems():
                print('header: key %s , value %s' % (k, v))

                if k == 'event-class-name':
                    print('event class name found')
                    if v == 'org.apache.stratos.messaging.event.topology.CompleteTopologyEvent':
                        print('CompleteTopologyEvent triggered')
                        print('received message\n %s' % message)
                    if v == 'org.apache.stratos.messaging.event.topology.MemberTerminatedEvent':
                        print('MemberTerminatedEvent triggered')
                    if v == 'org.apache.stratos.messaging.event.topology.ServiceCreatedEvent':
                        print('MemberTerminatedEvent triggered')
                    if v == 'org.apache.stratos.messaging.event.topology.InstanceSpawnedEvent':
                        print('MemberTerminatedEvent triggered')
                        print('received message\n %s' % message)
                    if v == 'org.apache.stratos.messaging.event.topology.ClusterCreatedEvent':
                        print('MemberTerminatedEvent triggered')
                    if v == 'org.apache.stratos.messaging.event.topology.InstanceSpawnedEvent':
                        print('MemberTerminatedEvent triggered')
                    else:
                        print('something else')


    dest = '/topic/topology'
    conn = stomp.Connection([('localhost', 61613)])
    print('set up Connection')
    conn.set_listener('somename', MyListener())
    print('Set up listener')

    conn.start()
    print('started connection')

    conn.connect(wait=True)
    print('connected')
    conn.subscribe(destination=dest, ack='auto')
    print('subscribed')


def listeningInstanceNotifier():
    instance_topic_client.on_connect = instance_notifier_connect
    instance_topic_client.on_message = instance_notifier_message

    # mb_client.connect(readProperty("mb.ip"), properties.get("agent", "mb.port"), 60)
    instance_topic_client.connect("127.0.0.1", 1883, 60)
    instance_topic_client.loop_forever()


def instance_notifier_connect(client, userdata, flags, rc):
    print "Connected! Subscribing to instance/# topics"
    instance_topic_client.subscribe("instance/#")


def artifact_updated(msg):
    extensionhandler.onArtifactUpdatedEvent(extensionsDir, 'artifacts-updated.sh')


def instance_cleanup_member(msg):
    # if sd['MEMBER_ID'] == member_id_from_event:
    extensionhandler.onInstanceCleanupMemberEvent(extensionsDir, 'clean.sh')


def instance_cleanup_cluster(msg):
    # if cluster_id == cluster_id_from_event:
    extensionhandler.onInstanceCleanupMemberEvent(extensionsDir, 'clean.sh')


def instance_notifier_message(client, userdata, msg):
    print "Topic: %r\nContent:%r" % (msg.topic, msg.payload)
    event = msg.topic.rpartition('/')[2]
    print "Event: %r" % event
    if event == "ArtifactUpdatedEvent":
        # TODO: event details to be passed to the script
        print "ArtifactUpdatedEvent received"
        artifact_updated(msg)
    elif event == "InstanceCleanupMemberEvent":
        print "InstanceCleanupMemberEvent received"
        # TODO: event details to be passed to the script
        instance_cleanup_member(msg)
    elif event == "InstanceCleanupClusterEvent":
        print "InstanceCleanupClusterEvent received"
        # TODO: event details to be passed to the script
        instance_cleanup_cluster(msg)
    else:
        print "Unidentified event: %r" % event


def publishInstanceStartedEvent():
    instance_started_event = InstanceStartedEvent(service_name, cluster_id, sd['NETWORK_PARTITION_ID'],
                                                  sd['PARTITION_ID'], sd['MEMBER_ID'])
    msgs = [{'topic': "instance/status/InstanceStartedEvent", 'payload': instance_started_event.to_JSON()}]
    #publish.single("instance", instance_started_event.to_JSON(), hostname="localhost", port=1883)
    publish.multiple(msgs, "localhost", 1883)


def checkPortsActive():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 80))
    if result == 0:
        print "Port is open"
    else:
        print "Port is not open"


class InstanceStartedEvent:
    serviceName = ''

    def __init__(self, serviceName, clusterId, networkPartitionId, partitionId, memberId):
        self.serviceName = serviceName
        self.clusterId = clusterId
        self.networkPartitionId = networkPartitionId
        self.partitionId = partitionId
        self.memberId = memberId

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def onInstanceStartedEvent():
    print('on instance start up event')
    event = InstanceStartedEvent(service_name, cluster_id, '', '', tenant_id)
    print(event.to_JSON())


def onArtifactUpdatedEvent():
    print('on srtifcats update event')

# Parse properties file
properties = ConfigParser.SafeConfigParser()
properties.read('agent.properties')

# TODO: check from properties file
util.validateRequiredSystemProperties()

payloadPath = sys.argv[1]
extensionsDir = sys.argv[2]
extensionhandler.onArtifactUpdatedEvent(extensionsDir, 'artifacts-updated.sh')

fo = open(payloadPath, "r+")
str = fo.read(1000);

print "Read String is : ", str

sd = dict(u.split("=") for u in str.split(","))

print [i for i in sd.keys()]

print "HOST_NAME   ", sd['HOST_NAME']

hostname = sd['HOST_NAME']
service_name = sd['SERVICE_NAME']
multitenant = sd['MULTITENANT']
tenant_id = sd['TENANT_ID']
tenantrange = sd['TENANT_RANGE']
cartridealies = sd['CARTRIDGE_ALIAS']
cluster_id = sd['CLUSTER_ID']
cartridge_key = sd['CARTRIDGE_KEY']
deployement = sd['DEPLOYMENT']
repourl = sd['REPO_URL']
ports = sd['PORTS']
puppetip = sd['PUPPET_IP']
puppethostname = sd['PUPPET_HOSTNAME']
puppetenv = sd['PUPPET_ENV']
persistance_mapping = sd['PERSISTENCE_MAPPING'] if 'PERSISTENCE_MAPPING' in sd else None

if 'COMMIT_ENABLED' in sd:
    commitenabled = sd['COMMIT_ENABLED']

if 'DB_HOST' in sd:
    dbhost = sd['DB_HOST']

if multitenant == "true":
    app_path = sd['APP_PATH']
else:
    app_path = ""

instance_topic_client = mqtt.Client()

env_params = {}
env_params['STRATOS_APP_PATH'] = app_path
env_params['STRATOS_PARAM_FILE_PATH'] = readProperty("param.file.path")
env_params['STRATOS_SERVICE_NAME'] = service_name
env_params['STRATOS_TENANT_ID'] = tenant_id
env_params['STRATOS_CARTRIDGE_KEY'] = cartridge_key
env_params['STRATOS_LB_CLUSTER_ID'] = sd['LB_CLUSTER_ID']
env_params['STRATOS_CLUSTER_ID'] = cluster_id
env_params['STRATOS_NETWORK_PARTITION_ID'] = sd['NETWORK_PARTITION_ID']
env_params['STRATOS_PARTITION_ID'] = sd['PARTITION_ID']
env_params['STRATOS_PERSISTENCE_MAPPINGS'] = persistance_mapping
env_params['STRATOS_REPO_URL'] = sd['REPO_URL']
# envParams['STRATOS_LB_IP']=
# envParams['STRATOS_LB_PUBLIC_IP']=
# envParams['']=
# envParams['']=
# envParams['']=
# envParams['']=

extensionhandler.onInstanceStartedEvent(extensionsDir, 'instance-started.sh', multitenant, 'artifacts-copy.sh.erb',
                                        app_path, env_params)

t1 = threading.Thread(target=runningSuspendScript, args=[])

t1.start()

t2 = threading.Thread(target=listeningInstanceNotifier, args=[])

t2.start()

t3 = threading.Thread(target=listeningTopology, args=[])

t3.start()

onInstanceStartedEvent()

checkPortsActive()

publishInstanceStartedEvent()

extensionhandler.startServerExtension()


def git(*args):
    return subprocess.check_call(['git'] + list(args))

# examples
git("status")
git("clone", "git://git.xyz.com/platform/manifest.git", "-b", "jb_2.5")





