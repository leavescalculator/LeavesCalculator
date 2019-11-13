# LeavesCalculator
This is the repository for a web app that is designed for Portland State University's HR department 
to assist PSU employees with determining the amount and types of leave they are eligible for.

This app uses Django, REST, Vue.js, NPM, and SQLite3 frameworks, and is released under MIT license.

## Cloning the project
1. Change directory to where you want the LeavesCalculator directory to be created
2. Run `git clone https://github.com/leavescalculator/LeavesCalculator.git` 

## Getting Started
1. Change directory into the LeavesCalculator directory and run the following commands: 
2. `chmod +x startup_script` Might be necessary, which gives startup_script executable permission
3. `./start` Runs a script that will install dependencies and spin up Django and Vue servers
4. `./start install` Will install dependencies without running the servers
5. `./start run` Will spin up the servers without attempting to install dependencies
6. Make changes to the code base as you require
7. To kill the servers, use control+C to exit the script, which will in turn kill the servers
