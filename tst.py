
import asyncio, time
import mrasyncmc

async def run(loop):

  #c = mrasyncmc.Client([("localhost",11211),("localhost",11212),("localhost",11213),("localhost",11214)])
  c = await mrasyncmc.create_client([("localhost",11211)],pool_size=2)

  print(await c.get(b"mrsession43709dd361cc443e976b05714581a7fb"))
  #print(await c.stats(0))
  exit()
  #print("")
  await c.set(b"keyexists",b'bal')
  await c.set(b"test",b'bal')
  await c.set(b"test2",b'bal')
  await c.set(b"incr",b'1')

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

  print(await c.delete(b"test2"))
  print("deleted?", await c.get(b"test2"))

  await c.close()


if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(run(loop))
  loop.close()


