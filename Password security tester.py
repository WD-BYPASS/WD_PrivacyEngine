import os
import time
import itertools
import threading
import queue
import math


def parse_bool(value, default=False):
    truthy = {"true", "t", "yes", "y", "1"}
    falsy = {"false", "f", "no", "n", "0"}
    normalized = value.strip().lower() if isinstance(value, str) else ""
    if not normalized:
        return default
    if normalized in truthy:
        return True
    if normalized in falsy:
        return False
    return default


def humanize_number(value):
    if isinstance(value, int):
        if abs(value) < 1_000_000_000_000:
            return f"{value:,}"
        return f"{value:.2e}"
    try:
        numeric = float(value)
    except (TypeError, ValueError, OverflowError):
        return str(value)
    if numeric == 0:
        return "0"
    if abs(numeric) < 1e-3 or abs(numeric) >= 1_000_000_000:
        return f"{numeric:.2e}"
    return f"{numeric:,.3f}"


def format_duration(seconds):
    try:
        seconds = float(seconds)
    except (TypeError, ValueError, OverflowError):
        return str(seconds)

    if seconds < 0:
        seconds = 0.0

    if math.isinf(seconds) or seconds > 9.46e15:  # roughly 300 million years
        return f"{seconds:.2e} seconds"

    if seconds < 1e-3:
        return f"{seconds * 1e6:.2f} µs"
    if seconds < 1:
        return f"{seconds * 1e3:.2f} ms"

    intervals = (
        ("years", 31_557_600),
        ("days", 86_400),
        ("hours", 3_600),
        ("minutes", 60),
        ("seconds", 1),
    )

    parts = []
    remaining = int(seconds)

    for label, unit_seconds in intervals:
        if remaining >= unit_seconds:
            value = remaining // unit_seconds
            remaining -= value * unit_seconds
            unit_label = label[:-1] if value == 1 and label.endswith("s") else label
            parts.append(f"{value} {unit_label}")
        if len(parts) == 2:
            break

    if not parts:
        return f"{seconds:.2f} seconds"

    return " ".join(parts)


def ordered_unique(iterable):
    seen = set()
    unique_items = []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)
    return tuple(unique_items)

charlist = ("A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "]", "[", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "{", "}", "|", ":", ";", "\"", "'", "<", ">", ",", ".", "?", "/", "~", "`", " ", "\\", " ")
additionalchar = ("¡", "¢", "£", "¤", "¥", "¦", "§", "¨", "©", "ª", "«", "¬", "®", "¯", "°", "±", "²", "³", "´", "µ", "¶", "·", "¸", "¹", "º", "»", "¼", "½", "¾", "¿", "Ñ", "ñ", "Ç", "ç", "Ö", "ö", "Ü", "ü", "Ä", "ä", "ß", "Α", "Β", "Γ", "Δ", "Ε", "Ζ", "Η", "Θ", "Ι", "Κ", "Λ", "Μ", "Ν", "Ξ", "Ο", "Π", "Ρ", "Σ", "Τ", "Υ", "Φ", "Χ", "Ψ", "Ω", "α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ", "λ", "μ", "ν", "ξ", "ο", "π", "ρ", "σ", "τ", "υ", "φ", "χ", "ψ", "ω")
BASE_CHAR_SET = set(charlist)
ADDITIONAL_CHAR_SET = set(additionalchar)
EXTENDED_CHARSET = charlist + tuple(ch for ch in additionalchar if ch not in BASE_CHAR_SET)
DEFAULT_GUESSES_PER_SECOND = 1_000_000
passlist = ("1234", "password", "letmein", "qwerty", "abc123", "welcome", "admin", "login", "123456", "iloveyou", "welcome1", "password1", "12345", "123456789", "football", "monkey", "dragon", "baseball", "master", "hello", "freedom", "whatever", "qazwsx", "trustno1", "")
ACTIVE_EXTENDED_CHARSET = EXTENDED_CHARSET
contains_only_base_chars = True
contains_additional_chars = False
missing_characters = ()


def analyze_charset_requirements(password):
    contains_only_base = all(ch in BASE_CHAR_SET for ch in password)
    contains_additional = any(ch in ADDITIONAL_CHAR_SET for ch in password)
    missing_chars = ordered_unique(
        ch for ch in password if ch not in BASE_CHAR_SET and ch not in ADDITIONAL_CHAR_SET
    )
    extended_charset = EXTENDED_CHARSET + missing_chars if missing_chars else EXTENDED_CHARSET
    return contains_only_base, contains_additional, missing_chars, extended_charset


