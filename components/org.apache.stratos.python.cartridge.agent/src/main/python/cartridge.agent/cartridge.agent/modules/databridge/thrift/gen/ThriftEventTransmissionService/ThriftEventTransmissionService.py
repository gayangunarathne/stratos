# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from ttypes import *
from ...thrift.Thrift import TProcessor
from ...thrift.transport import TTransport

try:
  from ...thrift.protocol import fastbinary
except:
  fastbinary = None


class Iface:
  def defineStream(self, sessionId, streamDefinition):
    """
    Parameters:
     - sessionId
     - streamDefinition
    """
    pass

  def findStreamId(self, sessionId, streamName, streamVersion):
    """
    Parameters:
     - sessionId
     - streamName
     - streamVersion
    """
    pass

  def publish(self, eventBundle):
    """
    Parameters:
     - eventBundle
    """
    pass

  def deleteStreamById(self, sessionId, streamId):
    """
    Parameters:
     - sessionId
     - streamId
    """
    pass

  def deleteStreamByNameVersion(self, sessionId, streamName, streamVersion):
    """
    Parameters:
     - sessionId
     - streamName
     - streamVersion
    """
    pass


class Client(Iface):
  def __init__(self, iprot, oprot=None):
    self._iprot = self._oprot = iprot
    if oprot is not None:
      self._oprot = oprot
    self._seqid = 0

  def defineStream(self, sessionId, streamDefinition):
    """
    Parameters:
     - sessionId
     - streamDefinition
    """
    self.send_defineStream(sessionId, streamDefinition)
    return self.recv_defineStream()

  def send_defineStream(self, sessionId, streamDefinition):
    self._oprot.writeMessageBegin('defineStream', TMessageType.CALL, self._seqid)
    args = defineStream_args()
    args.sessionId = sessionId
    args.streamDefinition = streamDefinition
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_defineStream(self):
    (fname, mtype, rseqid) = self._iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(self._iprot)
      self._iprot.readMessageEnd()
      raise x
    result = defineStream_result()
    result.read(self._iprot)
    self._iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    if result.ade is not None:
      raise result.ade
    if result.mtd is not None:
      raise result.mtd
    if result.tde is not None:
      raise result.tde
    if result.se is not None:
      raise result.se
    raise TApplicationException(TApplicationException.MISSING_RESULT, "defineStream failed: unknown result");

  def findStreamId(self, sessionId, streamName, streamVersion):
    """
    Parameters:
     - sessionId
     - streamName
     - streamVersion
    """
    self.send_findStreamId(sessionId, streamName, streamVersion)
    return self.recv_findStreamId()

  def send_findStreamId(self, sessionId, streamName, streamVersion):
    self._oprot.writeMessageBegin('findStreamId', TMessageType.CALL, self._seqid)
    args = findStreamId_args()
    args.sessionId = sessionId
    args.streamName = streamName
    args.streamVersion = streamVersion
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_findStreamId(self):
    (fname, mtype, rseqid) = self._iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(self._iprot)
      self._iprot.readMessageEnd()
      raise x
    result = findStreamId_result()
    result.read(self._iprot)
    self._iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    if result.tnde is not None:
      raise result.tnde
    if result.se is not None:
      raise result.se
    raise TApplicationException(TApplicationException.MISSING_RESULT, "findStreamId failed: unknown result");

  def publish(self, eventBundle):
    """
    Parameters:
     - eventBundle
    """
    self.send_publish(eventBundle)
    self.recv_publish()

  def send_publish(self, eventBundle):
    self._oprot.writeMessageBegin('publish', TMessageType.CALL, self._seqid)
    args = publish_args()
    args.eventBundle = eventBundle
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_publish(self):
    (fname, mtype, rseqid) = self._iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(self._iprot)
      self._iprot.readMessageEnd()
      raise x
    result = publish_result()
    result.read(self._iprot)
    self._iprot.readMessageEnd()
    if result.ue is not None:
      raise result.ue
    if result.se is not None:
      raise result.se
    return

  def deleteStreamById(self, sessionId, streamId):
    """
    Parameters:
     - sessionId
     - streamId
    """
    self.send_deleteStreamById(sessionId, streamId)
    return self.recv_deleteStreamById()

  def send_deleteStreamById(self, sessionId, streamId):
    self._oprot.writeMessageBegin('deleteStreamById', TMessageType.CALL, self._seqid)
    args = deleteStreamById_args()
    args.sessionId = sessionId
    args.streamId = streamId
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_deleteStreamById(self):
    (fname, mtype, rseqid) = self._iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(self._iprot)
      self._iprot.readMessageEnd()
      raise x
    result = deleteStreamById_result()
    result.read(self._iprot)
    self._iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    if result.se is not None:
      raise result.se
    raise TApplicationException(TApplicationException.MISSING_RESULT, "deleteStreamById failed: unknown result");

  def deleteStreamByNameVersion(self, sessionId, streamName, streamVersion):
    """
    Parameters:
     - sessionId
     - streamName
     - streamVersion
    """
    self.send_deleteStreamByNameVersion(sessionId, streamName, streamVersion)
    return self.recv_deleteStreamByNameVersion()

  def send_deleteStreamByNameVersion(self, sessionId, streamName, streamVersion):
    self._oprot.writeMessageBegin('deleteStreamByNameVersion', TMessageType.CALL, self._seqid)
    args = deleteStreamByNameVersion_args()
    args.sessionId = sessionId
    args.streamName = streamName
    args.streamVersion = streamVersion
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

  def recv_deleteStreamByNameVersion(self):
    (fname, mtype, rseqid) = self._iprot.readMessageBegin()
    if mtype == TMessageType.EXCEPTION:
      x = TApplicationException()
      x.read(self._iprot)
      self._iprot.readMessageEnd()
      raise x
    result = deleteStreamByNameVersion_result()
    result.read(self._iprot)
    self._iprot.readMessageEnd()
    if result.success is not None:
      return result.success
    if result.se is not None:
      raise result.se
    raise TApplicationException(TApplicationException.MISSING_RESULT, "deleteStreamByNameVersion failed: unknown result");


