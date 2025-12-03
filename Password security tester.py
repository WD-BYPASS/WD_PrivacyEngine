import time
import itertools
import threading
import queue

charlist = ("A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "]", "[", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "{", "}", "|", ":", ";", "\"", "'", "<", ">", ",", ".", "?", "/", "~", "`", " ", "\\", " ", "¡", "¢", "£", "¤", "¥", "¦", "§", "¨", "©", "ª", "«", "¬", "®", "¯", "°", "±", "²", "³", "´", "µ", "¶", "·", "¸", "¹", "º", "»", "¼", "½", "¾", "¿")
passlist = ("1234", "password", "letmein", "qwerty", "abc123", "welcome", "admin", "login", "123456", "iloveyou", "welcome1", "password1", "12345", "123456789", "football", "monkey", "dragon", "baseball", "master", "hello", "freedom", "whatever", "qazwsx", "trustno1", "")
target_password = input("Enter the password to crack: ")
printmode = input("Enable print mode? (True/False): ").strip().lower() == 'true'
maxlength = len(target_password)

found_event = threading.Event()
print_lock = threading.Lock()
task_queue = queue.Queue()
MAX_WORKERS = min(32, len(charlist))
CHARS_PER_TASK = 4


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


def enqueue_tasks():
    for length in range(1, maxlength + 1):
        for start in range(0, len(charlist), CHARS_PER_TASK):
            end = min(start + CHARS_PER_TASK, len(charlist))
            task_queue.put((length, start, end))


def brute_force_worker():
    while not found_event.is_set():
        try:
            length, start, end = task_queue.get_nowait()
        except queue.Empty:
            return

        first_slice = charlist[start:end]

        if length == 1:
            for ch in first_slice:
                if attempt_password(ch):
                    return
                if found_event.is_set():
                    return
            continue

        iterables = [first_slice] + [charlist] * (length - 1)
        for attempt in itertools.product(*iterables):
            if attempt_password(''.join(attempt)):
                return
            if found_event.is_set():
                return


def trypassword():
    if target_password in passlist:
        print(f"Password found in password list: {target_password}")
        return
    if target_password in charlist:
        print(f"Password found in character list: {target_password}")
        return
    enqueue_tasks()
    threads = []

    for _ in range(MAX_WORKERS):
        thread = threading.Thread(target=brute_force_worker)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    if not found_event.is_set():
        print("Password not found within the specified length range.")



input("Press Enter to start cracking the password...")
current_time_nanoseconds = time.time_ns()
current_time_microseconds = current_time_nanoseconds // 1000
start_hour = int(time.strftime("%H", time.localtime()))
start_minute = int(time.strftime("%M", time.localtime()))
start_second = int(time.strftime("%S", time.localtime()))
start_micro = int(current_time_microseconds)
trypassword()
current_time_nanoseconds = time.time_ns()
current_time_microseconds = current_time_nanoseconds // 1000
end_hour = int(time.strftime("%H", time.localtime())) - start_hour
end_minute = int(time.strftime("%M", time.localtime())) - start_minute
end_second = int(time.strftime("%S", time.localtime())) - start_second
if end_second < 0:
    end_second += 60
    end_minute -= 1
if end_minute < 0:
    end_minute += 60
    end_hour -= 1
end_micro = int(current_time_microseconds) - start_micro
end_time = f"{end_hour}hrs: {end_minute}mins: {end_second}secs: {end_micro}ms"
print(f"Password \"{target_password}\" took {end_time} to crack.")