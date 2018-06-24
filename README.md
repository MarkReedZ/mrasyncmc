# MrAsyncMC
Python 3.5+ async Memcached client

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

# TODO

The C memcached client embedded in [MrHTTP](https://github.com/MarkReedZ/mrhttp) gets almost 600,000 requests per second fetching session data from memcached so there is room for improvement.  The connection reader in server.py can be moved to C and add the responses to the response queue from there.


