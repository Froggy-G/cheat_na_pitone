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
    pm = Pymem("Slendytubbies 3 Multiplayer.exe")
    game_module = module_from_name(pm.process_handle, "GameAssembly.dll").lpBaseOfDll

except pymem.exception.ProcessNotFound:
    print('Could not find process')
    os.system('pause')
    sys.exit()

def unlimited_ammo_button():
    global unlimited_ammo

    try:
        ammo_rifle = int(get_sig('GameAssembly.dll',
                                    b'\x0f\x11\x43.\x8b\x40.\x89\x43.\x48\x8b\x15....\xe8....\x48\x8b\x97',
                                    ), 0)
        
        ammo_shotgun = int(get_sig('GameAssembly.dll',
                                    b'\x0f\x11\x43.\x8b\x40.\x89\x43.\x80\x7f',
                                    ), 0)

        ammo_rpg = int(get_sig('GameAssembly.dll',
                                    b'\xff\x48.\x48\x8b\xcf',
                                    ), 0)
        unlimited_ammo = False

    except AttributeError:
        ammo_rifle = int(get_sig('GameAssembly.dll',
                                    b'\x90\x90\x90\x90\x8b\x40.\x89\x43.\x48\x8b\x15....\xe8....\x48\x8b\x97',
                                    ), 0)

        ammo_shotgun = int(get_sig('GameAssembly.dll',
                                    b'\x90\x90\x90\x90\x8b\x40.\x89\x43.\x80\x7f',
                                    ), 0)
        
        ammo_rpg = int(get_sig('GameAssembly.dll',
                                    b'\x90\x90\x90\x48\x8b\xcf',
                                    ), 0)
        unlimited_ammo = True

    if unlimited_ammo:
        pm.write_bytes(ammo_rifle, b"\x0F\x11\x43\x68", 4)
        pm.write_bytes(ammo_shotgun, b"\x0F\x11\x43\x4C", 4)
        pm.write_bytes(ammo_rpg, b"\xFF\x48\x38", 3)
        button_ammo.configure(text="[Выкл]")
        unlimited_ammo = False
    else:
        pm.write_bytes(ammo_rifle, b"\x90\x90\x90\x90", 4)
        pm.write_bytes(ammo_shotgun, b"\x90\x90\x90\x90", 4)
        pm.write_bytes(ammo_rpg, b"\x90\x90\x90", 3)
        button_ammo.configure(text="[Вкл]")
        unlimited_ammo = True

label_ammo = Label(window, text="Unlimited ammo:", font=("Arial Bold", 16))
label_ammo.grid(column=0, row=0)

button_ammo = Button(window, text="[Выкл]", command=unlimited_ammo_button, font=("Arial Bold", 16))
button_ammo.grid(column=1, row=0)

window.mainloop()