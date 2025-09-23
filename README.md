# AtCoderEnv for C++

Script to create AtCoder environment for C++

- Create a directory structure for each problem
- Place template code and test code for each question
- Scraping and downloading sample tests with CloudFlare protection support
- Validate sample tests on test code

## Features

- **CloudFlare Support**: Handles AtCoder's CloudFlare Turnstile authentication
- **Cookie Management**: Saves login session for reuse
- **Manual Login**: Opens Chrome browser for secure authentication
- **Automatic Setup**: Creates complete contest directory structure

## How to use

### Setup

- Create virtual environment and install requirements

```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
pip install -r requirements.txt
```

- Create config.ini (optional - now uses manual login)

```ini
[user]
username = <your_atcoder_username>
password = <your_atcoder_password>
```

**Note**: Due to CloudFlare protection, the script now uses manual browser login instead of config.ini credentials.

### Running the setup script

```bash
python setup.py <contest_name> <contest_number>
```

### Initial Login Process (First Time)

1. Script will open Chrome browser automatically
2. Login to AtCoder manually in the opened browser
3. Complete any CloudFlare Turnstile challenges
4. Open Chrome DevTools (F12 or Cmd+Option+I)
5. Navigate: Application → Storage → Cookies → https://atcoder.jp
6. Find and copy the `REVEL_SESSION` cookie value
7. Paste the cookie value in the terminal when prompted
8. The script will save cookies for future use

### Subsequent Runs

- Saved cookies will be used automatically
- If cookies expire, manual login will be required again

### Compile and run

```bash
cd contests/<contest_name>/<contest_number>/<problem_name>
g++ main.cpp -o main
./main
```

### Run tests

- Output result and running time

```bash
g++ main_test.cpp -o test
./test
```

## Example Usage

```bash
# Set up ABC 423 contest
python setup.py abc 423

# Navigate to problem A
cd contests/abc/423/abc423_a

# Write your solution in main.cpp, then compile and run
g++ main.cpp -o main
./main

# Test with sample cases
g++ main_test.cpp -o test
./test
```

## Troubleshooting

### CloudFlare Issues

- If manual login fails, try using an incognito/private browser window
- Ensure you can see "Sign Out" in the AtCoder top menu before copying cookies
- The `REVEL_SESSION` cookie is essential for authentication

### Cookie Expiration

- If you get authentication errors, delete `atcoder_cookies.json` and run the script again
- Cookies typically expire after some time and need to be refreshed

### Browser Issues

- If Chrome doesn't open automatically, manually navigate to `https://atcoder.jp/login`
- The script works best with Google Chrome due to DevTools instructions

## Directory Structure

```
AtCoderEnv/
├── setup.py                        # Main setup script
├── config.ini                      # Optional config file
├── requirements.txt                 # Python dependencies
├── atcoder_cookies.json            # Saved login cookies (auto-generated)
├── template/
│   ├── main.cpp                    # Template for solution
│   └── main_test.cpp               # Template for testing
└── contests/
    └── <contest_name>/             # e.g., abc/
        └── <contest_number>/       # e.g., 423/
            └── <problem_name>/     # e.g., abc423_a/
                ├── main.cpp        # Solution template
                ├── main_test.cpp   # Test template
                └── sample/         # Sample test cases
                    ├── 1_input.txt
                    ├── 1_output.txt
                    ├── 2_input.txt
                    ├── 2_output.txt
                    └── ...
            └── <problem_name>/     # e.g., abc423_b/
                └── ...
```

## Requirements

- Python 3.10 or later
- Google Chrome browser
- macOS, Linux, or Windows
- Internet connection for AtCoder access

## Dependencies

- `requests`: HTTP requests
- `beautifulsoup4`: HTML parsing
- `subprocess`: Browser launching
- `json`: Cookie management

## License

MIT
