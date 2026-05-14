from PIL import Image
import numpy as np
import os


def str_to_bin(string: str) -> list[str]:
    bin_array = []
    for char in string:
        bin_array.append("0"*(7-len(bin(ord(char))[2:])) + (bin(ord(char))[2:]))
    return bin_array

def inject(image: list, bin_message: list[str]):
    injected_img = []
    bin_msg_copy = "".join(bin_message)
    message_len = bin(len(bin_message)*7)[2:]
    row_len = len(image[0])
    injected_len = []

    #prima riga dedicata alla lunghezza ([..., miliardi, milioni, migliaia, centinaia, decine, unita])

    for counter, pixel in enumerate(image[0]):
        if (row_len - counter) <= len(message_len):
            changed_bin = int(bin(pixel[0])[2:][:-1:] + message_len[0], 2)
            message_len = message_len[1:]
            injected_len.append([changed_bin] + pixel[1:])
        else:
            changed_bin = int(bin(pixel[0])[2:][:-1:] + "0", 2)
            injected_len.append([changed_bin] + pixel[1:])

    injected_img.append(injected_len)
    del injected_len

    #corpo del testo ([..., miliardi, milioni, migliaia, centinaia, decine, unita])

    for y, row in enumerate(image[1:]):
        injected_row = []
        for x, pixel in enumerate(row):
            last_x = x
            if bin_msg_copy:
                changed_bin = int(bin(pixel[0])[2:][:-1:] + bin_msg_copy[0], 2)
                bin_msg_copy = bin_msg_copy[1:]
                injected_row.append([changed_bin] + pixel[1:])
            else:
                injected_img.append(injected_row + image[y+1][last_x:])
                injected_row = []
                break
        if injected_row:
            injected_img.append(injected_row)
        
    return Image.fromarray(np.array(injected_img, dtype=np.uint8))
                

def decode(image: list) -> str:
    found_1 = False
    message = ""
    message_len = ""
    
    #ricavo la lunghezza del messaggio

    for pixel in image[0]:
        if not found_1:
            if not pixel[0] % 2:
                found_1 = True
        else:
            message_len = message_len + str(pixel[0]%2) 
    message_len = int(message_len, 2)

    #cerco il messaggio
    complete_rows = message_len//len(image[0])
    partial_row = message_len % len(image[0])
    char = ""

    for row in image[1: complete_rows+1]:
        for pixel in row:
            if len(char) == 7:
                message += chr(int(char, 2))
                char = ""
            char += bin(pixel[0])[-1]
    
    for pixel in image[complete_rows+1][:partial_row:]:
        if len(char) == 7:
            message += chr(int(char, 2))
            char = ""
        char += bin(pixel[0])[-1]

    message += "" if not char else chr(int(char, 2))

    return message

choice = None
title = "IMAGE TEXT INJECTOR AND DECODER"
title_size = 100

print("-".ljust(title_size, "-"))
print(title.center(title_size))
print("-".ljust(title_size, "-"))
print()
print("[1] : inject text into any image")
print()
print("[2] : decode text injected into an image", end="\n"*3)

while True:
    choice = input("Choose 1/2: ")
    if choice not in "12":
        print("Choice is not valid")
        if input("Type 'exit' to exit(any other key to continue): ") == "exit":
            exit()
    else:
        break

print()

while True:
    try:
        img = np.array(Image.open(input("file address: ").strip().replace("\"", "")))
        print("File was found! ")
        print("Loading...")
        img = img.tolist()
        print("Loaded into memory!")
        break
    except:
        print("File was not found / Is not valid")
        if input("Type 'exit' to exit(any other key to continue): ") == "exit":
            exit()

print()


if choice == "1":
    while True:
        hidden_msg = str_to_bin(input("message to hide: "))
        if len(hidden_msg)*7 > (max_len := 2**len(img[0])) or\
            len(hidden_msg)*7 > (max_len := len(img[0]) * len(img[1:])):
        
            print(f"message exeeds maximum leght({max_len} char)")
        else:
            break
        if input("Type 'exit' to exit(any other key to continue): ") == "exit":
            exit()
    print("Injecting image...")
    injected_image = inject(img, hidden_msg)
    print("Image injected successfully")
    target_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "injected_imgs")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    injected_image.save(os.path.join(target_dir, "injected_img.png"), quality = 100)
    print(f"Image saved in the folder {target_dir}")
else:
    print("Decoding image...")
    decoded_text = decode(img)
    print("Text decoded successfully")
    print(f"decoded text: {decoded_text}")


input()






