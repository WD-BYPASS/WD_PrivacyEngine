import time
import itertools
import threading

charlist = ["A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "]", "[", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "{", "}", "|", ":", ";", "\"", "'", "<", ">", ",", ".", "?", "/", "~", "`", " ", "\\", " ", "¡", "¢", "£", "¤", "¥", "¦", "§", "¨", "©", "ª", "«", "¬", "®", "¯", "°", "±", "²", "³", "´", "µ", "¶", "·", "¸", "¹", "º", "»", "¼", "½", "¾", "¿"]
target_password = input("Enter the password to crack: ")
printmode = input("Enable print mode? (True/False): ").strip().lower() == 'true'
maxlength = len(target_password)

found_event = threading.Event()
print_lock = threading.Lock()


def check_password(pw):
    return pw == target_password


def attempt_password(candidate):
    if found_event.is_set():
        return True
    if printmode:
        with print_lock:
            print(f"Trying password: {candidate}")
    if check_password(candidate):
        with print_lock:
            print(f"Password found: {candidate}")
        found_event.set()
        return True
    return False


def brute_force_length(length):
    if length <= 0:
        return
    for attempt in itertools.product(charlist, repeat=length):
        if found_event.is_set():
            return
        if attempt_password(''.join(attempt)):
            return


def trypassword():
    threads = []

    for length in range(1, maxlength + 1):
        thread = threading.Thread(target=brute_force_length, args=(length,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    if not found_event.is_set():
        print("Password not found within the specified length range.")


start_hour = int(time.strftime("%H", time.localtime()))
start_minute = int(time.strftime("%M", time.localtime()))
start_second = int(time.strftime("%S", time.localtime()))
start_micro = int(time.strftime("%f", time.localtime()))
start_time = f"{start_hour}:{start_minute}:{start_second}:{start_micro}"
print(start_time)
while input("Press Enter to start cracking the password...") == None:
    pass
trypassword()
end_hour = int(time.strftime("%H", time.localtime())) - start_hour
end_minute = int(time.strftime("%M", time.localtime())) - start_minute
end_second = int(time.strftime("%S", time.localtime())) - start_second
end_micro = int(time.strftime("%f", time.localtime())) - start_micro
end_time = f"{end_hour}hrs:{end_minute}mins:{end_second}secs:{end_micro}ms"
print(f"Password \"{target_password}\" took {end_time} to crack.")