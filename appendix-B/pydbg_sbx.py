# -*- coding: utf-8 -*-

from pydbg import *
from pydbg.defines import *
import sys
import struct
import pefile

def hook_CreateFileA(dbg):

    ret = dbg.read_process_memory(dbg.context.Esp,4)
    retaddr = struct.unpack("L",ret)[0]

    arg = dbg.read_process_memory(dbg.context.Esp+4,4)
    arg_addr = struct.unpack("L",arg)[0]

    retaddr = int(retaddr)
    arg_addr = int(arg_addr)
    if retaddr < 0x70000000:

        offset = 0
        buffer = ""
        while 1:
            byte = dbg.read_process_memory(arg_addr+offset, 1)
            if byte == '\00':
                break
            else:
                buffer += byte
                offset += 1
        print "pydbgSbx:@0x%08x CreateFileA(%s,...)" % (retaddr, buffer)

    return DBG_CONTINUE

def hook_install(dbg):

    hook_addr = dbg.func_resolve("kernel32.dll","CreateFileA")

    dbg.bp_set(hook_addr, handler=hook_CreateFileA)
    return DBG_CONTINUE

def main():

    target = sys.argv[1]
    dbg = pydbg()
    dbg.load(target, " ".join(sys.argv[2:]))

    pe = pefile.PE(target)
    entrypoint = pe.OPTIONAL_HEADER.ImageBase + pe.OPTIONAL_HEADER.AddressOfEntryPoint
    dbg.bp_set(entrypoint,handler=hook_install)
    dbg.run()

if __name__ == '__main__':
    main()
