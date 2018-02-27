from PIL import Image
from math import pow, floor
from collections import namedtuple
import sys
from os import path
import numpy as np

dims = namedtuple('ImageDimension', ['width', 'height'])
MAX_LEN = 11
DEBUG = True

def main():
        
    file_name, input_string, mode = arg_check()
    if mode == 'encode':
        encode(file_name, input_string)
    elif mode == 'decode':
        decode(file_name)

def encode(file_name, input_string):
    img, img_dim = pre_process(file_name)
    binary_string = gen_binary(input_string)
    debug("The binary representation of that string has {} bits".format(len(binary_string)))

    debug("{} bits can represent a max value of {}".format(11, pow(2, MAX_LEN) - 1))
    debug("Which is to say a maximum of {} characters".format(floor((pow(2, MAX_LEN) - 1))))
    if len(binary_string) > pow(2, MAX_LEN) - 1:
        debug("ERROR")
        return()
    
    size_bits = bin(len(input_string))[2:]
    debug("Length of message encoded as bits: {}".format(size_bits))
    # print(img[-MAX_LEN:])
    # Set the size bits
    for i in range(-MAX_LEN,0,+1):
        # Unused bits
        if i < -len(size_bits):
            img[i] &= 254
            continue
        # Used bits
        if size_bits[i] == '1':
            img[i] |= 1
        else:
            img[i] &= 254
    
    # print(img[-MAX_LEN:])
    # print(img[-len(binary_string)-MAX_LEN:-MAX_LEN])
    # print(binary_string)
    for i in range(-len(binary_string), 0, +1):
        if binary_string[i] == '1':
            img[i-MAX_LEN] |= 1
        else:
            img[i-MAX_LEN] &= 254
    # print(img[-len(binary_string)-MAX_LEN:-MAX_LEN])

    new_pixels = []
    for i in range(0, len(img), 3):
        new_pixels.append(tuple(img[i:i+3]))

    save = Image.new(mode='RGB', size=(img_dim.width, img_dim.height))
    save.putdata(new_pixels)
    save.save('output.png')

def decode(file_name):
    img, img_dim = pre_process(file_name)

    message_len =[]
    for i in range(-MAX_LEN,0,+1):
        message_len.append(img[i]&1)
    message_len = int("".join([str(bit) for bit in message_len]), 2)
    print(message_len)
    message_len *= 7    # str chars are 7 bits not 8?!?!

    
    message_bits = []
    for i in range(-message_len-MAX_LEN, -MAX_LEN, +1):
        message_bits.append(img[i]&1)
    message = []
    for i in range(0, message_len, 7):
        message.append(chr(int("".join([str(bit) for bit in message_bits[i:i+7]]), 2)))
    message = ''.join(message)
    print(message)
    pass



##########################
#### Helper Functions ####

def arg_check():
    """ Checks argv for input, otherwise set defaults, validates file existance 
    Output: file_name, input_string """

    if len(sys.argv) > 1:
        if len(sys.argv) != 4:
            exit("Wrong arguments \n\nUse: 'stegano <-e|-d> <file_name> <message>'")
        flag = sys.argv[1]
        file_name = sys.argv[2]
        input_string = sys.argv[3]
    else:
        file_name = "output.png"
        input_string = "hello world welcome to steganography"
        mode = 'encode'
        return (file_name, input_string, mode)

    if flag == '-e':
        mode = 'encode'
    elif flag == '-d':
        mode = 'decode'
    else:
        exit("Incorrect or missing flag \n\nUse: 'stegano <-e|-d> <file_name> <message>'")

    if not path.exists(file_name):
        exit("File Doesn't Exist \n\nUse: 'stegano <-e|-d> <file_name> <message>'")
    return (file_name, input_string, mode)

def gen_binary(input_string):
    """ Takens in a string and processes it into its binary representations """

    # First get the binary encoding for each character '0bxxxxxxxx'
    binary_list = list(map(bin, str.encode(input_string)))
    debug("The binary representation is: " + " ".join(binary_list))
    # Remove the leading '0b' and merge all elements
    binary_string = "".join([ truncated[2:].zfill(7) for truncated in binary_list])
    debug("The binary representation is: " + binary_string)
    return binary_string

def pre_process(file_name):
    """ Preprocesses an image by flattening it
    Input: file name
    Output: Flattened image, original dimensions """

    img = Image.open(file_name)
    debug("Loaded image: {}".format(img))
    img_dim = dims(img.size[0], img.size[1])
    debug("Width: {} Height: {}".format(img_dim.width, img_dim.height))
    img = img.getdata()
    debug("Has {} pixels".format(len(img)))

    # todo; outer loop; inner loop
    img_flat = [color_value for pixel in img for color_value in pixel]
    debug(img_flat[:10])
    return(img_flat, img_dim)

def debug(message):
    if DEBUG:
        print("DEBUG: " , message)

if __name__ == "__main__":
    main()
