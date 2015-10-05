# -*- coding: utf-8 -*-

from miasm2.core import utils
from miasm2.analysis.machine import Machine
from miasm2.jitter.csts import PAGE_READ, PAGE_WRITE
import miasm2.expression.expression as expr
from miasm2.arch.x86 import sem

from bhpasm import assemble_text, asm_helloworld
from bhpemu import init_syscall

ADDR_COUNTER = 0xF1000000
def emit_mov(ir, instr, a, b):
    # movの中間表現を生成
    instr_ir, extra_ir = sem.mov(ir, instr, a, b)
    # カウンタをインクリメントする中間表現を追加
    dst = expr.ExprMem(expr.ExprInt64(ADDR_COUNTER), 64)
    new_value = dst + expr.ExprInt64(1)
    instr_ir.append(expr.ExprAff(dst, new_value))
    return instr_ir, extra_ir
sem.mnemo_func['mov'] = emit_mov

def on_exit(jitter):
    jitter.run = False
    jitter.pc = 0
    return True

from struct import unpack
def main():
    sc = assemble_text(asm_helloworld, [("L_MAIN", 0)]) 

    mach = Machine("x86_64")
    jitter = mach.jitter(jit_type="tcc")
    run_addr =0x40000000
    jitter.init_stack()
    jitter.vm.add_memory_page(run_addr, PAGE_READ | PAGE_WRITE, sc)
    jitter.push_uint64_t(0xdeadbeef)
    jitter.add_breakpoint(0xdeadbeef, on_exit)
    #jitter.jit.log_regs = True
    jitter.jit.log_mn = True

    init_syscall(jitter)
    jitter.vm.add_memory_page(ADDR_COUNTER, PAGE_READ | PAGE_WRITE, "\x00" * 8)

    jitter.init_run(run_addr)
    jitter.continue_run()

    print "MOV: %d" % unpack("I", jitter.vm.get_mem(ADDR_COUNTER, 4))[0]

if __name__ == "__main__":
    main()
