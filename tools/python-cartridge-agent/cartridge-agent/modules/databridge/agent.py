from thrift.publisher import *
import logging


class StreamDefinition:
    """
    Represents a BAM/CEP stream definition
    """
    def __init__(self):
        self.name = None
        """:type : str"""
        self.version = None
        """:type : str"""
        self.nickname = None
        """:type : str"""
        self.description = None
        """:type : str"""
        self.meta_data = []
        """:type : list[str]"""
        self.correlation_data = []
        """:type : list[str]"""
        self.payload_data = []
        """:type : list[str]"""

    def add_metadata_attribute(self, name, type):
        self.meta_data.append({"name": name, "type": type})

    def add_payloaddata_attribute(self, name, type):
        self.payload_data.append({"name": name, "type": type})

    def add_correlationdata_attribute(self, name, type):
        self.correlation_data.append({"name": name, "type": type})

    def __str__(self):
        """
        To string override
        """

        json_str = "{"
        json_str += "\"name\":\"" + self.name + "\","
        json_str += "\"version\":\"" + self.version + "\","
        json_str += "\"nickName\":\"" + self.nickname + "\","
        json_str += "\"description\":\"" + self.description + "\","

        # add metadata attributes if exists
        if len(self.meta_data > 0):
            json_str += "\"metaData\":["
            for metadatum in self.meta_data:
                json_str += "{\"name\":\"" + metadatum["name"] + ", \"type\": \"" + metadatum["type"] + "\"},"

            json_str = json_str[:-1] + "],"

        # add correlationdata attributes if exists
        if len(self.correlation_data > 0):
            json_str += "\"correlationData\":["
            for coredatum in self.correlation_data:
                json_str += "{\"name\":\"" + coredatum["name"] + ", \"type\": \"" + coredatum["type"] + "\"},"

            json_str = json_str[:-1] + "],"

        # add payloaddata attributes if exists
        if len(self.payload_data > 0):
            json_str += "\"payloadData\":["
            for payloaddatum in self.payload_data:
                json_str += "{\"name\":\"" + payloaddatum["name"] + ", \"type\": \"" + payloaddatum["type"] + "\"},"

            json_str = json_str[:-1] + "],"

        json_str = json_str[:-1] + "}"

        return json_str


class LogEvent:
    """
    Represents an event to be published to a BAM/CEP monitoring server
    """
    def __init__(self):
        self.metaData = []
        """:type : list[str]"""
        self.correlationData = []
        """:type : list[str]"""
        self.payloadData = []
        """:type : list[str]"""


class ThriftPublisher:
    """
    Handles publishing events to BAM/CEP through thrift using the provided address and credentials
    """
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)

    def __init__(self, ip, port, username, password, stream_definition):
        """
        Initializes a ThriftPublisher object.

        At initialization a ThriftPublisher connects and defines a stream definition. A connection
        should be disconnected after all the publishing has been done.

        :param str ip: IP address of the monitoring server
        :param str port: Port of the monitoring server
        :param str username: Username
        :param str password: Password
        :param StreamDefinition stream_definition: StreamDefinition object for this particular connection
        :return: ThriftPublisher object
        :rtype: ThriftPublisher
        """
        self.__publisher = Publisher(ip, port)
        self.__publisher.connect(username, password)
        self.__publisher.defineStream(str(stream_definition))

    def publish(self, event):
        """
        Publishes the given event by creating the event bundle from the log event

        :param LogEvent event: The log event to be published
        :return: void
        """
        event_bundler = EventBundle()
        ThriftPublisher.assign_attributes(event.metaData, event_bundler)
        ThriftPublisher.assign_attributes(event.correlationData, event_bundler)
        ThriftPublisher.assign_attributes(event.payloadData, event_bundler)

        self.__publisher.publish(event)

    def disconnect(self):
        """
        Disconnect the thrift publisher
        :return: void
        """
        self.__publisher.disconnect()

    @staticmethod
    def assign_attributes(attributes, event_bundler):
        """
        Adds the given attributes to the given event bundler according to type of each attribute
        :param list attributes: attributes to be assigned
        :param EventBundle event_bundler: Event bundle to assign attributes to
        :return: void
        """

        # __intAttributeList = []
        # __longAttributeList = []
        # __doubleAttributeList = []
        # __boolAttributeList = []
        # __stringAttributeList = []

        if attributes is not None and len(attributes) > 0:
            for attrib in attributes:
                if isinstance(attrib, int):
                    event_bundler.addIntAttribute(attrib)
                elif isinstance(attrib, long):
                    event_bundler.addLongAttribute(attrib)
                elif isinstance(attrib, float):
                    event_bundler.addDoubleAttribute(attrib)
                elif isinstance(attrib, bool):
                    event_bundler.addBoolAttribute(attrib)
                elif isinstance(attrib, str):
                    event_bundler.addStringAttribute(attrib)
                else:
                    ThriftPublisher.log.error("Undefined attribute type: %r" % attrib)

        ThriftPublisher.log.debug("Empty attribute list")
