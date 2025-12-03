import itertools

charlist = ["A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "]", "[", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "{", "}", "|", ":", ";", "\"", "'", "<", ">", ",", ".", "?", "/", "~", "`", " ", "\\"]
password = ""
maxlength = int(input("Enter maximum password length: "))

def trypassword():
    global password
    for i in range(1, maxlength + 1):
        for attempt in itertools.product(charlist, repeat=i):
            password = ''.join(attempt)
            print(f"Trying password: {password}")
            if(False):  # Replace False with actual password check condition):
                print("Process interrupted by user.")
                return
    print("Password generation completed.")

trypassword()