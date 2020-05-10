# author: 11asi11
# first release date: 10.5.2020
import os
from colorama import Fore
from PIL import Image


def banner():
    return """


 ██▓███ ▓██   ██▓ ██▓███   ██▓ ▄████▄  
▓██░  ██▒▒██  ██▒▓██░  ██▒▓██▒▒██▀ ▀█  
▓██░ ██▓▒ ▒██ ██░▓██░ ██▓▒▒██▒▒▓█    ▄ 
▒██▄█▓▒ ▒ ░ ▐██▓░▒██▄█▓▒ ▒░██░▒▓▓▄ ▄██▒
▒██▒ ░  ░ ░ ██▒▓░▒██▒ ░  ░░██░▒ ▓███▀ ░
▒▓▒░ ░  ░  ██▒▒▒ ▒▓▒░ ░  ░░▓  ░ ░▒ ▒  ░
░▒ ░     ▓██ ░▒░ ░▒ ░      ▒ ░  ░  ▒   
░░       ▒ ▒ ░░  ░░        ▒ ░░        
         ░ ░               ░  ░ ░      
         ░ ░                  ░        

"""


def status_fail():
    return Fore.WHITE + "[" + Fore.RED + " FAILED " + Fore.WHITE + "]"


def status_ok():
    return Fore.WHITE + "[" + Fore.GREEN + " OK " + Fore.WHITE + "]"


def status_note():
    return Fore.WHITE + "[ * ]"


def get_pic_pixels(path):
    pic_reader = Image.open(path)
    pic_pixels = []  # create a list of bytes that will contain the pixels of the pic
    # pic_pixels format example:
    # [
    #   [255, 255, 255, 255],
    #   [0, 0, 0, 255],
    #   [128, 128, 0, 255],
    #   ...
    #   [0, 0, 0, 255]
    # ]
    for y in range(pic_reader.size[1]):
        for x in range(pic_reader.size[0]):
            pixel = list(pic_reader.getpixel((x, y)))  # convert the pixel from tuple to list
            pic_pixels.append(pixel)  # append the pixel to the pic bytes list
    return pic_pixels  # return the pic bytes content


def get_hidden_byte_from_pixel(pixel):
    hidden_byte = ""
    for byte in pixel:
        str_byte = byte_to_str(byte)  # convert the byte to str to get access to the bits
        hidden_byte += str(str_byte[6]) + str(str_byte[7])  # add the last to bits from the byte
    return int(hidden_byte, 2)  # convert the str to int in base 2 (binary)


def byte_to_str(byte):
    str_byte = bin(byte)  # convert the byte to bin format (0b11110000)
    str_byte = str_byte.split('b')[1]  # remove the "0b" from the bin format (11110000)
    str_byte = list(str_byte)  # convert to list in order to insert bits
    while len(str_byte) < 8:
        str_byte.insert(0, "0")  # format the byte str length to 8 by adding "0" bits to the beginning of the str
    str_byte = "".join(str_byte)  # convert from list back to str
    return str_byte  # return the byte as str in the next format: "00010110"


def str_to_byte(str_byte):
    byte = int(str_byte, 2)  # convert the str byte to an int in base 2 (binary)
    return byte  # return the byte value (0-255)


def rewrite_pixel(pixel, byte):
    # hide the byte inside the pixel
    i = 0
    new_pixel = []
    str_byte = byte_to_str(byte)  # convert the byte to str in order to access each bit
    for b in pixel:
        _2bit = [str_byte[i], str_byte[i + 1]]  # get 2 bits from the byte to write inside 1 pixel byte
        new_pixel.append(rewrite_byte(b, _2bit))  # rewrite the pixel byte and save to the new pixel
        i += 2
    return new_pixel  # return the new pixel with the hidden byte


