import os
import time
import itertools
import threading
import queue

charlist = ("A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "]", "[", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "{", "}", "|", ":", ";", "\"", "'", "<", ">", ",", ".", "?", "/", "~", "`", " ", "\\", " ")
additionalchar = ("¡", "¢", "£", "¤", "¥", "¦", "§", "¨", "©", "ª", "«", "¬", "®", "¯", "°", "±", "²", "³", "´", "µ", "¶", "·", "¸", "¹", "º", "»", "¼", "½", "¾", "¿", "Ñ", "ñ", "Ç", "ç", "Ö", "ö", "Ü", "ü", "Ä", "ä", "ß", "Α", "Β", "Γ", "Δ", "Ε", "Ζ", "Η", "Θ", "Ι", "Κ", "Λ", "Μ", "Ν", "Ξ", "Ο", "Π", "Ρ", "Σ", "Τ", "Υ", "Φ", "Χ", "Ψ", "Ω", "α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ", "λ", "μ", "ν", "ξ", "ο", "π", "ρ", "σ", "τ", "υ", "φ", "χ", "ψ", "ω")
BASE_CHAR_SET = set(charlist)
ADDITIONAL_CHAR_SET = set(additionalchar)
EXTENDED_CHARSET = charlist + tuple(ch for ch in additionalchar if ch not in BASE_CHAR_SET)
passlist = ("1234", "password", "letmein", "qwerty", "abc123", "welcome", "admin", "login", "123456", "iloveyou", "welcome1", "password1", "12345", "123456789", "football", "monkey", "dragon", "baseball", "master", "hello", "freedom", "whatever", "qazwsx", "trustno1", "")
target_password = input("Enter the password to crack: ")
printmode = input("Enable print mode? (True/False): ").strip().lower() == 'true'
maxlength = len(target_password)

found_event = threading.Event()
print_lock = threading.Lock()
MAX_WORKERS = min(32, (os.cpu_count() or 1) * 2)
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


def enqueue_tasks(charset, task_queue):
    char_len = len(charset)
    for length in range(1, maxlength + 1):
        for start in range(0, char_len, CHARS_PER_TASK):
            end = min(start + CHARS_PER_TASK, char_len)
            task_queue.put((length, start, end))


def checks_worker(charset, task_queue):
    while not found_event.is_set():
        try:
            length, start, end = task_queue.get_nowait()
        except queue.Empty:
            return

        first_slice = charset[start:end]

        if length == 1:
            for ch in first_slice:
                if attempt_password(ch):
                    return
                if found_event.is_set():
                    return
            continue

        iterables = [first_slice] + [charset] * (length - 1)
        for attempt in itertools.product(*iterables):
            candidate = ''.join(attempt)
            if attempt_password(candidate):
                return
            if found_event.is_set():
                return


def run_checks_with_charset(charset):
    found_event.clear()
    task_queue = queue.Queue()
    enqueue_tasks(charset, task_queue)
    threads = []

    worker_count = min(MAX_WORKERS, len(charset))
    for _ in range(worker_count):
        thread = threading.Thread(target=checks_worker, args=(charset, task_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return found_event.is_set()


def trypassword():
    if target_password in passlist:
        print(f"Password found in password list: {target_password}")
        return
    contains_only_base_chars = all(ch in BASE_CHAR_SET for ch in target_password)

    if not contains_only_base_chars:
        print("Detected characters outside the base character set. Running expanded search...")
        if run_checks_with_charset(EXTENDED_CHARSET):
            return
        print("Password not found within the specified length range.")
        return

    if run_checks_with_charset(charlist):
        return

    if any(ch in ADDITIONAL_CHAR_SET for ch in target_password):
        print("Password appears to need additional characters. Expanding search...")
    else:
        print("Base character set exhausted, expanding search as a fallback...")

    if run_checks_with_charset(EXTENDED_CHARSET):
        return

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