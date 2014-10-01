package org.apache.stratos.metadataservice.listener;

import javax.servlet.ServletContextEvent;
import javax.servlet.ServletContextListener;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.stratos.messaging.event.Event;
import org.apache.stratos.messaging.event.topology.MemberStartedEvent;
import org.apache.stratos.messaging.event.topology.MemberSuspendedEvent;
import org.apache.stratos.messaging.event.topology.MemberTerminatedEvent;
import org.apache.stratos.messaging.listener.topology.MemberStartedEventListener;
import org.apache.stratos.messaging.listener.topology.MemberSuspendedEventListener;
import org.apache.stratos.messaging.listener.topology.MemberTerminatedEventListener;
import org.apache.stratos.messaging.message.receiver.topology.TopologyEventReceiver;
import org.apache.stratos.messaging.message.receiver.topology.TopologyManager;
import org.apache.stratos.metadataservice.services.MetaDataAdmin;

public class TopologyListener implements ServletContextListener {

	private static final Log log = LogFactory.getLog(TopologyListener.class);

	private TopologyAgent topologyThread = null;
	private Thread thread = null;

	@Override
	public void contextInitialized(ServletContextEvent arg0) {
		log.info("Topology literner started....");
		if (topologyThread == null) {
			// load default agent
			topologyThread = new TopologyAgent();
			if (log.isDebugEnabled()) {
				log.debug("Loading default Cartridge Agent.");
			}
		}

		thread = new Thread(topologyThread);
		thread.start();

	}

	@Override
	public void contextDestroyed(ServletContextEvent arg0) {
		thread.stop();
	}
    

}
