#include "module.h"

static PyModuleDef internals_module = {
  PyModuleDef_HEAD_INIT,
  "internals",
  "C internals",
  -1,
  NULL,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit_internals(void)
{

  PyObject* m = NULL;
  if (PyType_Ready(&MemcachedClientType) < 0) return NULL;

  m = PyModule_Create(&internals_module);
  if(!m) return NULL;

  Py_INCREF(&MemcachedClientType);
  PyModule_AddObject(m, "MemcachedClient", (PyObject*)&MemcachedClientType);

  return m;
}

