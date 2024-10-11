# AtcoderEnv for c++
Script to create AtCoder environment for C++
- Create a directory structure for each problem
- Place template code and test code for each question
- Scraping and downloading sample tests
- Validate sample tests on test code

## How to use
- create `<contest title>` directory and download testcases
    - create `<question_alphabet>` directory
        - `main.cpp`      # copied by sample dir
        - `main_test.cpp` # same as above
        - `sample/`       # downloaded testcases
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