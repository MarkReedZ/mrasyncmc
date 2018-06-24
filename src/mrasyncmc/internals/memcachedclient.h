#pragma once

#include <Python.h>
#include <stdbool.h>

typedef struct {
  PyObject_HEAD
  int num_servers;
} MemcachedClient;

PyObject *MemcachedClient_new    (PyTypeObject* self, PyObject *args, PyObject *kwargs);
int       MemcachedClient_init   (MemcachedClient* self,    PyObject *args, PyObject *kwargs);
void      MemcachedClient_dealloc(MemcachedClient* self);

PyObject *MemcachedClient_cinit(MemcachedClient* self);
void MemcachedClient_setup( MemcachedClient* self ) ;

PyObject *MemcachedClient_get_server_index_and_validate( MemcachedClient *self, PyObject *key );

