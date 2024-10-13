# AtcoderEnv for c++
Script to create AtCoder environment for C++
- Create a directory structure for each problem
- Place template code and test code for each question
- Scraping and downloading sample tests
- Validate sample tests on test code

## How to use
### setup
- create virtual environment and install requirements
```
python venv -m venv venv
pip install -r requirements.txt
source venv/bin/activate
```

- create config.ini
```
[User]
username = <username>
password = <password>
```

- run setup.py with contest title and contest number
```
python setup.py <contest title> <contest number>
```

### compile
```sh
g++ main.cpp
a.out
```

### run test
- output result and running time
```sh
g++ main_test.cpp
a.out
```

## Example
```sh
python setup.py abc 199
g++ main.cpp
a.out
```

## Directory structure
```
AtCoderEnv/
├── setup.py
├── config.ini
└── template/
└── contests/
    └── <contest_title>/             # e.g., abc/
        └── <contest_number>/        # e.g., 199/
            └── <question_alphabet>/ # e.g., abc199_a/
                ├── main.cpp         # template file
                ├── main_test.cpp    # template file
                └── sample/          # directory for test cases
                    ├── 1.in         # input file for test case 1
                    ├── 1.out        # output file for test case 1
                    ├── ...          # more test cases
                    ├── n.in         # input file for test case n
                    └── n.out        # output file for test case n
            └──...                   # more questions
```

## Requirements
- Python 3.10 or later

## License
MIT
