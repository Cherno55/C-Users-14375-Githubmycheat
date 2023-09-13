import pymem
import pymem.process
import tkinter as tk
from tkinter import ttk
from threading import Thread

# Updated Offsets from hazedumper
dwEntityList = 0x4E0102C
dwGlowObjectManager = 0x535BAD0
m_iGlowIndex = 0x10488
m_iTeamNum = 0xF4

glow_active = True  # Global switch for glow

def cheat_thread():
    print("Cheat Thread Running.")
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    while glow_active:
        glow_manager = pm.read_int(client + dwGlowObjectManager)
        for i in range(1, 32):  # Entities 1-32 are reserved for players.
            entity = pm.read_int(client + dwEntityList + i * 0x10)
            if entity:
                entity_team_id = pm.read_int(entity + m_iTeamNum)
                entity_glow = pm.read_int(entity + m_iGlowIndex)
                
                if entity_team_id == 2:  # Terrorist
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(1))   # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))   # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(0))  # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)           # Enable glow

                elif entity_team_id == 3:  # Counter-terrorist
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))   # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)           # Enable glow

def toggle_glow():
    global glow_active
    glow_active = not glow_active
    if glow_active:
        print("Glow Activated!")
        Thread(target=cheat_thread).start()  # Starting the cheat in a separate thread
    else:
        print("Glow Deactivated!")

def create_gui():
    root = tk.Tk()
    root.title("Cheat Control Panel")

    # Add a label
    label = ttk.Label(root, text="CSGO ESP System")
    label.pack(pady=20)

    # Add a toggle glow button
    toggle_button = ttk.Button(root, text="Toggle Glow", command=toggle_glow)
    toggle_button.pack(pady=20)

    root.mainloop()

if __name__ == '__main__':
    create_gui()
