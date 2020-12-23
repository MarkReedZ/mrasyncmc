
from collections import deque
import asyncio
__all__ = ['Server']


class Connection():
  def __init__(self, reader, writer, server):
    self.r = reader
    self.w = writer
    self.server = server
    self.closed = False
    self.respq = asyncio.Queue(loop=server.loop)
    #self.futs = []
    self.futs = deque()
    self.loop = asyncio.get_event_loop()


  def close(self):
    c.r.feed_eof()
    c.w.close()
    self.closed = True;
    
        #elif spl[0] == b'CLIENT_ERROR' or spl[0] == b'SERVER_ERROR' or spl[0] == b'ERROR':
          #raise ValueError('Server returned an error: ' + line.decode("utf-8"))
        #else:
          #raise ValueError('Server responded with an unexpected response: ' + line.decode('utf-8'))
  async def reader(self):
    while not self.closed:
      line = await self.r.readline()
      #print(line)
      # TODO is == b'' okay? bench
      #if self.r.at_eof(): return
      if line == b'': 
        self.server.lost_connection(self)
        return

      #print("reader line >",line,"<")
      if line[0] == 86: #b'V'  VALUE
        await self.read_values(line)
      elif line == b'END\r\n':
        self.respq.put_nowait(None)
        #f = self.futs.popleft()
        #f.set_result(None)
      else:
        self.respq.put_nowait(line[:-2])
        #f = self.futs.popleft()
        #f.set_result(line[:-2])
     
  async def read_values(self, line):
    ret = {}
    r = None
    while line != b'END\r\n':
      #print("read_values:",line)
      spl = line.split()
      key = spl[1]
      length = int(spl[3])
      cas_token = None
      if (len(spl)==5): cas_token = spl[4]
      val = (await self.r.readexactly(length+2))[:-2]
      ret[key] = (val, cas_token) 
      line = await self.r.readline()
      if line == b'': return

    self.respq.put_nowait(ret)
    #f = self.futs.popleft()
    #f.set_result(ret)
    
       





class Server():
  def __init__(self, client, host, port, pool_size, loop, connection_timeout):
    self.conns = []
    self.failed = False
    self.loop = loop
    self.client = client
    self.host = host
    self.port = port
    self.max_connections = pool_size
    self.connection_timeout = connection_timeout
    self.next = 0
    self.reconnecting = False
    self.connection_attempts = 0

  async def open_connections(self):
    for x in range(self.max_connections):
      try:
        c = await self._create_new_conn()
        if c != None: 
          self.conns.append(c)
          asyncio.ensure_future(c.reader())
      except Exception as e:
        print("open_connections exception:",e)
        return False
    if len(self.conns) == 0: return False
    return True

  async def close(self):
    for c in self.conns:
      c.close()

  def get_connection(self):
    if self.reconnecting:
      return None
    c = self.conns[self.next]
    self.next = (self.next+1) % len(self.conns)
    return c

  def lost_connection(self, conn):
    if not self.reconnecting:
      self.conns.remove(conn)
      for c in self.conns:
        c.r.feed_eof()
        c.w.close()
      self.client.lost_server(self)
      self.reconnecting = True
      asyncio.ensure_future( self.reconnect() )


  async def _create_new_conn(self):
    if len(self.conns) >= self.max_connections: return None
    try:
      fut = asyncio.open_connection( self.host, self.port )
      r, w = await asyncio.wait_for(fut, timeout=self.connection_timeout)
    except asyncio.TimeoutError:
      print("ERROR timeout while connecting")# TODO test
      #TODO logging? print("Timeout, skipping {}".format(host[1]))
      return None
    #except Exception as e:
      #print("Exception while connecting:",e)
      #return None

    if len(self.conns) < self.max_connections:
      c = Connection(r, w, self)
      return c
    else:
      r.feed_eof()
      w.close()
      return None

  async def reconnect(self):
    self.conns = []
    while True:

      if self.connection_attempts < 3:
        await asyncio.sleep(5)
      elif self.connection_attempts < 10:
        await asyncio.sleep(30)
      else:
        await asyncio.sleep(360)

      try:
        self.connection_attempts += 1
        for x in range(self.max_connections):
          c = await self._create_new_conn()
          if c != None:
            self.conns.append(c)
            asyncio.ensure_future(c.reader())

        self.connection_attempts = 0
        self.reconnecting = False
        self.client.server_back(self)
        return
      except ConnectionRefusedError:
        for c in self.conns: 
          c.close()
        self.conns = []
      except Exception as e:
        print("  ",e)
        return False