def rewrite_byte(byte, _2bit):
    byte = byte_to_str(byte)  # convert the byte to str
    bits = list(byte)  # convert the byte to a list of bits
    bits[6] = str(_2bit[0])  # rewrite the last 2 bits
    bits[7] = str(_2bit[1])
    bits = "".join(bits)  # convert the bits to str
    bits = str_to_byte(bits)  # convert the str bits back to byte
    return bits  # return the bits as a byte


def request_pic_path(output):
    while True:
        pic_path = input(Fore.WHITE + output + Fore.GREEN)
        pic_type = os.path.splitext(pic_path)[1]  # get the pic file type
        if not os.path.exists(pic_path) or not os.path.isfile(pic_path):  # if the pic was not found
            print(status_fail() + " file not found")
        elif pic_type.lower() != ".png":  # if the pic is not in supported format
            print(status_fail() + " file is not in supported format")
            print(status_note() + " supported file formats are: png")
        else:  # if the file was found without errors
            break
    print(status_ok() + " pic found")
    return pic_path


def request_file_path(output):
    while True:
        file_path = input(Fore.WHITE + output + Fore.GREEN)
        if not os.path.exists(file_path) or not os.path.isfile(file_path):  # if the file was not found
            print(status_fail() + " file not found")
        else:  # if the file was found without errors
            break
    print(status_ok() + " file found")
    return file_path


def hide_in_pic():
    # get the file path
    file_path = request_file_path("enter the file path you want to hide inside a pic: ")
    file_reader = open(file_path, "rb")
    file_size = os.path.getsize(file_path)
    # to hide 1 byte 1 pixel is required and because of that the file size in bytes is the required pic pixel count
    print(Fore.WHITE + "file size: " + Fore.GREEN + str(file_size) + " bytes")
    print(Fore.WHITE + "min pic required pixel count: " + Fore.GREEN + str(file_size) + " pixels")
    # get the pic path
    pic_path = None
    pic_reader = None
    while True:
        pic_path = request_pic_path("enter the pic path you want to hide the file in: ")
        pic_reader = Image.open(pic_path)
        pic_pixel_count = pic_reader.size[0] * pic_reader.size[1]
        if pic_pixel_count > file_size:  # if the pic is big enough for the file
            print(status_ok() + " pic is large enough")
            break
        else:
            print(status_fail() + " pic is too small choose a larger one")
    print(Fore.WHITE + "pic's resolution: " + Fore.GREEN + str(pic_reader.size[0]) + "x" + str(pic_reader.size[1]))
    print(Fore.WHITE + "pic's pixel count: " + Fore.GREEN + str(pic_reader.size[0] * pic_reader.size[1]) + " pixels")
    input(Fore.WHITE + "press <ENTER> to continue...")
    # hide the file inside the pic
    print(status_note() + " loading file")
    file_bytes = file_reader.read()  # get the file bytes
    print(status_ok() + " file loaded")
    print(status_note() + " loading pic")
    pic_pixels_with_file = get_pic_pixels(pic_path)  # get the pic pixels into a list of pixels
    print(status_ok() + " pic loaded")

    print(status_note() + " hiding file inside the pic")
    for i in range(len(file_bytes)):
        pixel = pic_pixels_with_file[i]
        byte = file_bytes[i]
        pic_pixels_with_file[i] = rewrite_pixel(pixel, byte)  # change hide inside each pixel 1 byte of the file bytes
    print(status_ok() + " file is hidden")

    new_pic = Image.new(mode="RGBA", size=pic_reader.size, color="white")  # create a new pic to hide the file in
    new_pic_pixels = new_pic.load()  # create pixel access object to edit the new pic pixels
    i = 0
    for y in range(new_pic.size[1]):
        for x in range(new_pic.size[0]):
            pixel = pic_pixels_with_file[i]  # get the pixel with the hidden file byte
            new_pic_pixels[x, y] = tuple(pixel)  # (int(pixel[0], 2), int(pixel[1], 2), int(pixel[2], 2), int(pixel[3], 2))
            i += 1

    # save the pic with the hidden file
    while True:
        new_pic_save_path = input(Fore.WHITE + "enter the path you want to save the pic in: " + Fore.GREEN)
        try:
            new_pic.save(new_pic_save_path)
            break
        except():
            print(status_fail() + " failed saving the pic at the specified path")
    print(Fore.WHITE + "pic saved to " + Fore.GREEN + new_pic_save_path)


