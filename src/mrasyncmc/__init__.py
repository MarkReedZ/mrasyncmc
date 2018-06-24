
from .internals import MemcachedClient as CMemcachedClient
from .client import create_client
#from .exceptions import ClientException, ValidationException

__all__ = ('Client')#, 'ClientException', 'ValidationException')

__version__ = '0.1.0'
