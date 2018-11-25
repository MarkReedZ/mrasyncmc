
import asyncio, time
import mrasyncmc

async def run(loop):

  #c = mrasyncmc.Client([("localhost",11211),("localhost",11212),("localhost",11213),("localhost",11214)])
  c = await mrasyncmc.create_client([("localhost",11211)],pool_size=2)

  print(await c.get(b"mrsession4af8e257df96441998ee6088024a592b"))
  #print(await c.stats(0))
  #print("")
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


