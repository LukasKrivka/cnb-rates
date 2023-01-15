# Czech National Bank (CNB) official foreign exchange rates

The data can be found at https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/rok_form.html
This script scrapes the data for custom time range, as long as the requested years are available (currently 1991 - 2023).

The requirements are python 3+ (development version 3.9.6 should be garanteed to work) and packages listed in requirements.txt (pandas, requests and dependencies).
The script can be used as separate mini-module, which is why the __init__.py file is included. To import i, make sure the module's directory is included in PYTHONPATH. More in practical information is in notes.txt. 

### Final remarks:
This script was developed mainly for my own needs. I am not necessarily planing on extending functionality (like sql connection) or maintaining support for subsequent dependencies releases. Noting in this script or reposiory is guaranteed.
