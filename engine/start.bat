@echo off
echo Starting MK PRO Trading Engine...
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
pause