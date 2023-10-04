import customtkinter
from handler import find_select_encrypt
import pyuac
import os
import subprocess
import threading



def starting_progress(drive_letter_combo_box, drive_number_combo_box, bar, actual_progress_info, root):

    selected_drive = drive_letter_combo_box.get()
    print(selected_drive)

    second_selected_drive = drive_number_combo_box.get()
    print(selected_drive)

    delete_thread = threading.Thread(target=lambda: find_select_encrypt(selected_drive, second_selected_drive, bar, actual_progress_info, root))
    delete_thread.start()



def info_btn_window():
    result_ = subprocess.run(['diskpart', '/s', 'src\list_disk.txt'], capture_output=True, text=True)
    output_ = result_.stdout

    root = customtkinter.CTk()
    root.title('INFO')
    customtkinter.set_default_color_theme("green")

    customtkinter.CTkLabel(root, text=output_).pack(pady=30, padx=30)

    root.mainloop()


def GUI():
    root = customtkinter.CTk()
    root.title('D-CLEAN')
    root.geometry('340x350')
    customtkinter.set_default_color_theme("green")

    # get drives
    drives = ['%s:' % d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists('%s:' % d)]
    value_combo = []

    for drive in drives:
        value_combo.append(drive)

    # add drive numbers to list
    drive_number = len(value_combo)
    drive_numbers_value = [str(i) for i in range(drive_number)]

    # GUI
    customtkinter.CTkLabel(root, text='D-CLEAN  -  To actually wipe your hard drive').pack(pady=10)

    # Frame
    frame = customtkinter.CTkFrame(root)
    frame.pack(pady=10)
    

    customtkinter.CTkLabel(frame, text='Drive letter:').pack(padx=80)
    drive_letter_combo_box = customtkinter.CTkComboBox(frame, values=value_combo)
    drive_letter_combo_box.pack()

    customtkinter.CTkLabel(frame, text='Drive number:').pack(pady=10)
    drive_number_combo_box = customtkinter.CTkComboBox(frame, values=drive_numbers_value)
    drive_number_combo_box.pack()

    info_btn = customtkinter.CTkButton(frame, text='ⓘ', width=10, command=info_btn_window)
    info_btn.place(x=10, y=104)


    # Slider for future feature
    #slider_label = customtkinter.CTkLabel(frame, text='Security level:')
    #slider_label.pack(pady=10)

    #slider = customtkinter.CTkSlider(frame)
    #slider.pack()


    start_btn = customtkinter.CTkButton(frame, text='Start wiping', command=lambda: starting_progress(drive_letter_combo_box, drive_number_combo_box, bar, actual_progress_info, root))
    start_btn.pack(pady=20)

    
    # Not frame content

    progress_label = customtkinter.CTkLabel(root, text='Progress:')
    progress_label.pack()

    bar = customtkinter.CTkProgressBar(root)
    bar.pack()

    actual_progress_info = customtkinter.CTkLabel(root, text='/')
    actual_progress_info.pack()

    

    root.mainloop()


# start of program with adnib rights check
if pyuac.isUserAdmin():
    GUI()
else:
    pyuac.runAsAdmin()