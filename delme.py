
import asyncio, time
import mrasyncmc

async def run(loop):

  #c = mrasyncmc.Client([("localhost",11211),("localhost",11212),("localhost",11213),("localhost",11214)])
  c = await mrasyncmc.create_client([("localhost",11211)],pool_size=2)

  print(await c.get(b"mrsession43709dd361cc443e976b05714581a7fb"))
  await c.set(b"mrsession43709dd361cc443e976b05714581a7fb",b'{"username":"Mark","id":1}')
  exit()
  await c.set(b"test2",b'bal')
  await c.close()


if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(run(loop))
  loop.close()