def summarize_password(password, guess_rate, charset_label, charset_size):
    length = len(password)
    if length == 0:
        print("\nPassword Strength Report:\n- Empty password provided. Please supply at least one character.\n")
        return

    total_combinations = pow(charset_size, length)
    expected_attempts = max(1, total_combinations // 2)
    entropy_bits = length * math.log2(charset_size)

    best_case_seconds = 1 / guess_rate
    average_case_seconds = expected_attempts / guess_rate
    worst_case_seconds = total_combinations / guess_rate

    print("\nPassword Strength Report:")
    print(f"- Length: {length} characters")
    print(f"- Character set: {charset_label} ({charset_size} symbols)")
    print(f"- Estimated entropy: {entropy_bits:.2f} bits")
    print(f"- Total combinations: {humanize_number(total_combinations)}")
    print(f"- Expected attempts: {humanize_number(expected_attempts)}")
    print(f"- Assumed cracking speed: {humanize_number(int(guess_rate))} guesses/sec")
    print(f"- Best case (first try): {format_duration(best_case_seconds)}")
    print(f"- Average case (~50% space): {format_duration(average_case_seconds)}")
    print(f"- Worst case (full space): {format_duration(worst_case_seconds)}\n")
target_password = input("Enter the password to test: ")
printmode = parse_bool(input("Enable print mode? (True/False): "), default=False)

guess_rate_input = input(
    f"Estimated guesses per second (press Enter for {DEFAULT_GUESSES_PER_SECOND:,}): "
).strip()
try:
    guess_rate = float(guess_rate_input) if guess_rate_input else float(DEFAULT_GUESSES_PER_SECOND)
except ValueError:
    print("Invalid guess rate provided. Falling back to default value.")
    guess_rate = float(DEFAULT_GUESSES_PER_SECOND)

if guess_rate <= 0:
    print("Guesses per second must be positive. Falling back to default value.")
    guess_rate = float(DEFAULT_GUESSES_PER_SECOND)

simulate_bruteforce = parse_bool(
    input("Run brute-force simulation? (True/False): "),
    default=True,
)

maxlength = len(target_password)
target_chars = tuple(target_password)

(
    contains_only_base_chars,
    contains_additional_chars,
    missing_characters,
    ACTIVE_EXTENDED_CHARSET,
) = analyze_charset_requirements(target_password)

found_event = threading.Event()
print_lock = threading.Lock()
MAX_WORKERS = min(32, (os.cpu_count() or 1) * 2)
CHARS_PER_TASK = 4


def attempt_password(candidate_tuple):
    if found_event.is_set():
        return True

    candidate_str = None
    if printmode:
        candidate_str = ''.join(candidate_tuple)
        with print_lock:
            print(f"Trying password: {candidate_str}")

    if candidate_tuple == target_chars:
        if candidate_str is None:
            candidate_str = ''.join(candidate_tuple)
        with print_lock:
            print(f"Password found: {candidate_str}")
        found_event.set()
        return True

    return False


def enqueue_tasks(charset, task_queue):
    char_len = len(charset)
    if maxlength == 0:
        return
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
                if attempt_password((ch,)):
                    return
                if found_event.is_set():
                    return
            continue

        iterables = [first_slice] + [charset] * (length - 1)
        for attempt in itertools.product(*iterables):
            if attempt_password(attempt):
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
    if maxlength == 0:
        print("Empty password provided. Nothing to simulate.")
        return True

    if target_password in passlist:
        print(f"Password found in password list: {target_password}")
        return True

    if not contains_only_base_chars:
        if missing_characters:
            print(
                "Detected characters outside the configured sets. Adding your custom symbols to the search..."
            )
        else:
            print("Detected characters outside the base set. Using the extended character list...")

        if run_checks_with_charset(ACTIVE_EXTENDED_CHARSET):
            return True
        print("Password not found within the specified length range.")
        return False

    if run_checks_with_charset(charlist):
        return True

    if contains_additional_chars or missing_characters:
        print("Base search exhausted. Password appears to require additional characters. Expanding...")
    else:
        print("Base search exhausted. Expanding to the extended set as a fallback...")

    if run_checks_with_charset(ACTIVE_EXTENDED_CHARSET):
        return True

    print("Password not found within the specified length range.")
    return False


def run_bruteforce_simulation():
    if maxlength == 0:
        print("Empty password provided. Skipping brute-force simulation.")
        return False

    input("Press Enter to start the brute-force simulation...")
    start_ns = time.time_ns()
    start_stamp = time.strftime("%H:%M:%S", time.localtime())
    print(f"Simulation started at {start_stamp} local time.")

    found = trypassword()

    end_ns = time.time_ns()
    elapsed_seconds = (end_ns - start_ns) / 1_000_000_000
    print(
        f'Password "{target_password}" took {format_duration(elapsed_seconds)} in this simulation.'
    )
    return found


def report_and_optionally_simulate():
    charset_label = "base character set"
    charset_size = len(charlist)

    if not contains_only_base_chars or contains_additional_chars or missing_characters:
        charset_size = len(ACTIVE_EXTENDED_CHARSET)
        charset_label = "custom extended character set" if missing_characters else "extended character set"

    summarize_password(target_password, guess_rate, charset_label, charset_size)

    if missing_characters:
        custom_preview = " ".join(repr(ch) for ch in missing_characters)
        print(f"Added custom characters for analysis: {custom_preview}")

    if not target_password:
        print("No password supplied. Exiting without simulation.")
        return

    if not simulate_bruteforce:
        print("Brute-force simulation skipped by user request.")
        return

    run_bruteforce_simulation()


report_and_optionally_simulate()