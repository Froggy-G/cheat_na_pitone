import re
import tkinter.messagebox as mb

from tkinter import *
from pymem import *
from pymem.process import *

window = Tk()
window.title("cheat")
window.geometry('640x480')

unlimited_ammo = False

# USAGE EXAMPLE
# while True:
#   pm.write_int(get_ptr_addr(game_module + 0x0010A280, [0xE4, 0x470]), 20)
def get_ptr_addr(base, offsets):
        addr = pm.read_int(base)
        for i in offsets:
            if i != offsets[-1]:
                addr = pm.read_int(addr + i)
        return addr + offsets[-1]

# USAGE EXAMPLE
# ammo = int(get_sig(
#                       'ac_client.exe',
#                       b'\xFF\x0E\x57\x8B\x7C\x24.\x8D\x74\x24.\xE8....\x5F\x5E\xB0.\x5B\x8B\xE5\x5D\xC2..\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\x55',
#                       ), 0)
#
# pm.write_bytes(ammo, b"\xFF\x0E", 2)
def get_sig(modname, pattern):
    module = pymem.process.module_from_name(pm.process_handle, modname)
    bytes = pm.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
    match = re.search(pattern, bytes).start()
    relative = module.lpBaseOfDll + match
    return "0x{:X}".format(relative)

try:
    pm = Pymem("ac_client.exe")
    game_module = module_from_name(pm.process_handle, "ac_client.exe").lpBaseOfDll

    ammo = int(get_sig(
                        'ac_client.exe',
                        b'\xFF\x0E\x57\x8B\x7C\x24.\x8D\x74\x24.\xE8....\x5F\x5E\xB0.\x5B\x8B\xE5\x5D\xC2..\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\x55',
                        ), 0)

    def unlim_ammo_off():
        pm.write_bytes(ammo, b"\xFF\x0E", 2)

    def unlim_ammo_on():
        pm.write_bytes(ammo, b"\x90\x90", 2)

except pymem.exception.ProcessNotFound:
    print('Could not find process "ac_client.exe"')
    os.system('pause')
    sys.exit()

except pymem.exception.MemoryWriteError:
    print('Process "ac_client.exe" has been closed')
    os.system('pause')
    sys.exit()

lbl_money = Label(window, text="Unlimited ammo", font=("Arial Bold", 16))
lbl_money.grid(column=0, row=0)

btn_add_money = Button(window, text="выкл", command=unlim_ammo_off, font=("Arial Bold", 16))
btn_add_money.grid(column=2, row=0)

btn_sub_money = Button(window, text="вкл", command=unlim_ammo_on, font=("Arial Bold", 16))
btn_sub_money.grid(column=3, row=0)

window.mainloop()