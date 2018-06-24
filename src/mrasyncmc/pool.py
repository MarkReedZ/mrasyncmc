



import asyncio

__all__ = ['ConnectionPool']

class Connection():
  def __init__(self, reader, writer, pool):
    self.r = reader
    self.w = writer
    self.pool = pool

  def __enter__(self):
    pass

  def __exit__(self, type, value, traceback):
    self.release()

  def release(self):
    self.pool.release_connection(self)
    

class ConnectionPool:
  def __init__(self, host, port, size, loop=None, connection_timeout=1):
    loop = loop if loop is not None else asyncio.get_event_loop()
    self.host = host
    self.port = port
    self.max_size = size
    self.loop = loop
    self.connection_timeout = connection_timeout

    self.pool = asyncio.Queue(loop=loop)
    self.in_use = set()


  async def open_connections(self):
    for x in range(self.max_size):
      try:
        c = await self._create_new_conn()
        if c != None: self.pool.put_nowait(c)
      except:
        return False # TODO don't return false if we've created at least 1 connection?
    if self.pool.qsize() == 0: return False
    return True

  async def close(self):
    while not self.pool.empty():
      conn = await self.pool.get()
      self._close_connection(conn)

  async def get_connection(self):

    if self.size() < self.max_size:
      c = await self._create_new_conn()
      if c != None: 
        self.pool.put_nowait(c)
        return c

    c = None
    while not c:
      c = await self.pool.get()
      if c.r.at_eof() or c.r.exception():
        self._close_connection(c)
        c = await self._create_new_conn()

    self.in_use.add(c)
    return c

  def release_connection(self, conn):
    if conn in self.in_use:
      self.in_use.remove(conn)
      if conn.r.at_eof() or conn.r.exception(): self._close_connection(conn)
      else:                                     self.pool.put_nowait(conn)

  def size(self):
    return self.pool.qsize() + len(self.in_use)




  async def _create_new_conn(self):
    if self.size() < self.max_size:
      fut = asyncio.open_connection( self.host, self.port, loop=self.loop )
      try:
        r, w = await asyncio.wait_for(fut, timeout=self.connection_timeout)
      except asyncio.TimeoutError:
        print("Error timeout")# TODO
        #TODO logging? print("Timeout, skipping {}".format(host[1]))
        return None
      if self.size() < self.max_size:
        return Connection(r, w, self)
      else:
        r.feed_eof()
        w.close()
        return None
    else:
      return None

  def _close_connection(self, c):
    c.r.feed_eof()
    c.w.close()


