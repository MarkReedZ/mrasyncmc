
#pragma once
#include "Python.h"
#include "memcachedclient.h"

static PyMethodDef MemcachedClient_methods[] = {
  {"cinit", (PyCFunction)MemcachedClient_cinit, METH_NOARGS,   ""},
  {"get_server_index_and_validate", (PyCFunction)MemcachedClient_get_server_index_and_validate, METH_O,   ""},
  {NULL}
};

static PyTypeObject MemcachedClientType = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "internals.MemcachedClient",       /* tp_name */
  sizeof(MemcachedClient),          /* tp_basicsize */
  0,                         /* tp_itemsize */
  (destructor)MemcachedClient_dealloc, /* tp_dealloc */
  0,                         /* tp_print */
  0,                         /* tp_getattr */
  0,                         /* tp_setattr */
  0,                         /* tp_reserved */
  0,                         /* tp_repr */
  0,                         /* tp_as_number */
  0,                         /* tp_as_sequence */
  0,                         /* tp_as_mapping */
  0,                         /* tp_hash  */
  0,                         /* tp_call */
  0,                         /* tp_str */
  0,
  0,                         /* tp_setattro */
  0,                         /* tp_as_buffer */
  Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,        /* tp_flags */
  "MemcachedClient",                /* tp_doc */
  0,                         /* tp_traverse */
  0,                         /* tp_clear */
  0,                         /* tp_richcompare */
  0,                         /* tp_weaklistoffset */
  0,                         /* tp_iter */
  0,                         /* tp_iternext */
  MemcachedClient_methods,           /* tp_methods */
  0,                         /* tp_members */
  0,            /* tp_getset */
  0,                         /* tp_base */
  0,                         /* tp_dict */
  0,                         /* tp_descr_get */
  0,                         /* tp_descr_set */
  0,                         /* tp_dictoffset */
  (initproc)MemcachedClient_init,    /* tp_init */
  0,                         /* tp_alloc */
  MemcachedClient_new,              /* tp_new */
};

