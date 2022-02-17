1. Install python 3.6-3.8
## To Run webscraper.py in Terminal
2. Create a virtual environment inside the `datasci-bay-area-relief-data-mining` directory or whatever you called the project.
   1. ```python3 -m venv ./venv``` in terminal
3. Activate your virtual environment in terminal:
   1. ```source venv/bin/activate```
4. Install the project dependencies:
   1. ```pip install -r requirements.txt```
5. Install chromedriver for your specific version of Chrome
   1. i.e. 98.0.4758.102 -- Find this in Settings/About Chrome
   2. Visit https://chromedriver.chromium.org/downloads and look for a driver that has the same major version number (aka 98)
   3. Download it and add it to your PATH (i.e. `usr/local/bin`).
   4. If `/usr/local/bin` is not in your PATH already, add it by updating your PATH variable in your `.bashrc`, `.bash_profile`, `.zshrc` depending on shell.
      1. try ```sudo vi /etc/paths``` in terminal.
      2. or adding ```export PATH=$PATH: /path/to/set``` to your shells profile file, then `source` it.
6. Run the crawler using your python virtual environment:
   1. If it's running globally and getting errors, make sure you've completed steps 1-4 in the root directory.
   2. ```python googlescraper/webscraper.py```

## To Run webscraper.py with a version of PyCharm
2. Create an interpretter -> virtual environment 
   1. By default this should create a `venv` environment in your project directory.
3. PyCharm will activate it for you after you create and choose it. 
4. Install `chromedriver` in the same manner as #5 above.
5. Run `webscraper.py` by creating a run configuration or right mouse clicking on `webscraper.py` in the project explorer.