import sys
import pyzipper
import itertools
import os


verbose = False
zip_file_path = None
valid_options = ['-f', '--file', '-v', '--verbose', '-h', '--help', '-r', '--rockyou', '-b', '--brute', '-d', '--dictionary', '-i', '--input', '-a', '--all', '-c', '--custom']
number_of_threads = 1


def print_help():
    print("Usage: python UnZiper.py <filename> (options)")
    print("Options:")
    print("  -h, --help       Show this help message and exit.")
    print("  -v, --verbose    Show all the passwords tried.")
    print("  -f, --file       Specify the file to crack.")
    print("Cracking options:")
    print("  -r, --rockyou    Use the rockyou.txt wordlist to crack the password.")
    print("  -b, --brute      Brute force the password.")
    print("  -i, --input      Use a custom wordlist to crack the password.")
    print("  -c, --custom     Try to guess the password after a custom pattern.")
    print("  -a, --all        Try all the options.")
    sys.exit(0)


def try_password(password):
    global zip_file_path

    try:
        with pyzipper.AESZipFile(zip_file_path) as zf:
            zf.pwd = password.encode()
            zf.extractall()
        print(f"Password found: {password}")
        return True
    except RuntimeError as e:
        if 'Bad password for file' in str(e):
            if verbose:
                print(f"Failed with password: {password}")
            return False
        else:
            print(f"Error: {e}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def rockyou_crack():
    with open('utils/rockyou.bin', 'rb') as passwords:
        for password in passwords:
            password = password.strip().decode()
            if try_password(password):
                sys.exit(0)


def brute_force_crack():
    alfa_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@$#&* {}[],=-().+;'

    for length in range(1, 11):
        for password_tuple in itertools.product(alfa_chars, repeat=length):
            password = ''.join(password_tuple)
            if try_password(password):
                sys.exit(0)


def custom_wordlist_crack(wordlist):
    wordlist_path = os.path.abspath(wordlist)
    if not wordlist_path.endswith('.txt'):
        print("Error: The file must be a .txt file.")
        sys.exit(1)

    if not os.path.exists(wordlist_path):
        print(f"Error: The file {wordlist_path} does not exist.")
        sys.exit(1)

    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as passwords:
        for password in passwords:
            password = password.strip()
            if try_password(password):
                sys.exit(0)


def custom_crack(pattern):
    def expand(token):
        if '-' in token:
            start, end = token.split('-')
            return [chr(i) for i in range(ord(start), ord(end) + 1)]
        return list(token)

    def parse_pattern(regex):
        parts = []
        i = 0
        while i < len(regex):
            if regex[i] == '[':
                j = regex.index(']', i)
                parts.append(expand(regex[i + 1:j]))
                i = j + 1
            elif regex[i].isdigit() or regex[i] == '{':
                if regex[i] == '{':
                    j = regex.index('}', i)
                    n = int(regex[i + 1:j])
                    parts[-1] = parts[-1] * n
                    i = j + 1
                else:
                    parts.append([regex[i]])
                    i += 1
            else:
                parts.append([regex[i]])
                i += 1
        return parts

    parts = parse_pattern(pattern)

    combinations = itertools.product(*parts)
    for combination in combinations:
        password = ''.join(combination)
        if try_password(password):
            sys.exit(0)


def main():
    global verbose, zip_file_path, number_of_threads

    options = [arg for arg in sys.argv if arg.startswith('-')]

    for option in options:
        if option not in valid_options:
            print(f"Error: Invalid argument {option}")
            sys.exit(1)

    if '-v' in options or '--verbose' in options:
        verbose = True

    if '-f' in options or '--file' in options:
        if '-f' in options:
            zip_file_path = sys.argv[sys.argv.index('-f') + 1]
        else:
            zip_file_path = sys.argv[sys.argv.index('--file') + 1]
    else:
        print("Error: You must specify a file to crack.")
        sys.exit(1)

    if '-t' in options or '--threads' in options:
        if '-t' in options:
            number_of_threads = int(sys.argv[sys.argv.index('-t') + 1])
        else:
            number_of_threads = int(sys.argv[sys.argv.index('--threads') + 1])

    if option in ['-h', '--help']:
        print_help()
    elif '-r' in options or '--rockyou' in options:
        rockyou_crack()
    elif '-b' in options or '--brute' in options:
        brute_force_crack()
    elif '-c' in options or '--custom' in options:
        if '-c' in options:
            custom_crack(sys.argv[sys.argv.index('-c') + 1])
        else:
            custom_crack(sys.argv[sys.argv.index('--custom') + 1])
    elif '-i' in options or '--input' in options:
        if '-i' in options:
            custom_wordlist_crack(sys.argv[sys.argv.index('-i') + 1])
        else:
            custom_wordlist_crack(sys.argv[sys.argv.index('--input') + 1])
    elif '-a' in options or '--all' in options:
        rockyou_crack()
        brute_force_crack()


if __name__ == '__main__':
    main()
