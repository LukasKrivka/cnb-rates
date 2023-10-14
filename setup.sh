python3 -m venv rates-venv
source rates-venv/bin/activate
pip3 install -r requirements.txt || pip3 install pandas==1.5.2 pytz==2022.7.1 requests==2.28.2
python3 src/main.py
deactivate
#rm -r rates-venv
