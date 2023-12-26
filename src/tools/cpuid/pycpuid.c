#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "cpuid-aux.h"

PyObject* cpuid(PyObject* self, PyObject* args) {
	char buffer[13] = {0};
	PyObject* root_dict;
	unsigned eax = get_cpuid(buffer);
	root_dict = PyDict_New();
	PyDict_SetItem(root_dict, PyUnicode_FromString("eax"),
			PyLong_FromLong(eax));
	PyDict_SetItem(root_dict, PyUnicode_FromString("vendor"),
			PyUnicode_FromString(buffer));
	return root_dict;
}

PyObject* get_cpuid_leaf(PyObject* self, PyObject* args) {
	unsigned regdata[4];
	PyObject* ret_dict;
	if(!PyArg_ParseTuple(args, "I", &regdata[0])) {
		return NULL;
	}
	get_leaf(regdata[0], (char*)regdata);
	ret_dict = PyDict_New();
	PyDict_SetItem(ret_dict, PyUnicode_FromString("eax"),
			PyLong_FromLong(regdata[0]));
	PyDict_SetItem(ret_dict, PyUnicode_FromString("ebx"),
			PyLong_FromLong(regdata[1]));
	PyDict_SetItem(ret_dict, PyUnicode_FromString("ecx"),
			PyLong_FromLong(regdata[2]));
	PyDict_SetItem(ret_dict, PyUnicode_FromString("edx"),
			PyLong_FromLong(regdata[3]));
	return ret_dict;
}

PyObject* processor_info(PyObject* self, PyObject* args) {
	struct proc_info info;
	PyObject* root_dict;

	get_processor_info(&info);
	root_dict = PyDict_New();
	PyDict_SetItem(root_dict, PyUnicode_FromString("family"),
			PyLong_FromLong(info.family));
	PyDict_SetItem(root_dict, PyUnicode_FromString("model"),
			PyLong_FromLong(info.model));
	PyDict_SetItem(root_dict, PyUnicode_FromString("type"),
			PyLong_FromLong(info.type));
	PyDict_SetItem(root_dict, PyUnicode_FromString("stepping"),
			PyLong_FromLong(info.stepping));
	return root_dict;
}

PyObject* max_extended(PyObject* self, PyObject* args) {
	return PyLong_FromLong(get_max_extended());
}

PyObject* get_cpu_name(PyObject* self, PyObject* args) {
	char buffer[3*16 + 1] = { 0 };
	/* XXX: raise exception if this returns NULL */
	get_processor_name(buffer);
	return PyUnicode_FromString(buffer);
}

static PyMethodDef pycpuid_methods[] = {
		{"cpuid", cpuid, METH_NOARGS, ""}, 
		{"processor_info", processor_info, METH_NOARGS, ""},
		{"max_extended", max_extended, METH_NOARGS, ""},
		{"get_cpu_name", get_cpu_name, METH_NOARGS, ""},
		{"get_cpuid_leaf", get_cpuid_leaf, METH_VARARGS, ""},
		{NULL, NULL, 0, NULL}
	};

static PyModuleDef pycpuid = {
		.m_base = PyModuleDef_HEAD_INIT,
		.m_name = "cpuid",
		.m_doc = NULL,
		.m_size = -1,
		.m_methods = pycpuid_methods,
	};

PyMODINIT_FUNC
PyInit_pycpuid(void) {
	PyObject* cpuid_module = PyModule_Create(&pycpuid);
	// PyObject* locals = PyModule_GetDict(cpuid_module);
	return cpuid_module;
}
