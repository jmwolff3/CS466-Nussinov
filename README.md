# CS466-Nussinov
Implementation of Nussinov's Algorithm for CS466

### Installation
This program is designed to run using python 3.7+.

It is recommended you use a virtual environment when installing packages.

1. Clone the repository and cd into the directory
2. Create a virtual environment and activate it
3. Install the requirements

```bash
pip install -r requirements.txt
```
4. Create a .env file `touch .env` and add `SECRET_KEY="<secret_key>"`, where secret key is a 32 character string.
5. Run `python flask_app.py`
6. Navigate to `localhost:5000`.

### Docker
1. Run `docker build`
2. Run `docker run -d -it --name nuss --rm  -p 5000:5000 nussinov`
3. Navigate to `localhost:5000`

### Command Line interface
1. `pip install numpy`
2. `python nussinov/nussinov.py`
Include either the `-s` option and a sequence string or `-f` and a filepath to your sequence.

### Build and run C code
1. If you are on a mac, install argp: `brew install argp-standalone` or 
2. Compile: `gcc -largp c_implimentaiton/nussinov.c -o nussinov.o`
3. Run: `./nussinov.o -s <sequence>`
