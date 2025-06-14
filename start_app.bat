@echo off
REM This batch file sets up the environment and runs the Flask app

REM Create virtual environment if it doesn't exist
if not exist venv (
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install requirements
pip install -r requirements.txt

REM Download SpaCy English model if not already present
python -m spacy download en_core_web_sm

REM Start the Flask app
python app.py
