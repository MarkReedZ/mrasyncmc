import pytest
import asyncio
import mrasyncmc

@pytest.mark.asyncio
async def test_connections():
  with pytest.raises(ConnectionError) as exc:
    print("A")
    c = await mrasyncmc.create_client([("localhost",112)])
    print("B")
  print(dir(exc))



