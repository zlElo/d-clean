import os
import subprocess
import pyuac
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


def delete_gpt_mbr():

    result_ = subprocess.run(['diskpart', '/s', 'src\list_disk.txt'], capture_output=True, text=True)
    output_ = result_.stdout
    outliner(output_)


    selected_drive = input('\nEnter number of drive: ')


    # write into files
    with open('src\del_drive.txt', 'w') as f:
        command_to_write = f'sel disk {selected_drive}\nclean\ncreate partition primary\nformat quick fs=ntfs'
        f.write(command_to_write)

    with open('src\delete_gpt.txt', 'w') as f:
        command_to_write = f'sel disk {selected_drive}\nclean'
        f.write(command_to_write)

    with open('src\delete_mbr.txt', 'w') as f:
        command_to_write = f'sel disk {selected_drive}\nclean\nconvert gpt'
        f.write(command_to_write)
        
    with open('src\clean_all.txt', 'w') as f:
        command_to_write = f'sel disk {selected_drive}\nclean all'
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


def find_select_encrypt():
    drives = ['%s:' % d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists('%s:' % d)]

    print("Available drives:")
    for drive in drives:
        print(drive)

    selected_drive = input("Enter Letter of Drive (for example D:): ")
    
    if not os.path.exists(selected_drive):
        print("Drive not found.")
        exit()

    # Überprüfen, ob das ausgewählte Laufwerk das Systemlaufwerk ist
    if os.path.splitdrive(selected_drive)[0] == os.environ['SYSTEMDRIVE']:
        print("Wasnt able to select drive")
        exit()

    print('\n\nFiles to encrypt:\n')
    for root, dirs, files in os.walk(selected_drive):
        for file in files:
            chosen_file = os.path.join(root, file)
            print(chosen_file)
            encrypt(chosen_file)


    # delete functions
    for i in range(3):
        delete_gpt_mbr()
        overwriter(selected_drive)

    
    # make full clean
    subprocess.run(['diskpart', '/s', 'src\clean_all.txt'])


    print('\n\n\n\n################### \- Progress done -/ ###################')


    input('\nPress enter to exit...')


if pyuac.isUserAdmin():
    find_select_encrypt()
else:
    pyuac.runAsAdmin()


