# -*- coding: utf-8 -*-

from miasm2.core import utils
from miasm2.analysis.machine import Machine
from miasm2.jitter.csts import PAGE_READ, PAGE_WRITE
from miasm2.arch.x86 import sem, regs
import miasm2.expression.expression as expr
from bhpasm import assemble_text, asm_helloworld

def on_exit(jitter):
    jitter.run = False
    jitter.pc = 0
    return True

from struct import unpack
def main():
    native_code = assemble_text(asm_helloworld, [("L_MAIN", 0)]) 

    mach = Machine("x86_64")
    jitter = mach.jitter(jit_type="tcc")
    run_addr =0x40000000
    jitter.init_stack()
    jitter.vm.add_memory_page(run_addr, PAGE_READ | PAGE_WRITE, native_code)
    jitter.push_uint64_t(0xdeadbeef)
    jitter.add_breakpoint(0xdeadbeef, on_exit)
    jitter.jit.log_mn = True

    jitter.init_run(run_addr)
    jitter.continue_run()

if __name__ == "__main__":
    main()
