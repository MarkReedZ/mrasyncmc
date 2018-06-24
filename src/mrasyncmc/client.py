
import asyncio
import socket
import os
from . import CMemcachedClient
from .server import Server

async def create_client( servers, pool_size=2, loop=None, connection_timeout=1 ):
  loop = loop if loop is not None else asyncio.get_event_loop()
  c = Client(servers, pool_size, loop, connection_timeout)
  num = await c.setup_connections()
  if num == 0:
    print("WARNING: Unable to connect to any memcached servers")
  return c
  
  
class Client(CMemcachedClient):
  def __init__(self, servers, pool_size, loop, connection_timeout):
    self.connection_timeout = connection_timeout

    if not isinstance(servers, list):
      raise ValueError("Memcached client takes a list of (host, port) servers")

    self.servers = []
    for s in servers:
      self.servers.append( Server( s[0], s[1], pool_size, loop, connection_timeout ) ) 

    super().__init__(len(servers))

  async def setup_connections(self):
    cnt = 0
    for s in self.servers:
      if not await s.open_connections():
        s.failed = True
      else:
        cnt += 1
    return cnt
      
  async def close(self):
    for s in self.servers:
      await s.close()

  async def get(self, key, default=None):
    server_index = self.get_server_index_and_validate(key)
    c = self.servers[ server_index ].get_connection()
    c.w.write(b'get '  + key + b'\r\n')
    r = await c.respq.get()
    try:
      return r[key][0]
    except:
      return None

  async def gets(self, key, default=None):
    server_index = self.get_server_index_and_validate(key)
    c = self.servers[ server_index ].get_connection()
    c.w.write(b'gets '  + key + b'\r\n')
    r = await c.respq.get()
    try:
      return r[key]
    except:
      return None

  async def get_many(self, keys):

    batches = {}
    for k in keys:
      srv = self.get_server_index_and_validate(k)
      if not srv in batches:
        batches[srv] = [k]
      else:
        batches[srv].append(k)

    futs = []
    for srv in batches.keys():
      keys = batches[srv]
      c = self.servers[ srv ].get_connection()
      c.w.write(b'get '  + b' '.join(keys) + b'\r\n')
      futs.append( c.respq.get() )
 
    d = {}
    results = await asyncio.gather(*futs)
    for r in results:
      for k in r.keys():
        d[k] = r[k][0]
  
    return d

  async def _store(self, cmd, key, val, exp=0, flags=0, noreply=True):
    server_index = self.get_server_index_and_validate(key)
    if not isinstance(exp,int):
      raise ValueError("Expiration must be an int")
    c = self.servers[ server_index ].get_connection()
    args = [str(a).encode('utf-8') for a in (flags, exp, len(val))]
    cmd = cmd + b' ' + b' '.join([key] + args)
    if noreply: cmd += b' noreply'
    cmd += b'\r\n' + val + b'\r\n'
    c.w.write(cmd)
    if noreply: return True
    resp = await c.respq.get()
    return resp == b'STORED'

  async def set(self, key, val, exp=0, flags=0, noreply=True):
    return await self._store(b"set", key, val, exp, flags, noreply)
  async def append(self, key, val, exp=0, flags=0,noreply=True):
    return await self._store(b"append", key, val, exp, flags, noreply)
  async def prepend(self, key, val, exp=0, flags=0,noreply=True):
    return await self._store(b"prepend", key, val, exp, flags, noreply)
  async def replace(self, key, val, exp=0, flags=0,noreply=True):
    return await self._store(b"replace", key, val, exp, flags, noreply)
  async def add(self, key, val, exp=0, flags=0,noreply=True):
    return await self._store(b"add", key, val, exp, flags, noreply)

  async def delete(self, key):
    s = self.get_server_index_and_validate(key)
    c = self.servers[ s ].get_connection()
    c.w.write(b'delete ' + key + b'\r\n')
    resp = await c.respq.get()
    return resp == b'DELETED'

  async def incr(self, key, increment=1):
    # Returns the incremented value or None if the key wasn't found
    s = self.get_server_index_and_validate(key)
    c = self.servers[ s ].get_connection()
    c.w.write(b'incr ' + key + b' ' + str(increment).encode('utf-8') + b'\r\n')
    resp = await c.respq.get()
    if resp.isdigit(): return int(resp)
    if resp == b"NOT_FOUND": return None
    else:
      raise ValueError("Bad response from server on increment: " + str(resp))

  async def decr(self, key, decrement=1):
    # Returns the decremented value or None if the key wasn't found
    s = self.get_server_index_and_validate(key)
    c = self.servers[ s ].get_connection()
    c.w.write(b'decr ' + key + b' ' + str(decrement).encode('utf-8') + b'\r\n')
    resp = await c.respq.get()
    if resp.isdigit(): return int(resp)
    if resp == b"NOT_FOUND": return None
    else:
      raise ValueError("Bad response from server on decrement: " + str(resp))

