import os
import subprocess
from disk_filler import overwriter
import customtkinter


# function to continue after warning with os drive
def go(root):
    root.destroy()

# function to cancel after warning with os drive
def cancel(root, window):
    window.destroy()
    root.destroy()
    exit()

# os drive error
def error_os_drive(window):
    root = customtkinter.CTk()
    root.title('ATTENTION!')

    customtkinter.CTkLabel(root, text='The selected drive contains an OS, are you sure to continue?').pack(padx=30, pady=10)

    customtkinter.CTkButton(root, text='yes', fg_color='red', hover_color='salmon', command=lambda: go(root)).pack(pady=15, padx=36, side='left')
    customtkinter.CTkButton(root, text='no', fg_color='green', hover_color='yellowgreen', command=lambda: cancel(root, window)).pack(pady=15, padx=10, side='left')

    root.mainloop()




def delete_gpt_mbr(second_selected_drive): # selected drive is in this code snippet the number of the diskpart info

    # write into files
    with open('src\del_drive.txt', 'w') as f:
        command_to_write = f'sel disk {second_selected_drive}\nclean\ncreate partition primary\nformat quick fs=ntfs'
        f.write(command_to_write)

    with open('src\delete_gpt.txt', 'w') as f:
        command_to_write = f'sel disk {second_selected_drive}\nclean'
        f.write(command_to_write)

    with open('src\delete_mbr.txt', 'w') as f:
        command_to_write = f'sel disk {second_selected_drive}\nclean\nconvert gpt'
        f.write(command_to_write)
        
    with open('src\clean_all.txt', 'w') as f:
        command_to_write = f'sel disk {second_selected_drive}\nclean all'
        f.write(command_to_write)


    print('\n\n###############DISKPART OUTPUT###############\n')

    subprocess.run(['diskpart', '/s', 'src\delete_gpt.txt'])
    
    subprocess.run(['diskpart', '/s', 'src\delete_mbr.txt'])

    subprocess.run(['diskpart', '/s', 'src\del_drive.txt'])

# function to encrypt a file with 100.000 random key
def encrypt(file):
    have_to_encrypt = open(file, "rb").read()
    key = os.urandom(100000)
    encryptet = bytes(a ^ b for (a, b) in zip(have_to_encrypt, key))
    with open(file, "wb") as encryptet_out:
        encryptet_out.write(encryptet)

# main handler
def find_select_encrypt(selected_drive, second_selected_drive, bar, actual_progress_info, window):

    bar.set(0.1)
    
    if not os.path.exists(selected_drive):
        print("[log] Drive not found.")
        exit()

    # check if drive is available
    if os.path.splitdrive(selected_drive)[0] == os.environ['SYSTEMDRIVE']:
        print("[log] Wasnt able to select drive")
        error_os_drive(window)
        

    print('\n\nFiles to encrypt:\n')
    for root, dirs, files in os.walk(selected_drive):
        for file in files:
            chosen_file = os.path.join(root, file)
            print(chosen_file)
            encrypt(chosen_file)
            actual_progress_info.configure(text=f'encrypt: {chosen_file}')

    bar.set(0.2)

    steps = 0.2
    step_ = 0

    # delete functions
    for i in range(3):
        steps += 0.1
        step_ += 1

        bar.set(steps)
        actual_progress_info.configure(text=f'({step_}/3) Delete mbr')
        delete_gpt_mbr(second_selected_drive)
        
        bar.set(steps)
        actual_progress_info.configure(text=f'({step_}/3) Fill the full drive with files')
        overwriter(selected_drive)
        

    steps += 0.2
    actual_progress_info.configure(text=f'set to 0')
    # make full clean
    subprocess.run(['diskpart', '/s', 'src\clean_all.txt'])
    bar.step(steps)


    print('\n\n\n\n################### \- Progress done -/ ###################')


