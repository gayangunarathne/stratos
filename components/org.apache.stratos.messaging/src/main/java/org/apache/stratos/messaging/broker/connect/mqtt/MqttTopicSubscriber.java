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

package org.apache.stratos.messaging.broker.connect.mqtt;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.stratos.messaging.broker.connect.TopicConnector;
import org.apache.stratos.messaging.broker.connect.TopicSubscriber;
import org.apache.stratos.messaging.broker.subscribe.MessageListener;
import org.apache.stratos.messaging.domain.Message;
import org.apache.stratos.messaging.domain.exception.MessagingException;
import org.apache.stratos.messaging.util.Util;
import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class MqttTopicSubscriber extends MqttTopicConnector implements TopicSubscriber {

    protected static final Log log = LogFactory.getLog(MqttTopicSubscriber.class);

    private final MessageListener messageListener;
    private String topicName;

    public MqttTopicSubscriber(MessageListener messageListener, String topicName) {
        this.messageListener = messageListener;
        this.topicName = topicName;
        create();
    }

    /**
     * Return server URI.
     * @return
     */
    @Override
    public String getServerURI() {
        return mqttClient.getServerURI();
    }

    /**
     * Connect to message broker using MQTT client object created.
     */
    @Override
    public void connect() {
        try {
            if (log.isDebugEnabled()) {
                log.debug("Connecting to message broker");
            }

            if(mqttClient == null) {
                if(log.isWarnEnabled()) {
                    log.warn("Could not connect to message broker, MQTT client has not been initialized");
                }
                return;
            }

            MqttConnectOptions connectOptions = new MqttConnectOptions();
            // Do not maintain a session between the client and the server since it is nearly impossible to
            // generate a unique client id for each subscriber & publisher with the distributed nature of stratos.
            // Reliable message delivery is managed by topic subscriber and publisher.
            connectOptions.setCleanSession(true);
            // TODO: test this
            // set the keep alive interval less than MB's inactive connection detection time
            //connectOptions.setKeepAliveInterval(15);
            mqttClient.connect(connectOptions);
        } catch (Exception e) {
            String message = "Could not connect to message broker";
            log.error(message, e);
            throw new MessagingException(message, e);
        }
    }

    /**
     * Subscribe to topic.
     */
    @Override
    public void subscribe() {
        try {
            if (log.isDebugEnabled()) {
                log.debug("Subscribing to topic " + topicName);
            }

            if(mqttClient == null) {
                if(log.isWarnEnabled()) {
                    log.warn("Could not subscribe to topic, MQTT client has not been initialized");
                }
                return;
            }

            mqttClient.setCallback(new MQTTSubscriberCallback());
            mqttClient.subscribe(topicName, MqttConstants.QOS);
            if (log.isDebugEnabled()) {
                log.debug("Subscribed to topic " + topicName);
            }

        } catch (Exception e) {
            String errorMsg = "Error in subscribing to topic "  + topicName;
            log.error(errorMsg, e);
        }
    }

    /**
     * Disconnect from message broker and close the connection.
     */
    @Override
    public void disconnect() {
        try {
            if (log.isDebugEnabled()) {
                log.debug("Disconnecting from message broker");
            }

            if(mqttClient == null) {
                if(log.isWarnEnabled()) {
                    log.warn("Could not disconnect from message broker, MQTT client has not been initialized");
                }
                return;
            }

            synchronized (mqttClient) {
                if (mqttClient.isConnected()) {
                    mqttClient.disconnect();
                }
                closeConnection();
            }
        } catch (Exception e) {
            String errorMsg = "Error in disconnecting from Message Broker";
            log.error(errorMsg, e);
        }
    }

    private void closeConnection () {
        try {
            if (log.isDebugEnabled()) {
                log.debug("Closing connection to message broker");
            }

            if(mqttClient == null) {
                if(log.isWarnEnabled()) {
                    log.warn("Could not close connection, MQTT client has not been initialized");
                }
                return;
            }

            mqttClient.close();
        } catch (Exception e) {
            String message = "Could not close MQTT client";
            log.error(message, e);
        } finally {
            mqttClient = null;
        }
    }

    private class MQTTSubscriberCallback implements MqttCallback {

        @Override
        public synchronized void connectionLost(Throwable cause) {
            if(log.isWarnEnabled()) {
                log.warn("MQTT Connection is lost, topic: " + topicName, cause);
            }
            if (mqttClient.isConnected()) {
                if(log.isDebugEnabled()){
                    log.debug("MQTT client is already re-connected");
                }
                return;
            }
            if(log.isInfoEnabled()) {
                log.info("Reconnection initiated for topic " + topicName);
            }

            create();
            connect();
            subscribe();

            if(log.isInfoEnabled()) {
                log.info("Re-connected and subscribed to the topic " + topicName);
            }
        }

        @Override
        public void messageArrived(String topic, MqttMessage message) throws Exception {

            String messageText = new String(message.getPayload());
            if (log.isDebugEnabled()) {
                log.debug(String.format("Message received: %s", messageText));
            }
            messageListener.messageReceived(new Message(topic, messageText));
        }

        @Override
        public void deliveryComplete(IMqttDeliveryToken deliveryToken) {
            if (log.isDebugEnabled()) {
                log.debug(String.format("Message delivery is complete: %s",
                        ((deliveryToken != null) ? deliveryToken.toString() : "")));
            }
        }
    }
}
