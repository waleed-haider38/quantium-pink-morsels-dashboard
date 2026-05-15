python -m venv venv
source venv/bin/activate
pip install dash pandas
pip install "dash[testing]"
pip freeze > requirements.txt