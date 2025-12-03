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
    if printmode == True:
        with print_lock:
            print(f"Trying password: {candidate}")
    if check_password(candidate):
        with print_lock:
            print(f"Password found: {candidate}")
        found_event.set()
        return True
    return False


def brute_force_worker(prefixes):
    for first_char in prefixes:
        for length in range(1, maxlength + 1):
            if found_event.is_set():
                return

            if length == 1:
                if attempt_password(first_char):
                    return
                continue

            for suffix in itertools.product(charlist, repeat=length - 1):
                if attempt_password(first_char + ''.join(suffix)):
                    return


def chunked(sequence, chunk_size):
    for index in range(0, len(sequence), chunk_size):
        yield sequence[index:index + chunk_size]


def trypassword():
    thread_count = min(16, len(charlist))
    chunk_size = max(1, (len(charlist) + thread_count - 1) // thread_count)
    threads = []

    for chunk in chunked(charlist, chunk_size):
        thread = threading.Thread(target=brute_force_worker, args=(chunk,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    if not found_event.is_set():
        print("Password not found within the specified length range.")


start_time = time.time()
print(start_time)
trypassword()
end_time = time.time()
print(f"Password \"{target_password}\" took {end_time - start_time} seconds to crack.")