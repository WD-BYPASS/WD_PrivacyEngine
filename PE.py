import itertools
import threading

charlist = ["A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "]", "[", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "{", "}", "|", ":", ";", "\"", "'", "<", ">", ",", ".", "?", "/", "~", "`", " ", "\\", " ", "¡", "¢", "£", "¤", "¥", "¦", "§", "¨", "©", "ª", "«", "¬", "®", "¯", "°", "±", "²", "³", "´", "µ", "¶", "·", "¸", "¹", "º", "»", "¼", "½", "¾", "¿"]
password = ""
maxlength = int(input("Enter maximum password length: "))

def trypassword():
    global password
    for length in range(1, maxlength + 1):
        for attempt in itertools.product(charlist, repeat=length):
            password = ''.join(attempt)
            print(f"Trying password: {password}")
            # Here you would add the code to test the password against the target system
            # For example, attempting to log in or decrypt a file
            # If the password is correct, you can break out of the loops
            # if test_password(password):
            #     print(f"Password found: {password}")
            #     return

trypassword()