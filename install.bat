@echo off

REM Create a virtual environment called dnd-env
python -m venv dnd-env

REM Activate the virtual environment
call dnd-env\Scripts\activate.bat

REM Update pip
python -m pip install --upgrade pip

REM Install the requirements from requirements.txt
pip install -r requirements.txt

REM Pause to see any messages before the script closes
pause
