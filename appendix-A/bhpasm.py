# -*- coding: utf-8 -*-

from miasm2.analysis.machine import Machine
from miasm2.core import parse_asm, asmbloc
from elfesteem.strpatchwork import StrPatchwork
def assemble_text(src_text, symbols=[], mach_name="x86_64", mach_attr=64):
    # 指定アーキテクチャのニーモニックを取得
    mnemo = Machine(mach_name).mn
    # セクションとシンボルの取得
    sections, symbol_pool = parse_asm.parse_txt(mnemo, mach_attr, src_text)
    # シンボル毎のアドレスを設定
    for name, addr in symbols:
        symbol_pool.set_offset(symbol_pool.getby_name(name), addr)
    # アセンブル
    patches = asmbloc.asm_resolve_final(mnemo, sections[0], symbol_pool)
    # アセンブル結果の構築
    patch_worker = StrPatchwork()
    for offset, raw in patches.items():
        patch_worker[offset] = raw

    return str(patch_worker)

import ctypes
def execute_native_code(native_code):
    # libcを準備
    libc = ctypes.CDLL('libc.so.6')
    libc.mprotect.restype = ctypes.c_int
    libc.mprotect.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int]
    # ネイティブコード用のバッファを作成
    native_buf = ctypes.create_string_buffer(native_code, len(native_code))
    # メモリページのアドレスとページ数の計算
    native_addr = ctypes.addressof(native_buf)
    page_size = libc.getpagesize()
    page_addr = native_addr / page_size * page_size
    page_num = (native_addr + len(native_code) - 1) / page_size + 1
    # 実行権限の付与
    libc.mprotect(page_addr, page_num * page_size, 0x7)
    # 実行
    ctypes.cast(native_buf, ctypes.CFUNCTYPE(None))()

asm_helloworld = """
.text
L_MAIN:
    MOV RAX, 1      ; sys_writeを指定
    MOV RDI, 1      ; 標準出力のファイル記述子(1)を設定
    CALL L1
    .string "Hello, world.\\n"
L1:
    POP RSI         ; 文字列のアドレスを設定
    MOV RDX, 14     ; 文字数の設定
    SYSCALL         ; システムコールの呼び出し
    RET
"""

if __name__ == "__main__":
    native_code = assemble_text(asm_helloworld, [("L_MAIN", 0)])
    execute_native_code(native_code)
