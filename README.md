# Czech National Bank (CNB) official foreign exchange rates scraper

The official exchange rates for CZK can be found at https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/rok_form.html
This script scrapes the data for a custom time range, as long as the requested years are available (currently 1991 - 2023).

The requirements are python 3+ (development version 3.9.6 should be guaranteed to work) and packages listed in requirements.txt 
(pandas, requests and dependencies).

The script can be used as separate mini-module, which is why the __init__.py file is included. To import it, 
make sure the module's directory is included in PYTHONPATH. This can be setup in a project with:
```python
import sys
MODULE_PATH = 'path/to/the/module'  # should contain the directory to the file where the .py files are located
if not MODULE_PATH in sys.path:
    sys.path.append(MODULE_PATH)
```
Or by manual export to Environment Variable in zprofile.sh (for macOS)
```bash
export PYTHONPATH=$PYTHONPATH:/path/to/the/module
```

The main.py file shows en example how it could be used to export the data to csv file

## Black Box Solution
For those that are not interested in the inner workings or even do not want to understand and simply need the output, 
<<<<<<< HEAD
there is a prepared blackbox solution for MacOS/Linux. This might require installing developer-tools, xcode or similar.
=======
there is a prepared blackbox solution for macOS.
>>>>>>> f34bf59 (change project structure, fix warnings and typos, update README, add automatic year detection)

* In the Terminal application, verify that git is installed, by running:
```bash
git status
```
This should output something like: _fatal: not a git repository_. If so, proceed to the next step.

If the output says _git not found_, or the Terminal prompts you to install developer tools, X-code, then **git** is not installed.
You can install command line tools and proceed to the next step.
Alternatively you can install git with **homebrew**:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
followed by:
```bash
brew install git
```
The installation of **homebrew** might take a minute. You will be prompted for your password.

* Next, make a clone of this repository:
This default solution will create a folder in your Desktop, where everything happens
```bash
cd Desktop
git clone https://github.com/LukasKrivka/cnb-rates
```

* Finally, run a prepared bash script.
```bash
cd cnb-rates
bash setup.sh
```
This will handle everything else (python environment, packages, and execution).
The default option for this method is filled dataset - which means the missing dates (weekends etc.) 
are going to be filled with previous value.
The exported csv should appear on your Desktop. Then you can delete the CNB-rates cloned file to clean up.

#### OR
<<<<<<< HEAD
The entire repository can be downloaded as zipfile by adding '/zipball/master/' to the end of the github link in browser.
Then the automatic execution can be run with
```bash
cd Downloads
open LukasKrivka-CNB-rates-SUFFIX.zip
cd LukasKrivka-CNB-rates-SUFFIX
bash simple_run.sh
=======
The entire repository can be downloaded as zipfile by adding '/zipball/master/' to the end of the gitHub link.
Then the automatic execution can be run with
```bash
cd Downloads
open LukasKrivka-cnb-rates-20fd4a3.zip
cd LukasKrivka-cnb-rates-20fd4a3
bash setup.sh
>>>>>>> f34bf59 (change project structure, fix warnings and typos, update README, add automatic year detection)
```
The SUFFIX in the file name will be unique - you need to change it to the name of your particular file name.

## Final remarks:
This script was developed mainly for my own needs. I am not necessarily planing on extending or updating functionality
or maintaining support for subsequent dependencies releases. Noting in this script or reposiory is guaranteed.
