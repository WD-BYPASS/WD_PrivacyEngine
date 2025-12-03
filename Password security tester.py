import itertools
import threading

charlist = ["A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "]", "[", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "{", "}", "|", ":", ";", "\"", "'", "<", ">", ",", ".", "?", "/", "~", "`", " ", "\\", " ", "¡", "¢", "£", "¤", "¥", "¦", "§", "¨", "©", "ª", "«", "¬", "®", "¯", "°", "±", "²", "³", "´", "µ", "¶", "·", "¸", "¹", "º", "»", "¼", "½", "¾", "¿"]
password = input("Enter the password to crack: ")
maxlength = int(input("Enter maximum password length: "))

def check_password(pw):
    # Placeholder for actual password checking logic
    # For demonstration, let's assume the correct password is "Ab1!"
    correct_password = password
    return pw == correct_password

def trypassword():
    global password
    for length in range(1, maxlength + 1):
        for attempt in itertools.product(charlist, repeat=length):
            password = ''.join(attempt)
            print(f"Trying password: {password}")
            if check_password(password):
                print(f"Password found: {password}")
                return

trypassword()