class Processor(Iface, TProcessor):
  def __init__(self, handler):
    self._handler = handler
    self._processMap = {}
    self._processMap["defineStream"] = Processor.process_defineStream
    self._processMap["findStreamId"] = Processor.process_findStreamId
    self._processMap["publish"] = Processor.process_publish
    self._processMap["deleteStreamById"] = Processor.process_deleteStreamById
    self._processMap["deleteStreamByNameVersion"] = Processor.process_deleteStreamByNameVersion

  def process(self, iprot, oprot):
    (name, type, seqid) = iprot.readMessageBegin()
    if name not in self._processMap:
      iprot.skip(TType.STRUCT)
      iprot.readMessageEnd()
      x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
      oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
      x.write(oprot)
      oprot.writeMessageEnd()
      oprot.trans.flush()
      return
    else:
      self._processMap[name](self, seqid, iprot, oprot)
    return True

  def process_defineStream(self, seqid, iprot, oprot):
    args = defineStream_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = defineStream_result()
    try:
      result.success = self._handler.defineStream(args.sessionId, args.streamDefinition)
    except Exception.ttypes.ThriftDifferentStreamDefinitionAlreadyDefinedException, ade:
      result.ade = ade
    except Exception.ttypes.ThriftMalformedStreamDefinitionException, mtd:
      result.mtd = mtd
    except Exception.ttypes.ThriftStreamDefinitionException, tde:
      result.tde = tde
    except Exception.ttypes.ThriftSessionExpiredException, se:
      result.se = se
    oprot.writeMessageBegin("defineStream", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def process_findStreamId(self, seqid, iprot, oprot):
    args = findStreamId_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = findStreamId_result()
    try:
      result.success = self._handler.findStreamId(args.sessionId, args.streamName, args.streamVersion)
    except Exception.ttypes.ThriftNoStreamDefinitionExistException, tnde:
      result.tnde = tnde
    except Exception.ttypes.ThriftSessionExpiredException, se:
      result.se = se
    oprot.writeMessageBegin("findStreamId", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def process_publish(self, seqid, iprot, oprot):
    args = publish_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = publish_result()
    try:
      self._handler.publish(args.eventBundle)
    except Exception.ttypes.ThriftUndefinedEventTypeException, ue:
      result.ue = ue
    except Exception.ttypes.ThriftSessionExpiredException, se:
      result.se = se
    oprot.writeMessageBegin("publish", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def process_deleteStreamById(self, seqid, iprot, oprot):
    args = deleteStreamById_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = deleteStreamById_result()
    try:
      result.success = self._handler.deleteStreamById(args.sessionId, args.streamId)
    except Exception.ttypes.ThriftSessionExpiredException, se:
      result.se = se
    oprot.writeMessageBegin("deleteStreamById", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()

  def process_deleteStreamByNameVersion(self, seqid, iprot, oprot):
    args = deleteStreamByNameVersion_args()
    args.read(iprot)
    iprot.readMessageEnd()
    result = deleteStreamByNameVersion_result()
    try:
      result.success = self._handler.deleteStreamByNameVersion(args.sessionId, args.streamName, args.streamVersion)
    except Exception.ttypes.ThriftSessionExpiredException, se:
      result.se = se
    oprot.writeMessageBegin("deleteStreamByNameVersion", TMessageType.REPLY, seqid)
    result.write(oprot)
    oprot.writeMessageEnd()
    oprot.trans.flush()


# HELPER FUNCTIONS AND STRUCTURES

class defineStream_args:
  """
  Attributes:
   - sessionId
   - streamDefinition
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'sessionId', None, None, ), # 1
    (2, TType.STRING, 'streamDefinition', None, None, ), # 2
  )

  def __init__(self, sessionId=None, streamDefinition=None,):
    self.sessionId = sessionId
    self.streamDefinition = streamDefinition

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.sessionId = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.streamDefinition = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('defineStream_args')
    if self.sessionId is not None:
      oprot.writeFieldBegin('sessionId', TType.STRING, 1)
      oprot.writeString(self.sessionId)
      oprot.writeFieldEnd()
    if self.streamDefinition is not None:
      oprot.writeFieldBegin('streamDefinition', TType.STRING, 2)
      oprot.writeString(self.streamDefinition)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class defineStream_result:
  """
  Attributes:
   - success
   - ade
   - mtd
   - tde
   - se
  """

  thrift_spec = (
    (0, TType.STRING, 'success', None, None, ), # 0
    (1, TType.STRUCT, 'ade', (Exception.ttypes.ThriftDifferentStreamDefinitionAlreadyDefinedException, Exception.ttypes.ThriftDifferentStreamDefinitionAlreadyDefinedException.thrift_spec), None, ), # 1
    (2, TType.STRUCT, 'mtd', (Exception.ttypes.ThriftMalformedStreamDefinitionException, Exception.ttypes.ThriftMalformedStreamDefinitionException.thrift_spec), None, ), # 2
    (3, TType.STRUCT, 'tde', (Exception.ttypes.ThriftStreamDefinitionException, Exception.ttypes.ThriftStreamDefinitionException.thrift_spec), None, ), # 3
    (4, TType.STRUCT, 'se', (Exception.ttypes.ThriftSessionExpiredException, Exception.ttypes.ThriftSessionExpiredException.thrift_spec), None, ), # 4
  )

  def __init__(self, success=None, ade=None, mtd=None, tde=None, se=None,):
    self.success = success
    self.ade = ade
    self.mtd = mtd
    self.tde = tde
    self.se = se

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.STRING:
          self.success = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 1:
        if ftype == TType.STRUCT:
          self.ade = Exception.ttypes.ThriftDifferentStreamDefinitionAlreadyDefinedException()
          self.ade.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRUCT:
          self.mtd = Exception.ttypes.ThriftMalformedStreamDefinitionException()
          self.mtd.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRUCT:
          self.tde = Exception.ttypes.ThriftStreamDefinitionException()
          self.tde.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRUCT:
          self.se = Exception.ttypes.ThriftSessionExpiredException()
          self.se.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('defineStream_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.STRING, 0)
      oprot.writeString(self.success)
      oprot.writeFieldEnd()
    if self.ade is not None:
      oprot.writeFieldBegin('ade', TType.STRUCT, 1)
      self.ade.write(oprot)
      oprot.writeFieldEnd()
    if self.mtd is not None:
      oprot.writeFieldBegin('mtd', TType.STRUCT, 2)
      self.mtd.write(oprot)
      oprot.writeFieldEnd()
    if self.tde is not None:
      oprot.writeFieldBegin('tde', TType.STRUCT, 3)
      self.tde.write(oprot)
      oprot.writeFieldEnd()
    if self.se is not None:
      oprot.writeFieldBegin('se', TType.STRUCT, 4)
      self.se.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class findStreamId_args:
  """
  Attributes:
   - sessionId
   - streamName
   - streamVersion
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'sessionId', None, None, ), # 1
    (2, TType.STRING, 'streamName', None, None, ), # 2
    (3, TType.STRING, 'streamVersion', None, None, ), # 3
  )

  def __init__(self, sessionId=None, streamName=None, streamVersion=None,):
    self.sessionId = sessionId
    self.streamName = streamName
    self.streamVersion = streamVersion

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.sessionId = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.streamName = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.streamVersion = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('findStreamId_args')
    if self.sessionId is not None:
      oprot.writeFieldBegin('sessionId', TType.STRING, 1)
      oprot.writeString(self.sessionId)
      oprot.writeFieldEnd()
    if self.streamName is not None:
      oprot.writeFieldBegin('streamName', TType.STRING, 2)
      oprot.writeString(self.streamName)
      oprot.writeFieldEnd()
    if self.streamVersion is not None:
      oprot.writeFieldBegin('streamVersion', TType.STRING, 3)
      oprot.writeString(self.streamVersion)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class findStreamId_result:
  """
  Attributes:
   - success
   - tnde
   - se
  """

  thrift_spec = (
    (0, TType.STRING, 'success', None, None, ), # 0
    (1, TType.STRUCT, 'tnde', (Exception.ttypes.ThriftNoStreamDefinitionExistException, Exception.ttypes.ThriftNoStreamDefinitionExistException.thrift_spec), None, ), # 1
    (2, TType.STRUCT, 'se', (Exception.ttypes.ThriftSessionExpiredException, Exception.ttypes.ThriftSessionExpiredException.thrift_spec), None, ), # 2
  )

  def __init__(self, success=None, tnde=None, se=None,):
    self.success = success
    self.tnde = tnde
    self.se = se

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.STRING:
          self.success = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 1:
        if ftype == TType.STRUCT:
          self.tnde = Exception.ttypes.ThriftNoStreamDefinitionExistException()
          self.tnde.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRUCT:
          self.se = Exception.ttypes.ThriftSessionExpiredException()
          self.se.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('findStreamId_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.STRING, 0)
      oprot.writeString(self.success)
      oprot.writeFieldEnd()
    if self.tnde is not None:
      oprot.writeFieldBegin('tnde', TType.STRUCT, 1)
      self.tnde.write(oprot)
      oprot.writeFieldEnd()
    if self.se is not None:
      oprot.writeFieldBegin('se', TType.STRUCT, 2)
      self.se.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class publish_args:
  """
  Attributes:
   - eventBundle
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRUCT, 'eventBundle', (Data.ttypes.ThriftEventBundle, Data.ttypes.ThriftEventBundle.thrift_spec), None, ), # 1
  )

  def __init__(self, eventBundle=None,):
    self.eventBundle = eventBundle

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRUCT:
          self.eventBundle = Data.ttypes.ThriftEventBundle()
          self.eventBundle.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('publish_args')
    if self.eventBundle is not None:
      oprot.writeFieldBegin('eventBundle', TType.STRUCT, 1)
      self.eventBundle.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class publish_result:
  """
  Attributes:
   - ue
   - se
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRUCT, 'ue', (Exception.ttypes.ThriftUndefinedEventTypeException, Exception.ttypes.ThriftUndefinedEventTypeException.thrift_spec), None, ), # 1
    (2, TType.STRUCT, 'se', (Exception.ttypes.ThriftSessionExpiredException, Exception.ttypes.ThriftSessionExpiredException.thrift_spec), None, ), # 2
  )

  def __init__(self, ue=None, se=None,):
    self.ue = ue
    self.se = se

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRUCT:
          self.ue = Exception.ttypes.ThriftUndefinedEventTypeException()
          self.ue.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRUCT:
          self.se = Exception.ttypes.ThriftSessionExpiredException()
          self.se.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('publish_result')
    if self.ue is not None:
      oprot.writeFieldBegin('ue', TType.STRUCT, 1)
      self.ue.write(oprot)
      oprot.writeFieldEnd()
    if self.se is not None:
      oprot.writeFieldBegin('se', TType.STRUCT, 2)
      self.se.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class deleteStreamById_args:
  """
  Attributes:
   - sessionId
   - streamId
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'sessionId', None, None, ), # 1
    (2, TType.STRING, 'streamId', None, None, ), # 2
  )

  def __init__(self, sessionId=None, streamId=None,):
    self.sessionId = sessionId
    self.streamId = streamId

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.sessionId = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.streamId = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('deleteStreamById_args')
    if self.sessionId is not None:
      oprot.writeFieldBegin('sessionId', TType.STRING, 1)
      oprot.writeString(self.sessionId)
      oprot.writeFieldEnd()
    if self.streamId is not None:
      oprot.writeFieldBegin('streamId', TType.STRING, 2)
      oprot.writeString(self.streamId)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class deleteStreamById_result:
  """
  Attributes:
   - success
   - se
  """

  thrift_spec = (
    (0, TType.BOOL, 'success', None, None, ), # 0
    (1, TType.STRUCT, 'se', (Exception.ttypes.ThriftSessionExpiredException, Exception.ttypes.ThriftSessionExpiredException.thrift_spec), None, ), # 1
  )

  def __init__(self, success=None, se=None,):
    self.success = success
    self.se = se

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.BOOL:
          self.success = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 1:
        if ftype == TType.STRUCT:
          self.se = Exception.ttypes.ThriftSessionExpiredException()
          self.se.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('deleteStreamById_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.BOOL, 0)
      oprot.writeBool(self.success)
      oprot.writeFieldEnd()
    if self.se is not None:
      oprot.writeFieldBegin('se', TType.STRUCT, 1)
      self.se.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class deleteStreamByNameVersion_args:
  """
  Attributes:
   - sessionId
   - streamName
   - streamVersion
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'sessionId', None, None, ), # 1
    (2, TType.STRING, 'streamName', None, None, ), # 2
    (3, TType.STRING, 'streamVersion', None, None, ), # 3
  )

  def __init__(self, sessionId=None, streamName=None, streamVersion=None,):
    self.sessionId = sessionId
    self.streamName = streamName
    self.streamVersion = streamVersion

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.sessionId = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.streamName = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.streamVersion = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('deleteStreamByNameVersion_args')
    if self.sessionId is not None:
      oprot.writeFieldBegin('sessionId', TType.STRING, 1)
      oprot.writeString(self.sessionId)
      oprot.writeFieldEnd()
    if self.streamName is not None:
      oprot.writeFieldBegin('streamName', TType.STRING, 2)
      oprot.writeString(self.streamName)
      oprot.writeFieldEnd()
    if self.streamVersion is not None:
      oprot.writeFieldBegin('streamVersion', TType.STRING, 3)
      oprot.writeString(self.streamVersion)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class deleteStreamByNameVersion_result:
  """
  Attributes:
   - success
   - se
  """

  thrift_spec = (
    (0, TType.BOOL, 'success', None, None, ), # 0
    (1, TType.STRUCT, 'se', (Exception.ttypes.ThriftSessionExpiredException, Exception.ttypes.ThriftSessionExpiredException.thrift_spec), None, ), # 1
  )

  def __init__(self, success=None, se=None,):
    self.success = success
    self.se = se

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 0:
        if ftype == TType.BOOL:
          self.success = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 1:
        if ftype == TType.STRUCT:
          self.se = Exception.ttypes.ThriftSessionExpiredException()
          self.se.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('deleteStreamByNameVersion_result')
    if self.success is not None:
      oprot.writeFieldBegin('success', TType.BOOL, 0)
      oprot.writeBool(self.success)
      oprot.writeFieldEnd()
    if self.se is not None:
      oprot.writeFieldBegin('se', TType.STRUCT, 1)
      self.se.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
