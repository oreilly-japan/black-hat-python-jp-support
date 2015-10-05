#include <windows.h>
#include <stdio.h>
#include <excpt.h> 
#include <Python.h>

EXCEPTION_DISPOSITION excptHandler(
					 struct _EXCEPTION_RECORD* er, 
					 void* EstablisherFrame, 
					 struct _CONTEXT* ctx, 
					 void* DispatcherContext) 
{ 
	ctx->Eip++;
	return ExceptionContinueExecution;
} 


int checkVMware()
{
	int rc = 0;
    __try1(excptHandler){
		  int rslt = 0;
        __asm__("inl %%dx, %%eax" :                                     
                        "=b"(rslt) :    
                        "a"(0x564d5868),                   
                        "c"(0x0a),                    
                        "d"(0x5658), "b"(rslt):
                        "memory");
		  if(rslt == 0x564d5868)
		  	   rc = 1;
		  else
		      rc = 0;
	 }
	 __except1;

    return rc;
}

static PyObject* vmdetect_checkVMware(PyObject* self, PyObject* args)
{
	int ret = checkVMware();
	return Py_BuildValue("i", ret);
}

static PyMethodDef vmdetect_methods[] = {
	{"checkVMware", vmdetect_checkVMware, METH_NOARGS},
	{NULL, NULL}
};

void initvmdetect(void)
{
	(void) Py_InitModule("vmdetect", vmdetect_methods);
}



