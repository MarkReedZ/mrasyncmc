
import asyncio, time
import mrasyncmc
import tracemalloc
tracemalloc.start()


async def run(loop):

  #try:
  print("before")
  c = await mrasyncmc.create_client([("localhost",11211),("localhost",11212)],pool_size=1)
  #except ConnectionError as e:
    #print("Failed to connect:", e)
    #return
  #c = await mrasyncmc.create_client([("localhost",11211)],pool_size=2)
  print("FDAS")
  return

  x = b'a' * 100
  await c.set(b"test",x)
  print(await c.get(b"test"))
  print(await c.get(b"keyexists"))

  if 1:
    await c.set(b"test1",b"tets1")
    await c.set(b"test2",b"tets2")
    await c.set(b"test3",b"tets3")
    await c.set(b"test4",b"tets4")
    await c.set(b"test5",b"tets5")
    await c.set(b"test6",b"tets6")
    await c.set(b"test7",b"tets7")
    await c.set(b"test8",b"tets8")
    await c.set(b"test9",b"tets9")
    await c.set(b"test10",b"tets10")
    await c.set(b"test11",b"tets11")
  
    while 1:
      print("top")
      futs = []
      #print(await rc.get(b"test1"))
      futs.append( c.get(b"test1") )
      futs.append( c.get(b"test2") )
      futs.append( c.get(b"test3") )
      futs.append( c.get(b"test4") )
      futs.append( c.get(b"test5") )
      futs.append( c.get(b"test6") )
      futs.append( c.get(b"test7") )
      futs.append( c.get(b"test8") )
      futs.append( c.get(b"test9") )
      futs.append( c.get(b"test10") )
  
      try:
        ret = await asyncio.gather(*futs)
      except Exception as e:
        print(" Connection failed waiting 5: ",e)
        await asyncio.sleep(5)
        continue
      futs = []
      for v in ret:
        print(v)
      await asyncio.sleep(5)
  



  await c.close()
  print("YAY")
  return
  await c.set(b"keyexists",b'bal')
  await c.set(b"test",b'bal')
  await c.set(b"test2",b'bal')
  await c.set(b"incr",b'1')
  await c.set(b"5seconds",b'1',5)

  print(await c.get(b"test2"))
  await c.append(b"test2",b'foo')
  await c.prepend(b"test2",b'foo')
  print("app and pre", await c.get(b"test2"))
  await c.replace(b"test2",b'replace')
  print("replace", await c.get(b"test2"))
  await c.add(b"test2",b'add')
  print("add exists", await c.get(b"test2"))
  await c.add(b"test22",b'add')
  print("add", await c.get(b"test22"))

  print(await c.get(b"keyexists"))
  print(await c.get_many([b"keyexists",b"test",b"test2",b"test3"]))


  print(await c.incr(b"incr"))
  print(await c.incr(b"incr"))
  print(await c.incr(b"incr"))
  print(await c.incr(b"incr"))
  print(await c.decr(b"incr"))
  print(await c.decr(b"incr"))
  print(await c.decr(b"incr"))
  print(await c.decr(b"incr"))
  print(await c.decr(b"incr"))

  print(await c.delete(b"test2",noreply=False))
  print("deleted?", await c.get(b"test2"))

  try:
    print(await c.get(b"invalid char \x10 fffffffffffffffff"))
    print("ERROR")
  except:
    print("Saw invalid char exceptions")

  # expiration
  if 0:
    print("Waiting for expiration")
    await asyncio.sleep(2)
    print(await c.get(b"5seconds"))
    print(await c.touch(b"5seconds",10))
    await asyncio.sleep(5)
    print(await c.get(b"5seconds"))
    await asyncio.sleep(7)
    print(await c.get(b"5seconds"))

  await c.close()


if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(run(loop))
  loop.close()


