# UnZiper: A ZIP Archive Password Cracker

## Overview
UnZiper is a Python-based tool designed to crack passwords of ZIP archives using various techniques. Its goal is to assist in testing the robustness of password-protected files. The application provides multiple methods to attempt password recovery, making it versatile and adaptable to different use cases.

## Key Features
1. **RockYou Dictionary Attack**: 
   - Leverages the widely-used `rockyou.txt` wordlist to try common passwords.
2. **Brute Force Attack**: 
   - Systematically generates and tests all possible password combinations up to 10 characters.
3. **Custom Wordlist Attack**: 
   - Uses a user-provided wordlist to test passwords specific to a certain context or target.
4. **Custom Pattern Matching**: 
   - Attempts password recovery based on user-defined patterns, allowing fine-grained control over the cracking process.

## How to Use

### Basic Command
```bash
python UnZiper.py -f <filename> [options]
```

### Options
- **General Options**:
  - `-h, --help`: Display help information.
  - `-v, --verbose`: Show all attempted passwords.
  - `-f, --file`: Specify the ZIP file to crack.
  
- **Cracking Methods**:
  - `-r, --rockyou`: Use the `rockyou.txt` wordlist.
  - `-b, --brute`: Perform a brute-force attack.
  - `-i, --input`: Use a custom wordlist.
  - `-c, --custom`: Attempt passwords based on a pattern.
  - `-a, --all`: Use all available methods sequentially.

### Examples
1. Crack using the `rockyou.txt` wordlist:
   ```bash
   python UnZiper.py -f archive.zip -r
   ```
2. Perform a brute-force attack:
   ```bash
   python UnZiper.py -f archive.zip -b
   ```
3. Use a custom wordlist:
   ```bash
   python UnZiper.py -f archive.zip -i custom_wordlist.txt
   ```
4. Define a custom pattern:
   ```bash
   python UnZiper.py -f archive.zip -c "[a-z][0-9]"
   ```

## Requirements
- Python 3.x
- Libraries: `pyzipper`, `itertools`
- For the RockYou attack, ensure the `rockyou.txt` file is located in the `utils` directory.

## Disclaimer
This tool is intended for educational purposes and authorized security testing only. Misuse of this tool for unauthorized access or illegal activities is strictly prohibited and may result in severe legal consequences.
