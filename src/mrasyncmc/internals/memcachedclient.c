
#include <Python.h>
#include <stdbool.h>



#if defined __SSE4_2__
#ifdef _MSC_VER
#include <nmmintrin.h>
#else
#include <x86intrin.h>
#endif
#endif

#include "common.h"
#include "module.h"
#include "city.h"


#define MAX_SERVERS 8192
static int srvmap[MAX_SERVERS];

static char hexchar[256] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                             0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0, 
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                             0,10,11,12,13,14,15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

PyObject *MemcachedClient_new(PyTypeObject* type, PyObject *args, PyObject *kwargs) {
  MemcachedClient* self = NULL;
  self = (MemcachedClient*)type->tp_alloc(type, 0);
  return (PyObject*)self;
}


void MemcachedClient_dealloc(MemcachedClient* self) {
}

int MemcachedClient_init(MemcachedClient* self, PyObject *args, PyObject *kwargs) {
  if(!PyArg_ParseTuple(args, "i", &self->num_servers)) return 1;
  MemcachedClient_setup(self); 
  return 0;
}

PyObject *MemcachedClient_cinit(MemcachedClient* self) {
  Py_RETURN_NONE;
}

void MemcachedClient_setup( MemcachedClient* self ) {
  if ( self->num_servers == 0 ) return;

  int seg = MAX_SERVERS / self->num_servers;
  int i = 0;
  int off = 0;
  for ( ; i < self->num_servers-1; i++ ) {
    for (int j = 0; j < seg; j++ ) {
      srvmap[off++] = i; 
    }
  }
  while ( off < MAX_SERVERS ) srvmap[off++] = i;

}

#if __GNUC__ >= 3
#define likely(x) __builtin_expect(!!(x), 1)
#define unlikely(x) __builtin_expect(!!(x), 0)
#else
#define likely(x) (x)
#define unlikely(x) (x)
#endif

#ifdef _MSC_VER
#define ALIGNED(n) _declspec(align(n))
#else
#define ALIGNED(n) __attribute__((aligned(n)))
#endif


static int has_char_in_range(const char *buf, int bufsz, const char *ranges, size_t ranges_size)
{
    char *end = buf + bufsz;
#if __SSE4_2__
    if ( bufsz >= 16 ) {
        __m128i ranges16 = _mm_loadu_si128((const __m128i *)ranges);

        size_t left = bufsz & ~15;
        do {
            __m128i b16 = _mm_loadu_si128((const __m128i *)buf);
            int r = _mm_cmpestri(ranges16, ranges_size, b16, 16, _SIDD_LEAST_SIGNIFICANT | _SIDD_CMP_RANGES | _SIDD_UBYTE_OPS);
            if (unlikely(r != 16)) {
              return 1;
            }
            buf += 16;
            left -= 16;
        } while (likely(left != 0));
    }
#else
    /* suppress unused parameter warning */
    (void)bufsz;
    (void)ranges;
    (void)ranges_size;
#endif
    while ( buf < end ) {
      if ( *buf < 0x21 || *buf > 0x7E ) {
        return 1;
      }
      buf++;
    }
    return 0;
}


// Length is 1 < k < 250 and chars are 0x21 < c < 0x7E
PyObject *MemcachedClient_get_server_index_and_validate( MemcachedClient *self, PyObject *key ) {
  char *k;
  Py_ssize_t ksz;
  if ( -1 == PyBytes_AsStringAndSize( key, &k, &ksz ) ) return NULL;

  if ( ksz < 1 || ksz > 250 ) {
    PyErr_SetString(PyExc_ValueError, "Memcached key is not a valid length 1<k<250");
    return NULL;
  }
  static const char ALIGNED(16) ranges[] = "\x00\x21\x7e\xff"; // < 0x21 or > 0x7E is an invalid character
  if ( has_char_in_range(k, ksz, ranges, sizeof(ranges) - 1) ) {
    PyErr_SetString(PyExc_ValueError, "Memcached key has an invalid character");
    return NULL;
  }

  unsigned long hv = CityHash64(k, ksz);
  return PyLong_FromUnsignedLong( srvmap[hv & 0xFFF]);
}

