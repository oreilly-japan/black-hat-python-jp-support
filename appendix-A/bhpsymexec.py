# -*- coding: utf-8 -*-

from miasm2.ir.translators.translator import Translator
from miasm2.ir.translators.z3_ir import Z3Mem
from bhpasm import assemble_text
from miasm2.arch.x86.disasm import dis_x86_64 as dis_engine
from miasm2.arch.x86.ira import ir_a_x86_64
from miasm2.ir.symbexec import symbexec
from miasm2.expression.expression import ExprInt_from, ExprCond, ExprId
from miasm2.expression.expression import ExprInt, ExprMem, ExprInt64
from miasm2.expression import modint
from miasm2.expression.simplifications import expr_simp
from miasm2.arch.x86.regs import *
import z3, sys

def find_goal(ir, start_addr, start_symbols, is_goal,
              cond_limit=10, uncond_limit=100):
    def codepath_walk(addr, symbols, conds, depth):
        if depth >= cond_limit:
            return None

        for _ in range(uncond_limit):
            sb = symbexec(ir, symbols)
            pc = sb.emul_ir_blocs(ir, addr)
            if is_goal(sb.symbols) == True:
                return conds

            if isinstance(pc, ExprCond):
                cond_true  = {pc.cond: ExprInt_from(pc.cond, 1)}
                cond_false = {pc.cond: ExprInt_from(pc.cond, 0)}
                addr_true  = expr_simp(
                    sb.eval_expr(pc.replace_expr(cond_true), {}))
                addr_false = expr_simp(
                    sb.eval_expr(pc.replace_expr(cond_false), {}))
                conds_true = list(conds) + cond_true.items()
                conds_false = list(conds) + cond_false.items()
                rslt = codepath_walk(
                    addr_true, sb.symbols.copy(), conds_true, depth + 1)
                if rslt != None:
                    return rslt
                rslt = codepath_walk(
                    addr_false, sb.symbols.copy(), conds_false, depth + 1)
                if rslt != None:
                    return rslt
                break
            else:
                break
        return None

    return codepath_walk(start_addr, start_symbols, [], 0)

def rax_is_one(symbols):
    if symbols[ExprId("RIP", 64)] == ExprMem(ExprId("RSP_init", 64), 64):
        if symbols[ExprId("RAX", 64)] == ExprInt64(1):
            return True
    return False

test_code = """
.text
L_MAIN:
    MOV RAX, 0
    CMP RDI, 2010
    JNZ L_END
    CMP RSI, 12
    JNZ L_END
    CMP RDX, 20
    JNZ L_END
    XOR RCX, RDI
    XOR RCX, RSI
    XOR RCX, RDX
    CMP RCX, 763
    JNZ L_END
    INC RAX
L_END:
    RET
"""

def main():
    buf = assemble_text(test_code, [("L_MAIN", 0)])
    mdis = dis_engine(buf)

    disasm = mdis.dis_multibloc(0)
    ir = ir_a_x86_64(mdis.symbol_pool)
    for bbl in disasm:
        ir.add_bloc(bbl)

    symbols_init =  {}
    for i, r in enumerate(all_regs_ids):
        symbols_init[r] = all_regs_ids_init[i]

    conds = find_goal(ir, 0, symbols_init, rax_is_one)
    if conds == None:
        print "Goal was not found"
        sys.exit(-1)

    solver = z3.Solver()
    for lval, rval in conds:
        z3_cond = Translator.to_language("z3").from_expr(lval)
        solver.add(z3_cond == int(rval.arg))
    rslt = solver.check()
    if rslt == z3.sat:
        m = solver.model()
        for var in m:
            print "%s: %d" % (var.name(), m[var].as_long())
    else:
        print "No solution"
        sys.exit(-1)

if __name__ == "__main__":
    main()

