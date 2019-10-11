# LeavesCalculator
This is the repository for a web app that is designed for Portland State University's HR department 
to assist PSU employees with determining the amount and types of leave they are eligible for.

This app uses Django, REST, Vue.js, and SQLite3 frameworks, and is released under MIT license.

## Cloning the project
1. Change directory to where you want the LeavesCalculator directory to be created
2. Run `git clone https://github.com/leavescalculator/LeavesCalculator.git` 

## Getting Started
1. Change directory into the LeavesCalculator directory and run the following commands: 
2. `pip3 install virtualenv` Installs the virtual environment tool
3. `virtualenv env` Creates a directory env that contains a virtual environment
4. `source env/bin/activate` Will activate the virtual environment
5. `pip3 install -r requirements.txt` Will install the dependencies listed in requirements.txt
6. Make changes to the code base as you require
7. When you are done making changes, use `deactivate` to close the virtual environment

## Running the server
1. If your virtual environment is not active, activate it with `source env/bin/activate`
2. Run `python3 manage.py runserver` from the root of the LeavesCalculator directory to start the django server
3. Access `http://localhost:8000` to view the index page of the project
4. Deactivate the server by pressing control+c
5. Deactivate the virtual environment by running `deactivate`