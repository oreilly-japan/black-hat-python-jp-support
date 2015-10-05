# -*- coding: utf-8 -*-

from miasm2.core import utils
from miasm2.analysis.machine import Machine
from miasm2.jitter.csts import PAGE_READ, PAGE_WRITE
from miasm2.arch.x86 import sem, regs
import miasm2.expression.expression as expr
from bhpasm import assemble_text, asm_helloworld

ADDR_SYSCALL_NEXTIP = 0xF0000000
def emit_syscall(ir, instr):
    e = []
    # EXCEPT_PRIV_INSNの設定
    e.append(expr.ExprAff(regs.exception_flags,
        expr.ExprInt32(sem.EXCEPT_PRIV_INSN)))
    # syscallの次命令のポインタを保存
    e.append(expr.ExprAff(
        expr.ExprMem(expr.ExprInt64(ADDR_SYSCALL_NEXTIP), 64),
        expr.ExprId(ir.get_next_label(instr), instr.mode)
    ))
    return e, []

def on_syscall(jitter):
    nextip = unpack("<Q", jitter.vm.get_mem(ADDR_SYSCALL_NEXTIP, 8))[0]
    if nextip != 0:
        # ログ出力
        if jitter.cpu.RAX == 1:
            print "sys_write(%d, buf, %d)" % (jitter.cpu.RDI, jitter.cpu.RDX)
            buf = jitter.vm.get_mem(jitter.cpu.RSI, jitter.cpu.RDX)
            print "buf = "
            utils.hexdump(buf)
        else:
            print "Unknown system call"
        # 戻り値の設定
        jitter.cpu.RAX = jitter.cpu.RDX
        # 例外コードのクリア
        jitter.cpu.set_exception(0)

        # フラグのクリア
        jitter.vm.set_mem(ADDR_SYSCALL_NEXTIP, "\x00" * 8)
        jitter.pc = nextip

    return True

def init_syscall(jitter, callback=on_syscall):
    sem.mnemo_func['syscall'] = emit_syscall
    jitter.vm.add_memory_page(ADDR_SYSCALL_NEXTIP, PAGE_READ | PAGE_WRITE,
      "\x00" * 8)
    jitter.add_exception_handler(sem.EXCEPT_PRIV_INSN, callback)

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

    init_syscall(jitter, on_syscall)

    jitter.init_run(run_addr)
    jitter.continue_run()

if __name__ == "__main__":
    main()
