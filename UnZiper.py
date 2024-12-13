import sys
import pyzipper
import itertools


verbose = False
zip_file_path = None
valid_options = ['-v', '--verbose']


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
    with open('utils/rockyou.txt', 'r', errors='ignore') as passwords:
        for password in passwords:
            password = password.strip()
            if try_password(password):
                sys.exit(0)


def brute_force_crack():
    alfa_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@$#&* {}[],=-().+;'

    for length in range(1, 11):
        for password_tuple in itertools.product(alfa_chars, repeat=length):
            password = ''.join(password_tuple)
            if try_password(password):
                sys.exit(0)


if len(sys.argv) < 2:
    print("Usage: python UnZiper.py <filename> (options)")
else:
    options = sys.argv[2:]
    zip_file_path = sys.argv[1]
    print(zip_file_path)

    for option in options:
        if option not in valid_options:
            print(f"Error: Invalid argument {option}")
            sys.exit(1)

    if '-v' in options or '--verbose' in options:
        verbose = True

    if not zip_file_path.endswith('.zip'):
        print("Error: The file must be a .zip file.")
    else:
        # rockyou_crack()
        brute_force_crack()
