
# Notes
# longer keys is faster because of the sse instruction on key > 16 TODO speed up the key < 16?
#

import asyncio
import mrasyncmc
import aiomcache
import time

loop = asyncio.get_event_loop()

mc = None
async def setup():
  global mc, aiomc
  aiomc = aiomcache.Client("127.0.0.1", 11211, loop=loop)
  #mc = await mrasyncmc.create_client([("localhost",11211),("localhost",11212),("localhost",11213),("localhost",11214)],pool_size=8)
  mc = await mrasyncmc.create_client([("localhost",11211),("localhost",11212)],pool_size=8)
  await mc.set(b'longkeyexists012345678901234567890123456789',b'valislongaswellforthiskeyjustforfuntestingpurposes',noreply=True)
  await mc.set(b'keyexists',b'val',noreply=True)
  await mc.set(b'incrtest',b'1',noreply=True)
  await mc.set(b'decrtest',b'1000000',noreply=True)
  await aiomc.set(b'longkeyexists012345678901234567890123456789',b'valislongaswellforthiskeyjustforfuntestingpurposes')
  await aiomc.set(b'keyexists',b'val')
  await aiomc.set(b'incrtest',b'1')
  await aiomc.set(b'decrtest',b'1000000')
  for x in range(1000):
    v = await mc.get(b"keyexists")
    v = await aiomc.get(b"keyexists")

async def bench():

  async def timget(func, *args, **kwargs):
    num = 0
    s = time.time()
    numfuts = 100
    for x in range(100):
      futs = []
      for y in range(numfuts):
        futs.append( func(*args,**kwargs) )
      v = await asyncio.gather(*futs)
      num+=numfuts
    e = time.time()
    print( num/(e-s)," Requests/second", k)
  
  
  async def tim(func, *args,**kwargs):
    num = 0
    s = time.time()
    for x in range(10000):
      v = await func(*args,**kwargs)
      num+=1
    e = time.time()
    print( num/(e-s)," Requests/second", k)

  print("\nBenchmarking get\n")
  for k in [b"keyexists",b"keydoesnotexist",b"longkeyexists012345678901234567890123456789",b"longkeydoesnotexists012345678901234567890123456789"]:
    await timget(mc.get, k)
  print("\nBenchmarking set\n")
  for k in [b"keyexists",b"keydoesnotexist",b"longkeyexists012345678901234567890123456789",b"longkeydoesnotexists012345678901234567890123456789"]:
    await tim(mc.set, k, b"val", noreply=True)
  #print("\nBenchmarking the rest\n")
  #for k in [b"incr_test"]:
    #await timget(mc.incr, k)
  #for k in [b"decr_test"]:
    #await timget(mc.decr, k)

  if 0:
    print("\nBenchmarking get\n")
    for k in [b"keyexists",b"keydoesnotexist",b"longkeyexists012345678901234567890123456789",b"longkeydoesnotexists012345678901234567890123456789"]:
      await timget(aiomc.get, k)
    print("\nBenchmarking set\n")
    for k in [b"keyexists",b"keydoesnotexist",b"longkeyexists012345678901234567890123456789",b"longkeydoesnotexists012345678901234567890123456789"]:
      await tim(aiomc.set, k, b"val")


  print("")
  print("")

import psutil
import atexit

# You can top and add anything you run
noisy = ['atom', 'chrome', 'firefox', 'dropbox', 'opera', 'spotify', 'gnome-documents']
def silence():
  for proc in psutil.process_iter():
    if proc.name() in noisy:
      proc.suspend()

  def resume():
    for proc in psutil.process_iter():
      if proc.name() in noisy:
        proc.resume()
  atexit.register(resume)
silence()

loop.run_until_complete(setup())
loop.run_until_complete(bench())