def read_from_pic():
    print(status_note() + " please note that you will probably get some additional bytes at the end of the extracted " +
                          "file and due to that the extracted file size will probably be larger than " +
                          "the original hidden file")
    pic_path = request_pic_path("enter the pic path you want to extract hidden file from: ")
    pic_reader = Image.open(pic_path)
    # print info about the pic
    print(Fore.WHITE + "pic's resolution: " + Fore.GREEN + str(pic_reader.size[0]) + "x" + str(pic_reader.size[1]) + " pixels")
    print(Fore.WHITE + "pic's pixel count: " + Fore.GREEN + str(pic_reader.size[0] * pic_reader.size[1]) + " pixels")
    print(Fore.WHITE + "pic's file size: " + Fore.GREEN + str(pic_reader.size[0] * pic_reader.size[1] * 4) + " bytes")
    print(Fore.WHITE + "max hidden file size: " + Fore.GREEN + str(pic_reader.size[0] * pic_reader.size[1]) + " bytes")

    # get the pic pixels
    print(status_note() + " loading pic")
    pic_pixels = get_pic_pixels(pic_path)
    print(status_ok() + " pic loaded")

    # get a valid hidden file size
    print(status_note() + " extracting hidden file")
    file_size = None
    max_file_size = pic_reader.size[0] * pic_reader.size[1]
    while True:
        try:
            file_size = int(input(Fore.WHITE + "enter the file size in bytes (0 - " + str(max_file_size) + "): " + Fore.GREEN))
            if file_size > max_file_size:
                print(status_fail() + " hidden file size cant be bigger than max size: " + Fore.GREEN + str(max_file_size) + " bytes")
            elif file_size <= 0:
                print(status_fail() + " hidden file size cant be negative or 0")
            else:
                print(status_ok() + " the size " + Fore.WHITE + " is valid")
                break
        except():
            print(status_fail() + " error occurred the max hidden file size will be used: " + Fore.GREEN + str(max_file_size) + " bytes")
            file_size = max_file_size  # default size is the max size

    input()
    file_bytes = []  # create a byte list for the extracted file bytes

    for i in range(file_size):
        file_bytes.append(get_hidden_byte_from_pixel(pic_pixels[i]))  # extract hidden byte from each pixel and append it to the byte list
    print(status_ok() + " hidden file extracted")

    # save the extracted file bytes into a file
    while True:
        file_save_path = input(Fore.WHITE + "enter the path you want to save the extracted file to: " + Fore.GREEN)
        try:
            with open(file_save_path, "wb") as file_writer:
                file_writer.write(bytes(file_bytes))
            break
        except():
            print(status_fail() + " cant save the hidden file in the specified path")
    print(status_ok() + " extracted file saved to " + Fore.GREEN + file_save_path)


def menu():
    print(Fore.WHITE + "\nMenu:")
    print(Fore.GREEN + "1)" + Fore.WHITE + " hide file inside a pic")
    print(Fore.GREEN + "2)" + Fore.WHITE + " extract hidden file from a pic")
    print(Fore.GREEN + "exit)" + Fore.WHITE + " exit PyPic")
    return input(Fore.WHITE + "choose: " + Fore.GREEN)


def main():
    try:
        print(Fore.RED + banner())
        menu_option = menu()
        if menu_option == "1":
            hide_in_pic()
            pass
        elif menu_option == "2":
            read_from_pic()
            pass
        elif menu_option == "exit":
            exit()
        else:
            print(status_fail() + " unknown command: " + menu_option)
            exit()
    except KeyboardInterrupt:
        print(Fore.RED + "\nInterrupted")
        exit()


if __name__ == '__main__':
    main()

