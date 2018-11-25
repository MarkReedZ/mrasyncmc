# MrAsyncMC
Python 3.5+ async Memcached client that is 3-10x faster than aiomcache

# Installation

-  ``pip install mrasyncmc``

# Usage

```python

import asyncio
import mrasyncmc

loop = asyncio.get_event_loop()

async def runme():

  c = await mrasyncmc.create_client([("localhost",11211)],pool_size=2)

  print(await c.get(b"key-does-not-exist"))
  await c.set(b'keyexists',b'foo')
  print(await c.get(b"keyexists"))

  await c.close()

loop.run_until_complete(runme())

```


# Benchmarks

```
python b.py

Benchmarking get

39,119  Requests/second  b'keyexists'
47,600  Requests/second  b'keydoesnotexist'
38,916  Requests/second  b'longkeyexists012345678901234567890123456789'
47,540  Requests/second  b'longkeydoesnotexists012345678901234567890123456789'

Benchmarking set

125,820  Requests/second  b'keyexists'
127,726  Requests/second  b'keydoesnotexist'
128,350  Requests/second  b'longkeyexists012345678901234567890123456789'
128,490  Requests/second  b'longkeydoesnotexists012345678901234567890123456789'

Benchmarking the rest

45,844  Requests/second  b'incr_test'
45,921  Requests/second  b'decr_test'

```

