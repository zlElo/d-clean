import os
import subprocess
from disk_filler import overwriter

def outliner(output_):
    print('')
    # Calculate the width of the box based on the length of the longest line in the output
    box_width = max(len(line) for line in output_.split('\n')) + 2

    # Print the top border of the box
    print('+' + '-' * box_width + '+')

    # Print the content of the box with vertical lines on the sides
    for line in output_.split('\n'):
        print('|' + line.ljust(box_width) + '|')

    # Print the bottom border of the box
    print('+' + '-' * box_width + '+')


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



def encrypt(file):
    have_to_encrypt = open(file, "rb").read()
    key = os.urandom(100000)
    encryptet = bytes(a ^ b for (a, b) in zip(have_to_encrypt, key))
    with open(file, "wb") as encryptet_out:
        encryptet_out.write(encryptet)


def find_select_encrypt(selected_drive, second_selected_drive, bar, actual_progress_info, window):

    bar.set(0.1)
    
    if not os.path.exists(selected_drive):
        print("Drive not found.")
        exit()

    # check if drive is available
    if os.path.splitdrive(selected_drive)[0] == os.environ['SYSTEMDRIVE']:
        print("Wasnt able to select drive")
        exit()

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


