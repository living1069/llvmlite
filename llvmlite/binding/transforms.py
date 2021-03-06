from __future__ import print_function, absolute_import
from ctypes import c_uint, c_bool
from . import ffi
from . import passmanagers


def create_pass_manager_builder():
    return PassManagerBuilder(ffi.lib.LLVMPY_PassManagerBuilderCreate())


class PassManagerBuilder(ffi.ObjectRef):
    __slots__ = ()

    @property
    def opt_level(self):
        return ffi.lib.LLVMPY_PassManagerBuilderGetOptLevel(self)

    @opt_level.setter
    def opt_level(self, level):
        ffi.lib.LLVMPY_PassManagerBuilderSetOptLevel(self, level)

    @property
    def size_level(self):
        return ffi.lib.LLVMPY_PassManagerBuilderGetSizeLevel(self)

    @size_level.setter
    def size_level(self, size):
        ffi.lib.LLVMPY_PassManagerBuilderSetSizeLevel(self, size)

    @property
    def inlining_threshold(self):
        raise NotImplementedError("inlining_threshold is write-only")

    @inlining_threshold.setter
    def inlining_threshold(self, threshold):
        ffi.lib.LLVMPY_PassManagerBuilderUseInlinerWithThreshold(self, threshold)

    @property
    def disable_unit_at_a_time(self):
        return ffi.lib.LLVMPY_PassManagerBuilderGetDisableUnitAtATime(self)

    @disable_unit_at_a_time.setter
    def disable_unit_at_a_time(self, disable=True):
        ffi.lib.LLVMPY_PassManagerBuilderSetDisableUnitAtATime(self, disable)

    @property
    def disable_unroll_loops(self):
        return ffi.lib.LLVMPY_PassManagerBuilderGetDisableUnrollLoops(self)

    @disable_unroll_loops.setter
    def disable_unroll_loops(self, disable=True):
        ffi.lib.LLVMPY_PassManagerBuilderSetDisableUnrollLoops(self, disable)

    @property
    def loop_vectorize(self):
        return ffi.lib.LLVMPY_PassManagerBuilderGetLoopVectorize(self)

    @loop_vectorize.setter
    def loop_vectorize(self, enable=True):
        return ffi.lib.LLVMPY_PassManagerBuilderSetLoopVectorize(self, enable)

    @property
    def slp_vectorize(self):
        return ffi.lib.LLVMPY_PassManagerBuilderGetSLPVectorize(self)

    @slp_vectorize.setter
    def slp_vectorize(self, enable=True):
        return ffi.lib.LLVMPY_PassManagerBuilderSetSLPVectorize(self, enable)

    def _populate_module_pm(self, pm):
        ffi.lib.LLVMPY_PassManagerBuilderPopulateModulePassManager(self, pm)

    def _populate_function_pm(self, pm):
        ffi.lib.LLVMPY_PassManagerBuilderPopulateFunctionPassManager(self, pm)

    def populate(self, pm):
        if isinstance(pm, passmanagers.ModulePassManager):
            self._populate_module_pm(pm)
        elif isinstance(pm, passmanagers.FunctionPassManager):
            self._populate_function_pm(pm)
        else:
            raise TypeError(pm)

    def _dispose(self):
        self._capi.LLVMPY_PassManagerBuilderDispose(self)


# ============================================================================
# FFI

ffi.lib.LLVMPY_PassManagerBuilderCreate.restype = ffi.LLVMPassManagerBuilderRef

ffi.lib.LLVMPY_PassManagerBuilderDispose.argtypes = [
    ffi.LLVMPassManagerBuilderRef,
]

ffi.lib.LLVMPY_PassManagerBuilderPopulateModulePassManager.argtypes = [
    ffi.LLVMPassManagerBuilderRef,
    ffi.LLVMPassManagerRef,
]

ffi.lib.LLVMPY_PassManagerBuilderPopulateFunctionPassManager.argtypes = [
    ffi.LLVMPassManagerBuilderRef,
    ffi.LLVMPassManagerRef,
]

# Unsigned int PassManagerBuilder properties

for _func in (ffi.lib.LLVMPY_PassManagerBuilderSetOptLevel,
              ffi.lib.LLVMPY_PassManagerBuilderSetSizeLevel,
              ffi.lib.LLVMPY_PassManagerBuilderUseInlinerWithThreshold,
              ):
    _func.argtypes = [ffi.LLVMPassManagerBuilderRef, c_uint]

for _func in (ffi.lib.LLVMPY_PassManagerBuilderGetOptLevel,
              ffi.lib.LLVMPY_PassManagerBuilderGetSizeLevel,
              ):
    _func.argtypes = [ffi.LLVMPassManagerBuilderRef]
    _func.restype = c_uint

# Boolean PassManagerBuilder properties

for _func in (ffi.lib.LLVMPY_PassManagerBuilderSetDisableUnitAtATime,
              ffi.lib.LLVMPY_PassManagerBuilderSetDisableUnrollLoops,
              ffi.lib.LLVMPY_PassManagerBuilderSetLoopVectorize,
              ffi.lib.LLVMPY_PassManagerBuilderSetSLPVectorize,
              ):
    _func.argtypes = [ffi.LLVMPassManagerBuilderRef, c_bool]

for _func in (ffi.lib.LLVMPY_PassManagerBuilderGetDisableUnitAtATime,
              ffi.lib.LLVMPY_PassManagerBuilderGetDisableUnrollLoops,
              ffi.lib.LLVMPY_PassManagerBuilderGetLoopVectorize,
              ffi.lib.LLVMPY_PassManagerBuilderGetSLPVectorize,
              ):
    _func.argtypes = [ffi.LLVMPassManagerBuilderRef]
    _func.restype = c_bool

