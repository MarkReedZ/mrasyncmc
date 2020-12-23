
import asyncio
import mrasyncmc
import inspect

async def raises( f, *args, exc=ValueError,details="", **kwargs ):
  cf = inspect.currentframe()
  try:
    await f(*args,**kwargs)
    print("  ERROR",__file__,"line", cf.f_back.f_lineno," failed to raise the expected exception" ,exc)
  except Exception as e:
    if type(e) != exc:
      print("  ERROR",__file__,"line", cf.f_back.f_lineno," exception type miscompare\n  act:",type(e),"\n  exp:",exc )
    if str(e) != details:
      print("  ERROR",__file__,"line", cf.f_back.f_lineno," exception details miscompare\n  act:",e,"\n  exp:",details )

def eq( a, b ):
  if a != b:
    cf = inspect.currentframe()
    #print(cf.f_back.f_code.co_name)
    print("  ERROR",__file__,"line", cf.f_back.f_lineno,a,"!=",b)


def foo( a, b ):
  pass
  #raise ConnectionError("foo")


def test_a():
  print("test_a")
  raises( foo, 1, 2, exc=ValueError, details="fart" )
  eq(1,2)


async def single():

  await raises( mrasyncmc.create_client, [("localhost",11211)], pool_size=2, exc=ValueError, details="Unable to connect to any memcached servers" )
  #try:
    #c = await mrasyncmc.create_client([("localhost",11211)],pool_size=2)
  #except Exception as e:
    #print("YAY",type(e),e)

  #await c.close()

async def cluster():

  c = await mrasyncmc.create_client([("localhost",11211),("localhost",11212)],pool_size=2)

  await c.close()

if __name__ == '__main__':
  #test_a()
  asyncio.run(single())
  #asyncio.run(cluster())

