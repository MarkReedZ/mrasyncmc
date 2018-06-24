
import asyncio
__all__ = ['Server']


class Connection():
  def __init__(self, reader, writer, server):
    self.r = reader
    self.w = writer
    self.server = server
    self.closed = False
    self.respq = asyncio.Queue(loop=server.loop)

        #elif spl[0] == b'CLIENT_ERROR' or spl[0] == b'SERVER_ERROR' or spl[0] == b'ERROR':
          #raise ValueError('Server returned an error: ' + line.decode("utf-8"))
        #else:
          #raise ValueError('Server responded with an unexpected response: ' + line.decode('utf-8'))
  async def reader(self):
    while not self.closed:
      line = await self.r.readline()

      # TODO is == b'' okay? bench
      #if self.r.at_eof(): return
      if line == b'': return

      #print("reader line >",line,"<")
      if line[0] == 86: #b'V'  VALUE
        await self.read_values(line)
      elif line == b'END\r\n':
        self.respq.put_nowait(None)
      else:
        self.respq.put_nowait(line[:-2])
     
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
    
       





class Server(object):
  def __init__(self, host, port, pool_size, loop, connection_timeout):
    self.conns = []
    self.failed = False
    self.loop = loop
    self.host = host
    self.port = port
    self.max_connections = pool_size
    self.connection_timeout = connection_timeout
    self.next = 0

  async def open_connections(self):
    for x in range(self.max_connections):
      try:
        c = await self._create_new_conn()
        if c != None: 
          self.conns.append(c)
          asyncio.ensure_future(c.reader())
      except Exception as e:
        print("WTF",e)
      
        return False # TODO don't return false if we've created at least 1 connection?
    if len(self.conns) == 0: return False
    return True

  async def close(self):
    for conn in self.conns:
      self._close_connection(conn)

  def get_connection(self):
    c = self.conns[self.next]
    self.next = (self.next+1) % len(self.conns)
    return c

  async def _create_new_conn(self):
    if len(self.conns) >= self.max_connections: return None
    fut = asyncio.open_connection( self.host, self.port, loop=self.loop )
    try:
      r, w = await asyncio.wait_for(fut, timeout=self.connection_timeout)
    except asyncio.TimeoutError:
      print("Error timeout")# TODO
      #TODO logging? print("Timeout, skipping {}".format(host[1]))
      print("timeout while connecting")
      return None
    except Exception as e:
      print("exception while connecting:",e)
      return None

    if len(self.conns) < self.max_connections:
      c = Connection(r, w, self)
      return c
    else:
      r.feed_eof()
      w.close()
      return None

  def _close_connection(self, c):
    c.r.feed_eof()
    c.w.close()


